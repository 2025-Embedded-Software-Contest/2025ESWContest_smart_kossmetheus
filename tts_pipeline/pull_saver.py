# pull_saver.py
from flask import Flask, request, jsonify
from pathlib import Path
from datetime import datetime
import requests
import re
import os
import logging
import tempfile

from pydub import AudioSegment  # ffmpeg 필요

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# --- 저장 경로 설정 ---
DEFAULT_SAVE_DIR = (Path(__file__).resolve().parent.parent / "voices" / "korean_male")
SAVE_DIR = Path(os.getenv("VOX_SAVE_DIR", str(DEFAULT_SAVE_DIR))).resolve()
SAVE_DIR.mkdir(parents=True, exist_ok=True)

app.logger.info(f"cwd={Path.cwd()}")
app.logger.info(f"__file__={Path(__file__).resolve()}")
app.logger.info(f"SAVE_DIR={SAVE_DIR}")

# --- 유틸 ---
_FORBIDDEN = r'[<>:"/\\|?*\x00-\x1F]'

def safe_filename(name: str) -> str:
    name = Path(name).name
    name = re.sub(_FORBIDDEN, "-", name)
    name = re.sub(r"\s+", " ", name).strip()
    name = re.sub(r"-{2,}", "-", name)
    return name or "file"

def infer_ext_from_content_type(ct: str | None) -> str:
    if not ct:
        return ".bin"
    ct = ct.lower().split(";")[0].strip()
    mapping = {
        "audio/mpeg": ".mp3",
        "audio/mp3": ".mp3",
        "audio/wav": ".wav",
        "audio/x-wav": ".wav",
        "audio/ogg": ".ogg",
        "audio/flac": ".flac",
        "audio/x-flac": ".flac",
        "application/octet-stream": ".bin",
    }
    return mapping.get(ct, ".bin")

def convert_to_wav(src_path: Path, dst_path: Path,
                   target_rate: int = 16_000,
                   target_channels: int = 1,
                   sample_width_bytes: int = 2) -> None:
    audio = AudioSegment.from_file(src_path)
    if audio.frame_rate != target_rate:
        audio = audio.set_frame_rate(target_rate)
    if audio.channels != target_channels:
        audio = audio.set_channels(target_channels)
    if audio.sample_width != sample_width_bytes:
        audio = audio.set_sample_width(sample_width_bytes)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    audio.export(dst_path, format="wav")

@app.post("/pull")
def pull():
    tmp_file_path = None
    try:
        data = request.get_json(force=True) or {}
        url = data.get("url")
        if not url:
            return jsonify({"ok": False, "error": "Missing 'url'"}), 400

        # ✅ 항상 ref039.wav로 저장 (덮어쓰기)
        final_filename = "ref039.wav"
        out_path = SAVE_DIR / final_filename
        if out_path.exists():
            try:
                out_path.unlink()
            except Exception as e:
                return jsonify({"ok": False, "error": f"Cannot overwrite existing file: {e}"}), 500

        # 원본을 임시 파일에 스트리밍 저장
        with requests.get(url, timeout=30, stream=True) as r:
            r.raise_for_status()
            src_ext = infer_ext_from_content_type(r.headers.get("Content-Type"))
            with tempfile.NamedTemporaryFile(delete=False, suffix=src_ext) as tmpf:
                tmp_file_path = Path(tmpf.name)
                for chunk in r.iter_content(chunk_size=1024 * 64):
                    if chunk:
                        tmpf.write(chunk)

        # 임시 파일 → WAV 변환 저장
        convert_to_wav(tmp_file_path, out_path)
        app.logger.info(f"Saved WAV to: {out_path}  ({out_path.stat().st_size} bytes)")
        return jsonify({"ok": True, "saved": str(out_path)})

    except requests.exceptions.RequestException as e:
        return jsonify({"ok": False, "error": f"Request failed: {e}"}), 502
    except FileNotFoundError as e:
        return jsonify({"ok": False, "error": f"ffmpeg not found or file path issue: {e}"}), 500
    except Exception as e:
        try:
            if 'out_path' in locals() and out_path.exists():
                out_path.unlink(missing_ok=True)
        except Exception:
            pass
        return jsonify({"ok": False, "error": f"Unexpected error: {e}"}), 500
    finally:
        try:
            if tmp_file_path and Path(tmp_file_path).exists():
                Path(tmp_file_path).unlink(missing_ok=True)
        except Exception:
            pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055)
