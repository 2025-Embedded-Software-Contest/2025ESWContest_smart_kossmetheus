from __future__ import annotations

import json, os, sys, logging
from logging.handlers import RotatingFileHandler


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "ts": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            payload.update(record.extra)
        return json.dumps(payload, ensure_ascii=False)

def _build_stream_handler(json_mode: bool) -> logging.Handler:
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(JsonFormatter() if json_mode else logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s", "%Y-%m-%d %H:%M:%S"
    ))
    return h

def _build_file_handler(path: str, json_mode: bool) -> logging.Handler:
    fh = RotatingFileHandler(path, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
    fh.setFormatter(JsonFormatter() if json_mode else logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s", "%Y-%m-%d %H:%M:%S"
    ))
    return fh

def setup_logging(level="INFO", json_mode=None, log_file=None, quiet_uvicorn_access=False):
    if json_mode is None:
        json_mode = os.getenv("LOG_JSON", "0") == "1"
    if log_file is None:
        log_file = os.getenv("LOG_FILE")

    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)

    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.addHandler(_build_stream_handler(json_mode))
    
    if log_file:
        try:
            root.addHandler(_build_file_handler(log_file, json_mode))
        except Exception:
            root.warning("file handler init failed, continue with console only")

    for name, lvl in (
        ("uvicorn", level), ("uvicorn.error", level),
        ("uvicorn.access", "WARNING" if quiet_uvicorn_access else level),
        ("httpx", level), ("asyncio", level),
    ):
        logging.getLogger(name).setLevel(getattr(logging, lvl.upper(), logging.INFO))
