#!/usr/bin/env bash
set -euo pipefail

# ---------------- args ----------------
STAY=1
SERVER=1        # 기본: 서버 실행
SERVICES=1      # 기본: 서버 + pull_saver (+선택 ngrok)
PULL=0
PULL_PORT=20001
NGROK=0
STOP_ONLY=0
LOGS=0
SERVER_URI="tcp://0.0.0.0:20000"
SERVER_LOG_LEVEL="INFO"
SERVER_VOICES_DIR=""
SERVER_DEFAULT_SPEAKER="korean_male"
SERVER_FRONTEND="ko"
SERVER_DEFAULT_PROMPT_AUDIO=""
SERVER_DEFAULT_PROMPT_TEXT_FILE=""
for arg in "$@"; do
  case "$arg" in
    --no-stay) STAY=0 ;;
    --server) SERVER=1 ;;
    --server-only) SERVER=1; SERVICES=0; PULL=0 ;;
    --services|--all) SERVICES=1; SERVER=1; PULL=1; NGROK=1 ;;
    --server-uri=*) SERVER=1; SERVER_URI="${arg#*=}" ;;
    --server-log-level=*) SERVER=1; SERVER_LOG_LEVEL="${arg#*=}" ;;
    --server-voices-dir=*) SERVER=1; SERVER_VOICES_DIR="${arg#*=}" ;;
    --server-default-speaker=*) SERVER=1; SERVER_DEFAULT_SPEAKER="${arg#*=}" ;;
    --server-default-prompt-audio=*) SERVER=1; SERVER_DEFAULT_PROMPT_AUDIO="${arg#*=}" ;;
    --server-default-prompt-text-file=*) SERVER=1; SERVER_DEFAULT_PROMPT_TEXT_FILE="${arg#*=}" ;;
    --server-frontend=*) SERVER=1; SERVER_FRONTEND="${arg#*=}" ;;
    --pull) PULL=1; SERVICES=0 ;;
    --pull-only) SERVER=0; SERVICES=0; PULL=1 ;;
    --pull-port=*) PULL=1; PULL_PORT="${arg#*=}" ;;
    --ngrok) NGROK=1 ;;
    --logs) LOGS=1 ;;
    --stop) STOP_ONLY=1; SERVER=0; SERVICES=0; PULL=0; NGROK=0; STAY=0 ;;
    *) echo "Unknown option: $arg"; exit 2 ;;
  esac
done

# ---------------- utils ----------------
have() { command -v "$1" >/dev/null 2>&1; }

msg() { printf "\033[1;32m%s\033[0m\n" "$*"; }
warn() { printf "\033[1;33m%s\033[0m\n" "$*"; }
err() { printf "\033[1;31m%s\033[0m\n" "$*"; }

# ------------- process helpers -------------
is_pid_alive() { kill -0 "$1" 2>/dev/null; }

stop_pid_file() {
  local pidfile="$1"; local label="${2:-process}"
  if [ -f "$pidfile" ]; then
    local pid
    pid="$(cat "$pidfile" 2>/dev/null || true)"
    if [ -n "$pid" ] && is_pid_alive "$pid"; then
      msg "${label} 중지 중… (PID=${pid})"
      kill "$pid" 2>/dev/null || true
      for _ in $(seq 1 25); do
        is_pid_alive "$pid" || break
        sleep 0.2
      done
      if is_pid_alive "$pid"; then
        warn "${label} 강제 종료(SIGKILL)… (PID=${pid})"
        kill -9 "$pid" 2>/dev/null || true
      fi
    fi
    rm -f "$pidfile"
  fi
}

is_port_in_use() {
  local port="$1"
  if have ss; then
    ss -lnt | awk '{print $4}' | grep -E "(^|[:.])${port}$" -q
  elif have lsof; then
    lsof -iTCP:"$port" -sTCP:LISTEN -t >/dev/null 2>&1
  elif have netstat; then
    netstat -lnt | awk '{print $4}' | grep -E "(^|[:.])${port}$" -q
  elif have fuser; then
    fuser -n tcp "$port" >/dev/null 2>&1
  else
    return 1
  fi
}

