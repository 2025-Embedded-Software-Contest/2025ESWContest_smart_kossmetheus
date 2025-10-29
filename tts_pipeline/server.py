#!/usr/bin/env python3
"""Wyoming TTS server that wraps the local VoxCPM tts_pipeline."""

from __future__ import annotations

import argparse
import asyncio
import logging
import shutil
import os
import shlex
import signal
import subprocess
import sys
import tempfile
import time
import wave
from dataclasses import dataclass
from functools import partial
from importlib import metadata
from pathlib import Path
from typing import Callable, Dict, Iterable, Optional

from wyoming.audio import AudioChunk, AudioStart, AudioStop
from wyoming.error import Error
from wyoming.event import Event
from wyoming.info import Attribution, Describe, Info, TtsProgram, TtsVoice, TtsVoiceSpeaker
from wyoming.server import AsyncEventHandler, AsyncServer
from wyoming.tts import Synthesize, SynthesizeStart, SynthesizeStop

from .synth_voxcpm import synth
from .text_frontend import ko_text_frontend

PCM_SAMPLE_RATE = 16_000
PCM_WIDTH = 2
PCM_CHANNELS = 1
DEFAULT_MAX_TEXT_LENGTH = 1_000

_LOGGER = logging.getLogger(__name__)


try:  # Optional; only used for logging voice asset metadata
    import soundfile as sf  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    sf = None


@dataclass(frozen=True)
class VoicePreset:
    """Prompt assets required for speaker-adapted synthesis."""

    speaker: str
    prompt_wav: Path
    prompt_text: Optional[str]


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:  # pragma: no cover - defensive
        raise argparse.ArgumentTypeError("expected integer") from exc

    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be > 0")

    return parsed


def run_ffmpeg(args: Iterable[str]) -> None:
    """Execute ffmpeg command and surface errors with logging."""

    quoted = " ".join(shlex.quote(str(a)) for a in args)
    _LOGGER.debug("Executing: %s", quoted)
    try:
        subprocess.run(list(args), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError as exc:  # pragma: no cover - depends on environment
        raise RuntimeError("ffmpeg executable not found") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"ffmpeg command failed: {quoted}") from exc


class PipelineSynthesizer:
    """Thread-safe wrapper around the tts_pipeline synthesis stages."""

    def __init__(
        self,
        *,
        cfg_value: float,
        inference_steps: int,
        use_denoise: bool,
        use_normalize: bool,
        fallback_voice: Optional[VoicePreset],
        frontend: Optional[Callable[[str], str]],
        ffmpeg_bin: str = "ffmpeg",
    ) -> None:
        self.cfg_value = cfg_value
        self.inference_steps = inference_steps
        self.use_denoise = use_denoise
        self.use_normalize = use_normalize
        self._fallback_voice = fallback_voice
        self._frontend = frontend
        self._ffmpeg_bin = ffmpeg_bin
        self._lock = asyncio.Lock()

    def update_fallback_voice(self, voice: VoicePreset) -> None:
        """Refresh fallback voice metadata after on-disk changes."""
        self._fallback_voice = voice


    async def synthesize(
        self,
        *,
        text: str,
        prompt_wav: Optional[Path],
        prompt_text: Optional[str],
    ) -> tuple[bytes, float, float]:
        """Run the pipeline for a single request and return PCM audio."""

        async with self._lock:
            start = time.perf_counter()
            pcm, duration = await asyncio.to_thread(
                self._synthesize_blocking,
                text,
                prompt_wav,
                prompt_text,
            )
            wall = time.perf_counter() - start
        return pcm, duration, wall

    def _synthesize_blocking(
        self,
        text: str,
        prompt_wav: Optional[Path],
        prompt_text: Optional[str],
    ) -> tuple[bytes, float]:
        voice = self._select_voice(prompt_wav, prompt_text)
        processed_text = self._frontend(text) if self._frontend else text

        with tempfile.TemporaryDirectory(prefix="tts_pipeline_") as tmp_dir_str:
            tmp_dir = Path(tmp_dir_str)
            prompt_copy = tmp_dir / "prompt.wav"
            raw_out = tmp_dir / "raw.wav"

            # Work on a copy so that ensure_format() can safely rewrite the file.
            shutil.copy2(voice.prompt_wav, prompt_copy)

            synth(
                processed_text,
                voice.prompt_text or "",
                prompt_copy,
                raw_out,
                self.cfg_value,
                self.inference_steps,
                self.use_denoise,
                self.use_normalize,
            )

            pcm, duration = self._read_wav_as_pcm(raw_out)

        return pcm, duration

    def _select_voice(
        self,
        prompt_wav: Optional[Path],
        prompt_text: Optional[str],
    ) -> VoicePreset:
        if prompt_wav is not None:
            return VoicePreset("custom", prompt_wav, prompt_text)
        if self._fallback_voice is None:
            raise RuntimeError("No prompt audio supplied and no fallback voice configured")
        if prompt_text is not None:
            return VoicePreset(
                self._fallback_voice.speaker,
                self._fallback_voice.prompt_wav,
                prompt_text,
            )
        return self._fallback_voice

    def _read_wav_as_pcm(self, wav_path: Path) -> tuple[bytes, float]:
        with tempfile.NamedTemporaryFile(prefix="tts_pcm_", suffix=".wav", delete=False) as tmp:
            tmp_name = Path(tmp.name)
        try:
            run_ffmpeg(
                (
                    self._ffmpeg_bin,
                    "-y",
                    "-i",
                    str(wav_path),
                    "-ac",
                    str(PCM_CHANNELS),
                    "-ar",
                    str(PCM_SAMPLE_RATE),
                    "-sample_fmt",
                    "s16",
                    str(tmp_name),
                )
            )

            with wave.open(str(tmp_name), "rb") as wav_file:
                rate = wav_file.getframerate()
                width = wav_file.getsampwidth()
                channels = wav_file.getnchannels()
                frames = wav_file.getnframes()
                audio = wav_file.readframes(frames)

            if rate != PCM_SAMPLE_RATE or width != PCM_WIDTH or channels != PCM_CHANNELS:
                raise RuntimeError("Unexpected PCM format after ffmpeg conversion")

            duration = frames / float(rate) if rate else 0.0
            return audio, duration
        finally:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass


