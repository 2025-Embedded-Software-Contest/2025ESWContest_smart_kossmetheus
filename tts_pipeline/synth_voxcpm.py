import os
import shlex
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Optional, Sequence

import soundfile as sf

from voxcpm.core import VoxCPM

DEFAULT_HF_ID = "openbmb/VoxCPM-0.5B"
DEFAULT_ZIPENHANCER_ID = "iic/speech_zipenhancer_ans_multiloss_16k_base"

def _format_cmd(parts: Sequence[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in parts)


def run(cmd: Sequence[str]) -> None:
    pretty = _format_cmd(cmd)
    print("[RUN]", pretty)
    subprocess.run(cmd, check=True)


def _env_flag(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _expand_path(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return str(Path(value).expanduser())


@lru_cache(maxsize=None)
def _load_voxcpm(
    *,
    enable_denoiser: bool,
    model_path: Optional[str],
    hf_model_id: str,
    cache_dir: Optional[str],
    local_files_only: bool,
    zipenhancer_model_path: Optional[str],
) -> VoxCPM:
    resolved_model_path = _expand_path(model_path)
    resolved_cache_dir = _expand_path(cache_dir)
    resolved_zipenhancer = _expand_path(zipenhancer_model_path) or DEFAULT_ZIPENHANCER_ID

    if resolved_model_path:
        print(f"Loading VoxCPM model from local path: {resolved_model_path}")
        return VoxCPM(
            voxcpm_model_path=resolved_model_path,
            zipenhancer_model_path=resolved_zipenhancer if enable_denoiser else None,
            enable_denoiser=enable_denoiser,
        )

    print(f"Loading VoxCPM model from pretrained repo: {hf_model_id}")
    return VoxCPM.from_pretrained(
        hf_model_id=hf_model_id,
        load_denoiser=enable_denoiser,
        zipenhancer_model_id=resolved_zipenhancer,
        cache_dir=resolved_cache_dir,
        local_files_only=local_files_only,
    )


def ensure_format(ref: Path) -> None:
    # Ensure VoxCPM prompt audio stays 16 kHz mono s16.
    tmp_wav = ref.with_name(f"{ref.name}.tmp.wav")
    run([
        "ffmpeg",
        "-y",
        "-i",
        str(ref),
        "-ac",
        "1",
        "-ar",
        "16000",
        "-sample_fmt",
        "s16",
        str(tmp_wav),
    ])
    os.replace(tmp_wav, ref)


def synth(
    text_for_tts: str,
    prompt_text: str,
    ref_audio: Path,
    raw_out: Path,
    cfg: float,
    steps: int,
    use_denoise: bool,
    use_normalize: bool,
) -> None:
    ensure_format(ref_audio)

    model = _load_voxcpm(
        enable_denoiser=use_denoise,
        model_path=os.getenv("VOXCPM_MODEL_PATH"),
        hf_model_id=os.getenv("VOXCPM_HF_ID", DEFAULT_HF_ID),
        cache_dir=os.getenv("VOXCPM_CACHE_DIR"),
        local_files_only=_env_flag("VOXCPM_LOCAL_ONLY", False),
        zipenhancer_model_path=os.getenv("ZIPENHANCER_MODEL_PATH"),
    )

    raw_out.parent.mkdir(parents=True, exist_ok=True)

    waveform = model.generate(
        text=text_for_tts,
        prompt_wav_path=str(ref_audio),
        prompt_text=prompt_text,
        cfg_value=cfg,
        inference_timesteps=steps,
        normalize=use_normalize,
        denoise=use_denoise,
    )

    if hasattr(waveform, "astype"):
        waveform = waveform.astype("float32")

    sf.write(str(raw_out), waveform, 16000)