stop_services() {
  stop_pid_file .pull_saver.pid pull_saver
  stop_pid_file .tts_server.pid wyoming_server
  stop_pid_file .ngrok.pid ngrok
}

# ---------------- cd to repo root ----------------
cd "$(dirname "$0")/.." || exit 1
REPO_ROOT="$(pwd -P)"

if [ "$STOP_ONLY" -eq 1 ]; then
  stop_services
  msg "모든 백그라운드 서비스 중지 완료"
  exit 0
fi

# ---------------- Python 3.11 / venv ----------------
PYBIN="python3.11"
if ! have "$PYBIN"; then
  if have python3; then
    warn "python3.11 미발견 → python3로 대체합니다."
    PYBIN="python3"
  elif have python; then
    warn "python3 미발견 → python로 대체합니다."
    PYBIN="python"
  else
    err "Python이 없습니다. macOS: 'brew install python@3.11', Ubuntu: 'sudo apt-get install python3.11' 등으로 설치 후 재시도하세요."
    exit 1
  fi
fi

if [ ! -d ".venv" ]; then
  msg "venv 생성(.venv)…"
  "$PYBIN" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
msg "venv 활성화: $(python -V)"

# ---------------- pip / deps (재사용 최적화) ----------------
# 캐시 디렉터리를 리포 내부로 고정하여 컨테이너 재시작/재배포 시에도 볼륨만 유지하면 재사용 가능
mkdir -p .cache/pip .cache/huggingface
export PIP_CACHE_DIR="${PIP_CACHE_DIR:-$PWD/.cache/pip}"
export HF_HOME="${HF_HOME:-$PWD/.cache/huggingface}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$PWD/.cache}"

python -m pip install --upgrade pip setuptools wheel

# requirements 해시가 동일하면 설치 생략
REQ_FILE="requirements.txt"
if [ -f requirements.lock.txt ]; then
  REQ_FILE="requirements.lock.txt"
fi

calc_hash() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    # Python 백업
    python - "$1" <<'PY'
import hashlib, sys
p=sys.argv[1]
with open(p,'rb') as f:
    h=hashlib.sha256(f.read()).hexdigest()
print(h)
PY
  fi
}

REQ_HASH_NOW="$(calc_hash "$REQ_FILE")"
REQ_HASH_FILE=".venv/.requirements.hash"

if [ -f "$REQ_HASH_FILE" ] && [ "$(cat "$REQ_HASH_FILE" 2>/dev/null || true)" = "$REQ_HASH_NOW" ]; then
  msg "요구사항 변경 없음 → 의존성 설치 생략"
else
  msg "의존성 설치… ($REQ_FILE)"
  pip install -r "$REQ_FILE"
  echo "$REQ_HASH_NOW" > "$REQ_HASH_FILE"
fi

# ---------------- FFmpeg ----------------
ensure_ffmpeg() {
  if have ffmpeg; then
    ffmpeg -version | head -n1
    return 0
  fi
  warn "FFmpeg 미발견 → 설치 시도"

  OS="$(uname -s)"
  case "$OS" in
    Darwin)
      if have brew; then
        brew install ffmpeg || { err "brew 설치 실패"; exit 1; }
      else
        err "Homebrew가 없습니다. 설치 후 'brew install ffmpeg' 실행하세요: https://brew.sh/"
        exit 1
      fi
      ;;
    Linux)
      if have apt-get; then
        sudo apt-get update -y && sudo apt-get install -y ffmpeg
      elif have dnf; then
        sudo dnf install -y ffmpeg
      elif have pacman; then
        sudo pacman -Sy --noconfirm ffmpeg
      elif have zypper; then
        sudo zypper install -y ffmpeg
      else
        err "지원 패키지 관리자를 찾지 못했습니다. 배포판에 맞는 방법으로 ffmpeg를 설치하세요."
        exit 1
      fi
      ;;
    *)
      err "미지원 OS: $OS. 수동으로 ffmpeg 설치 후 재시도하세요."
      exit 1
      ;;
  esac

  if ! have ffmpeg; then
    err "ffmpeg 설치가 완료되지 않았습니다."
    exit 1
  fi
}