class PipelineEventHandler(AsyncEventHandler):
    """Handles Wyoming events by dispatching into the pipeline."""

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        *,
        synthesizer: PipelineSynthesizer,
        voices: Dict[str, VoicePreset],
        fallback_voice: VoicePreset,
        voices_dir: Optional[Path],
        fallback_prompt_text_source: Optional[Path],
        model_name: str,
        attribution: Attribution,
        package_version: Optional[str],
        max_text_length: int,
        languages: Iterable[str],
    ) -> None:
        super().__init__(reader, writer)
        self._synthesizer = synthesizer
        self._voices = voices
        self._fallback_voice = fallback_voice
        self._voices_dir = voices_dir
        self._voices_snapshot = self._scan_voice_dir()
        self._fallback_prompt_text_source = fallback_prompt_text_source
        self._fallback_mtime = self._stat_mtime(fallback_voice.prompt_wav)
        self._model_name = model_name
        self._attribution = attribution
        self._package_version = package_version
        self._max_text_length = max_text_length
        self._languages = list(languages)

    def _stat_mtime(self, path: Path) -> Optional[float]:
        if path is None:
            return None
        try:
            return path.stat().st_mtime
        except FileNotFoundError:
            _LOGGER.warning("Prompt audio '%s' not found", path)
            return None

    def _scan_voice_dir(self) -> Dict[Path, float]:
        if not self._voices_dir:
            return {}
        snapshot: Dict[Path, float] = {}
        if self._voices_dir.exists():
            for wav_path in self._voices_dir.glob("*.wav"):
                try:
                    snapshot[wav_path] = wav_path.stat().st_mtime
                except FileNotFoundError:
                    continue
                text_path = wav_path.with_suffix(".txt")
                if text_path.exists():
                    try:
                        snapshot[text_path] = text_path.stat().st_mtime
                    except FileNotFoundError:
                        continue
        return snapshot

    def _refresh_fallback_voice(self) -> None:
        if self._fallback_voice is None:
            return
        current = self._stat_mtime(self._fallback_voice.prompt_wav)
        if current is None or current == self._fallback_mtime:
            return
        prompt_text = self._fallback_voice.prompt_text
        if self._fallback_prompt_text_source and self._fallback_prompt_text_source.exists():
            try:
                prompt_text = self._fallback_prompt_text_source.read_text(encoding='utf-8').strip() or None
            except Exception:
                _LOGGER.warning(
                    "Unable to reload fallback prompt text from %s",
                    self._fallback_prompt_text_source,
                    exc_info=True,
                )
        refreshed = VoicePreset(
            speaker=self._fallback_voice.speaker,
            prompt_wav=self._fallback_voice.prompt_wav,
            prompt_text=prompt_text,
        )
        self._fallback_voice = refreshed
        self._voices[refreshed.speaker.lower()] = refreshed
        self._synthesizer.update_fallback_voice(refreshed)
        self._fallback_mtime = current
        _LOGGER.info("Detected updated fallback prompt audio '%s'", refreshed.prompt_wav.name)

    def _refresh_voices_dir(self) -> None:
        if not self._voices_dir:
            return
        snapshot = self._scan_voice_dir()
        if snapshot == self._voices_snapshot:
            return
        _LOGGER.info("Reloading voice presets from %s", self._voices_dir)
        reloaded = load_voice_presets(self._voices_dir)
        self._voices = reloaded
        lower = self._fallback_voice.speaker.lower()
        updated = reloaded.get(lower)
        if updated:
            self._fallback_voice = updated
            self._synthesizer.update_fallback_voice(updated)
            self._fallback_mtime = self._stat_mtime(updated.prompt_wav)
        else:
            self._voices[lower] = self._fallback_voice
        self._voices_snapshot = snapshot

    async def handle_event(self, event: Event) -> bool:
        if Describe.is_type(event.type):
            await self._handle_describe()
            return True

        if Synthesize.is_type(event.type):
            synth_event = Synthesize.from_event(event)
            await self._handle_synthesize(synth_event)
            return True

        if SynthesizeStart.is_type(event.type):
            await self.write_event(
                Error(text="Streaming synthesis is not supported", code="not_supported").event()
            )
            return False

        if SynthesizeStop.is_type(event.type):
            return False

        _LOGGER.debug("Unhandled event type=%s", event.type)
        return True

    async def _handle_describe(self) -> None:
        _LOGGER.info("Describe request; reporting model '%s'", self._model_name)

        unique: Dict[str, VoicePreset] = {}
        unique[self._fallback_voice.speaker.lower()] = self._fallback_voice
        for key, preset in self._voices.items():
            unique.setdefault(key, preset)

        speakers = [
            TtsVoiceSpeaker(name=preset.speaker)
            for preset in sorted(unique.values(), key=lambda p: p.speaker.lower())
        ] or None

        voice = TtsVoice(
            name=self._model_name,
            languages=list(self._languages),
            speakers=speakers,
            attribution=self._attribution,
            installed=True,
            description="tts_pipeline VoxCPM synthesis",
            version=self._package_version,
        )

        program = TtsProgram(
            name=self._model_name,
            attribution=self._attribution,
            installed=True,
            description="tts_pipeline VoxCPM synthesis",
            version=self._package_version,
            voices=[voice],
            supports_synthesize_streaming=False,
        )

        await self.write_event(Info(tts=[program]).event())

    async def _handle_synthesize(self, synth_event: Synthesize) -> None:
        text = (synth_event.text or "").strip()
        if not text:
            await self.write_event(Error(text="Text must not be empty", code="empty_text").event())
            return

        if len(text) > self._max_text_length:
            await self.write_event(
                Error(
                    text=f"Text length exceeds {self._max_text_length} characters",
                    code="text_too_long",
                ).event()
            )
            return

        self._refresh_fallback_voice()
        self._refresh_voices_dir()

        requested: Optional[str] = None
        preset: Optional[VoicePreset] = None

        if synth_event.voice:
            requested = synth_event.voice.speaker or synth_event.voice.name

        if requested:
            preset = self._voices.get(requested.lower())
            if preset is None:
                _LOGGER.warning("Requested speaker '%s' not found; falling back to default", requested)

        if preset is None:
            preset = self._fallback_voice

        prompt_wav = preset.prompt_wav if preset != self._fallback_voice else self._fallback_voice.prompt_wav
        prompt_text = preset.prompt_text if preset != self._fallback_voice else self._fallback_voice.prompt_text

        if requested:
            _LOGGER.info("Synthesis request for speaker '%s'", preset.speaker)
        else:
            _LOGGER.info("Synthesis request using default speaker '%s'", preset.speaker)

        if sf is not None:
            try:
                info = sf.info(str(prompt_wav))
                _LOGGER.debug(
                    "Prompt audio '%s': %s ch @ %s Hz", prompt_wav.name, info.channels, info.samplerate
                )
            except Exception:  # pragma: no cover - best effort logging
                pass

        _LOGGER.info("Synthesize text: %s", text)

        try:
            pcm, audio_seconds, wall = await self._synthesizer.synthesize(
                text=text,
                prompt_wav=prompt_wav,
                prompt_text=prompt_text,
            )
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Synthesis failed")
            await self.write_event(Error(text="Synthesis failed", code="synthesis_error").event())
            return

        await self.write_event(
            AudioStart(rate=PCM_SAMPLE_RATE, width=PCM_WIDTH, channels=PCM_CHANNELS).event()
        )

        for chunk in chunk_audio(pcm):
            await self.write_event(
                AudioChunk(
                    rate=PCM_SAMPLE_RATE,
                    width=PCM_WIDTH,
                    channels=PCM_CHANNELS,
                    audio=chunk,
                ).event()
            )

        await self.write_event(AudioStop().event())

        rtf = wall / audio_seconds if audio_seconds else float("inf")
        _LOGGER.info(
            "Synthesized %.2fs audio in %.0f ms (RTF=%.2f)",
            audio_seconds,
            wall * 1000.0,
            rtf,
        )


