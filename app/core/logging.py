"""
모듈: core/logging.py (로깅 초기화 유틸리티)

목적:
  - 애플리케이션 전역 로거를 일관된 포맷으로 설정한다.
  - JSON 로그와 텍스트 로그를 선택적으로 지원한다.
  - 콘솔(Stream) + 파일(Rotating) 핸들러를 손쉽게 구성한다.
  - uvicorn/httpx/asyncio 등 외부 로거 레벨도 함께 조정한다.

핵심 기능 요약:
  * JsonFormatter: 로그 레코드를 JSON 객체로 직렬화
  * _build_stream_handler(): 표준출력 스트림 핸들러 생성
  * _build_file_handler(): rotating 파일 핸들러 생성(최대 5MB, 백업 3개)
  * setup_logging(): 루트 로거 초기화 및 하위 로거 레벨 설정 진입점

환경 변수:
  - LOG_JSON=1 이면 json_mode 기본값이 True (그 외 False)
  - LOG_FILE=/path/to/app.log 지정 시 파일 로깅 활성화

사용 예:
  from app.core.logging import setup_logging
  setup_logging(level="INFO", json_mode=None, log_file=None, quiet_uvicorn_access=True)
"""

from __future__ import annotations
import json, os, sys, logging
from logging.handlers import RotatingFileHandler


class JsonFormatter(logging.Formatter):
    """로그 레코드를 JSON 문자열로 변환하는 포매터.

    출력 필드:
      - ts: 타임스탬프(ISO-like)
      - level: 로그 레벨명
      - logger: 로거 이름
      - msg: 메시지(포맷 적용 후)
      - exc_info: 예외 스택(있을 때만)
      - extra: record.extra 딕셔너리가 있으면 해당 키/값을 병합
    """
    def format(self, record):
        payload = {
            "ts": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        # 예외 정보가 있으면 스택트레이스를 문자열로 추가
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        # logger.info("...", extra={"request_id": "..."}) 형태의 추가 필드 병합
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            payload.update(record.extra)
        return json.dumps(payload, ensure_ascii=False)


def _build_stream_handler(json_mode: bool) -> logging.Handler:
    """표준 출력으로 내보내는 스트림 핸들러 생성.

    - json_mode=True → JsonFormatter
    - json_mode=False → 일반 텍스트 포맷("YYYY-mm-dd HH:MM:SS LEVEL LOGGER MSG")
    """
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(
        JsonFormatter() if json_mode else logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s", "%Y-%m-%d %H:%M:%S"
        )
    )
    return h


def _build_file_handler(path: str, json_mode: bool) -> logging.Handler:
    """회전(rotating) 파일 핸들러 생성.

    - maxBytes=5MB, backupCount=3 → 파일이 5MB를 넘으면 자동으로 롤링, 최대 3개 백업 유지
    - UTF-8 인코딩으로 기록
    - 포맷터는 스트림 핸들러와 동일한 규칙 적용(JSON/텍스트)
    """
    fh = RotatingFileHandler(path, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
    fh.setFormatter(
        JsonFormatter() if json_mode else logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s", "%Y-%m-%d %H:%M:%S"
        )
    )
    return fh


def setup_logging(level: str = "INFO", json_mode: bool | None = None,
                  log_file: str | None = None, quiet_uvicorn_access: bool = False):
    """루트 로거 및 서브 로거 레벨을 초기화한다.

    Args:
      level: 루트 로거 레벨(예: "DEBUG"/"INFO"/"WARNING"/"ERROR")
      json_mode: True 이면 JSON 포맷, False 이면 텍스트 포맷.
                 None 이면 환경변수 LOG_JSON=="1" 일 때만 True
      log_file: 파일 로깅 경로(미지정 시 LOG_FILE 환경변수 참조). 없으면 콘솔만.
      quiet_uvicorn_access: True 이면 uvicorn.access 로거 레벨을 WARNING으로 올려 액세스 로그 소거

    동작:
      1) 기존 루트 핸들러 제거(중복 출력 방지)
      2) 루트 레벨 설정 및 콘솔 핸들러 추가
      3) log_file 지정 시 회전 파일 핸들러 추가(실패해도 콘솔만으로 계속)
      4) uvicorn / httpx / asyncio 등 서브 로거 레벨 일괄 조정
    """
    # json_mode 기본값: 환경 변수 LOG_JSON=1 일 때 True
    if json_mode is None:
        json_mode = os.getenv("LOG_JSON", "0") == "1"
    # log_file 기본값: 환경 변수 LOG_FILE 지정 시 사용
    if log_file is None:
        log_file = os.getenv("LOG_FILE")

    root = logging.getLogger()

    # (1) 기존 핸들러 제거 → 중복 로깅 방지
    for h in list(root.handlers):
        root.removeHandler(h)

    # (2) 루트 레벨/콘솔 핸들러 설정
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.addHandler(_build_stream_handler(json_mode))
    
    # (3) 파일 핸들러(옵션) 추가: 실패해도 서비스 중단 없이 경고만
    if log_file:
        try:
            root.addHandler(_build_file_handler(log_file, json_mode))
        except Exception:
            root.warning("file handler init failed, continue with console only")

    # (4) 서브 로거 레벨 조정
    #   - uvicorn: 서버 자체 로그
    #   - uvicorn.access: 액세스 로그(quiet 옵션에 따라 WARNING 으로 상향 가능)
    #   - httpx/asyncio: 필요 시 레벨 통일
    for name, lvl in (
        ("uvicorn", level),
        ("uvicorn.error", level),
        ("uvicorn.access", "WARNING" if quiet_uvicorn_access else level),
        ("httpx", level),
        ("asyncio", level),
    ):
        logging.getLogger(name).setLevel(getattr(logging, lvl.upper(), logging.INFO))