ensure_ffmpeg

# ---------------- HuggingFace symlink 이슈 회피(무해) ----------------
export HF_HUB_DISABLE_SYMLINKS=1

# ---------------- run ----------------
# 오프라인 합성(run.py) 경로 제거됨 — 서버/풀세이버만 지원

run_server() {
  local uri="$1"
  local log_level="$2"
  local voices_dir="$3"
  local default_speaker="$4"
  local default_prompt_audio="$5"
  local default_prompt_text_file="$6"

  msg "Wyoming TTS 서버 실행… (URI: ${uri})"

  SERVER_URI_VALUE="$uri" \
  SERVER_LOG_LEVEL_VALUE="$log_level" \
  SERVER_VOICES_DIR_VALUE="$voices_dir" \
  SERVER_DEFAULT_SPEAKER_VALUE="$default_speaker" \
  SERVER_DEFAULT_PROMPT_AUDIO_VALUE="$default_prompt_audio" \
  SERVER_DEFAULT_PROMPT_TEXT_FILE_VALUE="$default_prompt_text_file" \
  SERVER_FRONTEND_VALUE="$SERVER_FRONTEND" \
    python - <<'PY'
import asyncio
import os
import sys

from tts_pipeline import config as C
from tts_pipeline import server as srv

uri = os.environ.get("SERVER_URI_VALUE", "tcp://0.0.0.0:20000")
log_level = os.environ.get("SERVER_LOG_LEVEL_VALUE", "INFO")
voices_dir_env = os.environ.get("SERVER_VOICES_DIR_VALUE") or None
default_speaker_env = os.environ.get("SERVER_DEFAULT_SPEAKER_VALUE") or "korean_male"
default_prompt_audio_env = os.environ.get("SERVER_DEFAULT_PROMPT_AUDIO_VALUE")
default_prompt_text_file_env = os.environ.get("SERVER_DEFAULT_PROMPT_TEXT_FILE_VALUE")

  # 참고: 기본 프롬프트 오디오(C.REF_AUDIO)가 없더라도, 아래에서
  # --default-prompt-audio 또는 --voices-dir로 대체 가능하므로
  # 존재 여부를 강제하지 않습니다.

argv = [
    "--uri",
    uri,
    "--log-level",
    log_level,
    "--default-speaker-name",
    default_speaker_env,
    "--frontend",
    os.environ.get("SERVER_FRONTEND_VALUE", "ko"),
    "--cfg-value",
    str(C.CFG_VALUE),
    "--inference-timesteps",
    str(C.STEPS),
]

# Default prompt audio/text-file selection (존재할 때만 전달)
prompt_audio = (default_prompt_audio_env or str(C.REF_AUDIO)).strip()
if prompt_audio:
    pa = os.path.expanduser(prompt_audio)
    if os.path.exists(pa):
        argv.extend(["--default-prompt-audio", pa])
default_prompt_text_file_path = None
if default_prompt_text_file_env:
    tf = os.path.expanduser(default_prompt_text_file_env)
    if os.path.exists(tf):
        default_prompt_text_file_path = tf
if default_prompt_text_file_path:
    argv.extend(["--default-prompt-text-file", default_prompt_text_file_path])

if C.USE_DENOISE:
    argv.append("--denoise")
else:
    argv.append("--no-denoise")

if C.USE_NORMALIZE:
    argv.append("--normalize")
else:
    argv.append("--no-normalize")

post_chain = getattr(C, "POST_CHAIN", None)
if post_chain:
    argv.extend(["--postprocess-chain", post_chain])

prompt_text = (C.PROMPT_TEXT or "").strip()
# Only pass inline prompt text if text-file isn't provided
if (not default_prompt_text_file_env) and prompt_text:
    argv.extend(["--default-prompt-text", prompt_text])

if voices_dir_env:
    argv.extend(["--voices-dir", os.path.expanduser(voices_dir_env)])

parser = srv.create_arg_parser()
args = parser.parse_args(argv)

try:
    asyncio.run(srv.run_server(args))
except KeyboardInterrupt:
    pass
except Exception as exc:  # pragma: no cover - bootstrap guard
    print(f"[bootstrap] Wyoming server crashed: {exc}", file=sys.stderr)
    raise
PY
}