def chunk_audio(audio: bytes, *, chunk_size: int = 32_000) -> Iterable[bytes]:
    for index in range(0, len(audio), chunk_size):
        yield audio[index : index + chunk_size]


def load_voice_presets(directory: Optional[Path]) -> Dict[str, VoicePreset]:
    presets: Dict[str, VoicePreset] = {}
    if directory is None:
        return presets

    if not directory.exists():
        _LOGGER.warning("Voices directory '%s' does not exist", directory)
        return presets

    for wav_path in sorted(directory.glob("*.wav")):
        speaker = wav_path.stem
        text_path = wav_path.with_suffix(".txt")

        prompt_text: Optional[str] = None
        if text_path.exists():
            prompt_text = text_path.read_text(encoding="utf-8").strip() or None
        else:
            _LOGGER.warning(
                "Speaker '%s': missing %s; proceeding with audio-only cloning",
                speaker,
                text_path.name,
            )

        if sf is not None:
            try:
                info = sf.info(str(wav_path))
                _LOGGER.debug(
                    "Voice preset '%s': %s ch @ %s Hz", speaker, info.channels, info.samplerate
                )
                if info.channels != PCM_CHANNELS or info.samplerate != PCM_SAMPLE_RATE:
                    _LOGGER.warning(
                        "Voice preset '%s' is %s ch @ %s Hz; will convert at runtime",
                        speaker,
                        info.channels,
                        info.samplerate,
                    )
            except Exception:  # pragma: no cover - optional logging
                _LOGGER.warning("Unable to inspect audio for speaker '%s'", speaker, exc_info=True)

        presets[speaker.lower()] = VoicePreset(
            speaker=speaker,
            prompt_wav=wav_path,
            prompt_text=prompt_text,
        )

    return presets


