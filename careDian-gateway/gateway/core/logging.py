from __future__ import annotations # 타입 힌트 평가 X, 문자열로 저장
import json, os, sys # JSON, OS, SYSTEM 모듈
import logging # 진단 정보 기록(로그 기록)
from logging import Logger # 로거
from logging.handlers import RotatingFileHandler # 로그 파일 관리
from typing import Optional # 타입 힌트


class JsonFormatter(logging.Formatter):
    """최소 의존성 JSON 포매터"""
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        # 선택 필드 (있으면 담기)

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            payload.update(record.extra)

        return json.dumps(payload, ensure_ascii=False)


def _build_stream_handler(json_mode: bool) -> logging.Handler:
    handler = logging.StreamHandler(sys.stdout)

    if json_mode:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))

    return handler


def _build_file_handler(log_file: str, json_mode: bool, max_bytes: int = 5 * 1024 * 1024, backup_count: int = 3) -> logging.Handler:
    fh = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")

    if json_mode:
        fh.setFormatter(JsonFormatter())
    else:
        fh.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))

    return fh


def setup_logging(level: str = "INFO", *, json_mode: Optional[bool] = None, log_file: Optional[str] = None, quiet_uvicorn_access: bool = False,) -> None:
    """
    게이트웨이 공통 로깅 설정.
    - level: "DEBUG" | "INFO" | "WARNING" | "ERROR"
    - json_mode: True면 JSON 라인 로그, None이면 ENV(LOG_JSON) 따라감
    - log_file: 지정 시 콘솔 + 파일 동시 로깅(순환 로그)
    - quiet_uvicorn_access: True면 uvicorn.access 로그 레벨 WARNING으로 낮춤
    """

    # ENV 우선 적용
    if json_mode is None:
        json_mode = os.getenv("LOG_JSON", "0") == "1"
    if log_file is None:
        log_file = os.getenv("LOG_FILE")

    root = logging.getLogger()
    # 중복 핸들러 방지
    for h in list(root.handlers):
        root.removeHandler(h)

    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.addHandler(_build_stream_handler(json_mode))

    if log_file:
        root.addHandler(_build_file_handler(log_file, json_mode))

    # 소음 줄이기/정렬
    for name, lvl in (
        ("uvicorn", level),
        ("uvicorn.error", level),
        ("uvicorn.access", "WARNING" if quiet_uvicorn_access else level),
        ("httpx", level),
        ("asyncio", level),
    ):
        logging.getLogger(name).setLevel(getattr(logging, lvl.upper(), logging.INFO))


def get_logger(name: str) -> Logger:
    return logging.getLogger(name)