run_server_bg() {
  local uri="$1"
  local log_level="$2"
  local voices_dir="$3"
  local default_speaker="$4"
  local default_prompt_audio="$5"
  local default_prompt_text_file="$6"

  # stop existing background server if tracked
  stop_pid_file .tts_server.pid wyoming_server

  msg "Wyoming TTS 서버(백그라운드) 실행… (URI: ${uri})"

  SERVER_URI_VALUE="$uri" \
  SERVER_LOG_LEVEL_VALUE="$log_level" \
  SERVER_VOICES_DIR_VALUE="$voices_dir" \
  SERVER_DEFAULT_SPEAKER_VALUE="$default_speaker" \
  SERVER_DEFAULT_PROMPT_AUDIO_VALUE="$default_prompt_audio" \
  SERVER_DEFAULT_PROMPT_TEXT_FILE_VALUE="$default_prompt_text_file" \
  SERVER_FRONTEND_VALUE="$SERVER_FRONTEND" \
    python - <<'PY' >> .wyoming_server.log 2>&1 &
import asyncio
import os
import sys

from tts_pipeline import config as C
from tts_pipeline import server as srv

uri = os.environ.get("SERVER_URI_VALUE", "tcp://0.0.0.0:20000")
log_level = os.environ.get("SERVER_LOG_LEVEL_VALUE", "INFO")
voices_dir_env = os.environ.get("SERVER_VOICES_DIR_VALUE") or None
default_speaker_env = os.environ.get("SERVER_DEFAULT_SPEAKER_VALUE") or "korean_male"
default_prompt_audio_env = os.environ.get("SERVER_DEFAULT_PROMPT_AUDIO_VALUE")
default_prompt_text_file_env = os.environ.get("SERVER_DEFAULT_PROMPT_TEXT_FILE_VALUE")

# 기본 프롬프트 오디오 존재 강제하지 않음 (상동)

argv = [
    "--uri",
    uri,
    "--log-level",
    log_level,
    "--default-speaker-name",
    default_speaker_env,
    "--cfg-value",
    str(C.CFG_VALUE),
    "--inference-timesteps",
    str(C.STEPS),
]

prompt_audio = (default_prompt_audio_env or str(C.REF_AUDIO)).strip()
if prompt_audio:
    pa = os.path.expanduser(prompt_audio)
    if os.path.exists(pa):
        argv.extend(["--default-prompt-audio", pa])
default_prompt_text_file_path = None
if default_prompt_text_file_env:
    tf = os.path.expanduser(default_prompt_text_file_env)
    if os.path.exists(tf):
        default_prompt_text_file_path = tf
if default_prompt_text_file_path:
    argv.extend(["--default-prompt-text-file", default_prompt_text_file_path])

if C.USE_DENOISE:
    argv.append("--denoise")
else:
    argv.append("--no-denoise")

if C.USE_NORMALIZE:
    argv.append("--normalize")
else:
    argv.append("--no-normalize")

post_chain = getattr(C, "POST_CHAIN", None)
if post_chain:
    argv.extend(["--postprocess-chain", post_chain])

prompt_text = (C.PROMPT_TEXT or "").strip()
if (not default_prompt_text_file_env) and prompt_text:
    argv.extend(["--default-prompt-text", prompt_text])

if voices_dir_env:
    argv.extend(["--voices-dir", os.path.expanduser(voices_dir_env)])

parser = srv.create_arg_parser()
args = parser.parse_args(argv)

try:
    asyncio.run(srv.run_server(args))
except KeyboardInterrupt:
    pass
except Exception as exc:  # pragma: no cover - bootstrap guard
    print(f"[bootstrap] Wyoming server crashed: {exc}", file=sys.stderr)
    raise
PY
  echo $! > .tts_server.pid
  msg "[Wyoming] PID=$(cat .tts_server.pid) (log: $REPO_ROOT/.wyoming_server.log)"
}

