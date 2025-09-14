from __future__ import annotations # 타입 힌트 평가 X, 문자열로 저장
import json, os, sys # JSON, OS, SYSTEM 모듈
import logging # 진단 정보 기록(로그 기록)
from logging import Logger # 로거
from logging.handlers import RotatingFileHandler # 순환 파일 로그 관리
from typing import Optional # 타입 힌트


# 로그를 JSON 형식으로 출력
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"), # 타임스탬프
            "level": record.levelname, # 로그 레벨
            "logger": record.name, # 로거 이름
            "msg": record.getMessage(), # 최종 메시지
        }

        # 예외 정보가 있으면 스택트레이스를 문자열로 추가
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        # 레코드에 extra 딕셔너리가 있으면 병합
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            payload.update(record.extra)

        return json.dumps(payload, ensure_ascii=False)

# 콘솔 핸들러 생성
def _build_stream_handler(json_mode: bool) -> logging.Handler:
    handler = logging.StreamHandler(sys.stdout)
    
    if json_mode: # JSON 모드
        handler.setFormatter(JsonFormatter())
    else: # 텍스트 모드
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))

    return handler

# 순환 파일 로그(5mb * 3개) 생성
def _build_file_handler(log_file: str, json_mode: bool, max_bytes: int = 5 * 1024 * 1024, backup_count: int = 3) -> logging.Handler:
    fh = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes, # 파일 최대 크기: 5MB
        backupCount=backup_count, # 백업 개수: 3개 
        encoding="utf-8" # 인코딩: UTF-8
    )

    if json_mode: # JSON 모드
        fh.setFormatter(JsonFormatter())
    else: # 텍스트 모드
        fh.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))

    return fh

# 기존 root 핸들러 제거
def setup_logging(
    level: str = "INFO", # 전체 로그 레벨
    *,
    json_mode: Optional[bool] = None, # JSON 모드
    log_file: Optional[str] = None, # 파일 로그 경로
    quiet_uvicorn_access: bool = False, # uvicorn access 로그 레벨
) -> None:

    # ENV 우선 적용
    if json_mode is None:
        json_mode = os.getenv("LOG_JSON", "0") == "1"
    if log_file is None:
        log_file = os.getenv("LOG_FILE")

    # 중복 핸들러 방지
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)

    # 루트 로거 레벨 설정
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    # 콘솔 핸들러 추가
    root.addHandler(_build_stream_handler(json_mode))

    # 파일 핸들러(선택) 추가
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

# 모듈/컴포넌트별로 로거 획득
def get_logger(name: str) -> Logger:
    return logging.getLogger(name)