def get_package_version(package: str) -> Optional[str]:
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:  # pragma: no cover - depends on env
        return None


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a Wyoming TTS server backed by the local tts_pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--uri", default="tcp://0.0.0.0:10200", help="Server URI")
    parser.add_argument("--log-level", default="INFO", help="Logging verbosity")
    parser.add_argument(
        "--use-uvloop",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Install uvloop if available",
    )
    parser.add_argument(
        "--max-text-length",
        type=positive_int,
        default=DEFAULT_MAX_TEXT_LENGTH,
        help="Maximum number of characters per request",
    )
    parser.add_argument("--voices-dir", type=Path, help="Directory containing <speaker>.wav/.txt pairs")
    parser.add_argument(
        "--default-speaker-name",
        default="default",
        help="Display name for the fallback speaker",
    )
    parser.add_argument(
        "--default-prompt-audio",
        type=Path,
        help="Reference audio used when no speaker is requested",
    )
    parser.add_argument(
        "--default-prompt-text",
        help="Prompt text used with the fallback speaker (string)",
    )
    parser.add_argument(
        "--default-prompt-text-file",
        type=Path,
        help="Path to a file containing prompt text for the fallback speaker",
    )
    parser.add_argument(
        "--cfg-value",
        type=float,
        default=1.8,
        help="Classifier-free guidance scale",
    )
    parser.add_argument(
        "--inference-timesteps",
        type=positive_int,
        default=14,
        help="Number of diffusion steps",
    )
    parser.add_argument(
        "--denoise",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable denoising of prompt audio",
    )
    parser.add_argument(
        "--normalize",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Normalize/clean the input text within the VoxCPM CLI",
    )

    parser.add_argument(
        "--frontend",
        choices=("ko", "none"),
        default="ko",
        help="Text frontend to pre-process incoming text",
    )
    parser.add_argument(
        "--ffmpeg-bin",
        default="ffmpeg",
        help="ffmpeg executable to use for conversions",
    )

    return parser