run_pull_saver() {
  local port="$1"
  # stop existing tracked pull_saver
  stop_pid_file .pull_saver.pid pull_saver

  # proactively free same port if still bound by a previous process
  if is_port_in_use "$port"; then
    warn "포트 ${port}가 사용 중입니다. 기존 프로세스 종료를 시도합니다."
    if have fuser; then fuser -k -n tcp "$port" >/dev/null 2>&1 || true; fi
    sleep 0.5
  fi
  if is_port_in_use "$port"; then
    err "포트 ${port}가 여전히 사용 중입니다. '--pull-port='로 다른 포트를 지정하거나 '--stop' 후 재시도하세요."
    return 1
  fi

  msg "pull_saver 실행… (http://0.0.0.0:${port}/pull)"
  # 로그 리다이렉션
  : > .pull_saver.log
  FLASK_APP="tts_pipeline.pull_saver" \
    python -m flask run --host 0.0.0.0 --port "$port" >> .pull_saver.log 2>&1 &
  echo $! > .pull_saver.pid
  msg "[pull_saver] PID=$(cat .pull_saver.pid) (log: $REPO_ROOT/.pull_saver.log)"
}

run_ngrok() {
  local port="$1"
  if have ngrok; then
    msg "ngrok 실행… (http ${port})"
    : > .ngrok.log
    ngrok http "$port" >> .ngrok.log 2>&1 &
    echo $! > .ngrok.pid
    msg "[ngrok] PID=$(cat .ngrok.pid) (log: $REPO_ROOT/.ngrok.log)"
  else
    warn "ngrok 미설치 — 생략합니다. (설치 후 'ngrok http ${port}')"
  fi
}

if [ "$SERVER" -eq 1 ] && [ "$SERVICES" -eq 0 ]; then
  run_server "$SERVER_URI" "$SERVER_LOG_LEVEL" "${SERVER_VOICES_DIR:-./voices}" "$SERVER_DEFAULT_SPEAKER" "$SERVER_DEFAULT_PROMPT_AUDIO" "$SERVER_DEFAULT_PROMPT_TEXT_FILE"
fi

if [ "$PULL" -eq 1 ] && [ "$SERVICES" -eq 0 ]; then
  run_pull_saver "$PULL_PORT"
fi

if [ "$SERVICES" -eq 1 ]; then
  # Stop stale processes first to avoid 'Address already in use'
  stop_services
  # Run both server and pull_saver; ngrok optional
  run_server_bg "$SERVER_URI" "$SERVER_LOG_LEVEL" "${SERVER_VOICES_DIR:-./voices}" "$SERVER_DEFAULT_SPEAKER" "${SERVER_DEFAULT_PROMPT_AUDIO:-./voices/${SERVER_DEFAULT_SPEAKER}/ref039.wav}" "${SERVER_DEFAULT_PROMPT_TEXT_FILE:-./voices/${SERVER_DEFAULT_SPEAKER}/ref039.txt}"
  run_pull_saver "$PULL_PORT"
  if [ "$NGROK" -eq 1 ]; then
    run_ngrok "$PULL_PORT"
  fi
fi

# ---------------- stay (venv shell keep-open) ----------------
if [ "$LOGS" -eq 1 ]; then
  # 실시간 로그 보기 (tail -F)
  touch .wyoming_server.log .pull_saver.log
  msg "로그 팔로우 시작 (.wyoming_server.log, .pull_saver.log) — 중지: Ctrl+C"
  exec tail -n +1 -F .wyoming_server.log .pull_saver.log
fi

if [ "$STAY" -eq 1 ]; then
  msg "venv 유지용 인터랙티브 셸을 엽니다. 종료: exit"
  TARGET_SHELL="${SHELL:-/bin/bash}"
  # REPO_ROOT 절대경로 기준으로 venv 활성화 (vast.ai auto-tmux로 cwd가 바뀌어도 안전)
  exec "$TARGET_SHELL" -i -c "cd '$REPO_ROOT'; source '$REPO_ROOT/.venv/bin/activate' 2>/dev/null || true; echo '[venv] ready'; exec '$TARGET_SHELL' -i"
fi

msg "bootstrap 완료"
