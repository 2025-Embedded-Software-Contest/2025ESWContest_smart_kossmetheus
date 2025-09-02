from __future__ import annotations
import os
from pydantic import BaseModel, Field # 데이터 유효성 검사 및 설정 관리
from typing import List, Optional # 타입 힌트


class Settings(BaseModel):
    ha_base_url: str = Field(..., alias="HA_BASE_URL")
    ha_token: str = Field(..., alias="HA_TOKEN")

    jwt_secret: Optional[str] = Field(default=None, alias="JWT_SECRET")
    jwt_issuer: Optional[str] = Field(default=None, alias="JWT_ISSUER")
    jwt_audience: Optional[str] = Field(default=None, alias="JWT_AUDIENCE")
    access_ttl: int = Field(default=900, alias="ACCESS_TTL") # 15m
    refresh_ttl: int = Field(default=1209600, alias="REFRESH_TTL") # 14d

    api_keys: List[str] = Field(default_factory=list, alias="API_KEYS")
    rate_limit: int = Field(default=60, alias="RATE_LIMIT")
    rate_window_sec: int = Field(default=60, alias="RATE_WINDOW_SEC")
    allowed_origins: List[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    request_timeout: int = Field(default=10, alias="REQUEST_TIMEOUT_S")

    @staticmethod
    def _split(v: Optional[str]) -> List[str]:
        return [s.strip() for s in v.split(",")] if v else []

    @staticmethod
    def load_from_env() -> "Settings":
        data = {
            "HA_BASE_URL": os.getenv("HA_BASE_URL", ""),
            "HA_TOKEN": os.getenv("HA_TOKEN", ""),
            "JWT_SECRET": os.getenv("JWT_SECRET"),
            "JWT_ISSUER": os.getenv("JWT_ISSUER"),
            "JWT_AUDIENCE": os.getenv("JWT_AUDIENCE"),
            "API_KEYS": os.getenv("API_KEYS"),
            "RATE_LIMIT": int(os.getenv("RATE_LIMIT", "60")),
            "RATE_WINDOW_SEC": int(os.getenv("RATE_WINDOW_SEC", "60")),
            "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "REQUEST_TIMEOUT_S": int(os.getenv("REQUEST_TIMEOUT_S", "10")),
            "ACCESS_TTL": int(os.getenv("ACCESS_TTL", "900")),
            "REFRESH_TTL": int(os.getenv("REFRESH_TTL", "1209600")),
        }

        return Settings(
            **{k: v for k, v in data.items() if k not in ("API_KEYS", "ALLOWED_ORIGINS")},
            API_KEYS=Settings._split(data["API_KEYS"]),
            ALLOWED_ORIGINS=Settings._split(data["ALLOWED_ORIGINS"]),
        )