async def run_server(args: argparse.Namespace) -> None:
    setup_logging(args.log_level)

    if args.use_uvloop:
        try:
            import uvloop  # noqa: WPS433 (runtime import)

            uvloop.install()
            _LOGGER.debug("uvloop installed")
        except ImportError:  # pragma: no cover - optional dependency
            _LOGGER.debug("uvloop not available; using default event loop")

    default_prompt_text = args.default_prompt_text
    if args.default_prompt_text_file:
        default_prompt_text = args.default_prompt_text_file.read_text(encoding="utf-8").strip() or None
    elif default_prompt_text is not None:
        default_prompt_text = default_prompt_text.strip() or None

    voices = load_voice_presets(args.voices_dir)

    default_voice: Optional[VoicePreset] = None
    if args.default_prompt_audio:
        if not args.default_prompt_audio.exists():
            raise FileNotFoundError(f"Fallback prompt audio not found: {args.default_prompt_audio}")
        default_voice = VoicePreset(
            speaker=args.default_speaker_name,
            prompt_wav=args.default_prompt_audio,
            prompt_text=default_prompt_text,
        )
        voices[args.default_speaker_name.lower()] = default_voice
    elif voices:
        default_voice = next(iter(voices.values()))
    else:
        raise RuntimeError("At least one voice (default or from --voices-dir) must be provided")

    if default_voice.prompt_text is None:
        _LOGGER.warning("Fallback speaker '%s' has no prompt text; proceeding with audio-only cloning", default_voice.speaker)

    fallback_prompt_text_source: Optional[Path]
    if args.default_prompt_text_file:
        fallback_prompt_text_source = args.default_prompt_text_file
    elif args.default_prompt_audio is None:
        candidate = default_voice.prompt_wav.with_suffix(".txt")
        fallback_prompt_text_source = candidate if candidate.exists() else None
    else:
        fallback_prompt_text_source = args.default_prompt_text_file


    frontend: Optional[Callable[[str], str]]
    if args.frontend == "ko":
        frontend = ko_text_frontend
    else:
        frontend = None

    synthesizer = PipelineSynthesizer(
        cfg_value=args.cfg_value,
        inference_steps=args.inference_timesteps,
        use_denoise=args.denoise,
        use_normalize=args.normalize,
        fallback_voice=default_voice,
        frontend=frontend,
        ffmpeg_bin=args.ffmpeg_bin,
    )

    attribution = Attribution(name="tts_pipeline", url="https://github.com/OpenBMB/VoxCPM")
    package_version = get_package_version("voxcpm")

    server = AsyncServer.from_uri(args.uri)

    handler_factory = partial(
        PipelineEventHandler,
        synthesizer=synthesizer,
        voices=voices,
        fallback_voice=default_voice,
        voices_dir=args.voices_dir,
        fallback_prompt_text_source=fallback_prompt_text_source,
        model_name="tts_pipeline-VoxCPM",
        attribution=attribution,
        package_version=package_version,
        max_text_length=args.max_text_length,
        languages=("ko", "en"),
    )

    _LOGGER.info(
        "Starting Wyoming TTS server on %s (cfg=%.2f, steps=%d, denoise=%s, normalize=%s)",
        args.uri,
        args.cfg_value,
        args.inference_timesteps,
        args.denoise,
        args.normalize,
    )

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def _signal_handler(*_: int) -> None:
        stop_event.set()

    for signame in ("SIGINT", "SIGTERM"):
        if hasattr(signal, signame):
            try:
                loop.add_signal_handler(getattr(signal, signame), _signal_handler)
            except NotImplementedError:  # pragma: no cover - Windows fallback
                signal.signal(getattr(signal, signame), lambda *_: stop_event.set())

    server_task = asyncio.create_task(server.start(handler_factory))
    await stop_event.wait()
    await server.stop()
    await server_task

    _LOGGER.info("Server stopped")


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def main() -> None:
    parser = create_arg_parser()
    args = parser.parse_args()

    try:
        asyncio.run(run_server(args))
    except KeyboardInterrupt:  # pragma: no cover - graceful shutdown
        pass
    except Exception:  # pylint: disable=broad-except
        _LOGGER.exception("Fatal error: server crashed")
        sys.exit(1)


if __name__ == "__main__":
    main()
