from __future__ import annotations # 타입 힌트 평가 X, 문자열로 저장
import os # OS 모듈
from pydantic import BaseModel, Field # 데이터 모델, 데이터 모델의 Field 정의
from typing import List, Optional # 타입 힌트


class Settings(BaseModel):
    # HA (프록시/알림용)
    ha_base_url: Optional[str] = Field(default=None, alias="HA_BASE_URL") # required
    ha_token: Optional[str] = Field(default=None, alias="HA_TOKEN") # required
    ha_notify_services: List[str] = Field(default_factory=list, alias="HA_NOTIFY_SERVICES")

    # OAuth(OIDC) → 내부 JWT 재발급
    oidc_issuer_url: Optional[str] = Field(default=None, alias="OIDC_ISSUER_URL") # required
    oidc_client_id: Optional[str] = Field(default=None, alias="OIDC_CLIENT_ID") # required

    jwt_secret: Optional[str] = Field(default=None, alias="JWT_SECRET") # required
    jwt_issuer: Optional[str] = Field(default=None, alias="JWT_ISSUER") # optional
    jwt_audience: Optional[str] = Field(default=None, alias="JWT_AUDIENCE") # optional
    access_ttl: int = Field(default=900, alias="ACCESS_TTL")          # optional 15m
    refresh_ttl: int = Field(default=1209600, alias="REFRESH_TTL")    # optional 14d

    # API 보호
    api_keys: List[str] = Field(default_factory=list, alias="API_KEYS") # optional
    rate_limit: int = Field(default=60, alias="RATE_LIMIT") # optional
    rate_window_sec: int = Field(default=60, alias="RATE_WINDOW_SEC") # optional

    # CORS/네트워크
    allowed_origins: List[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS") # optional CORS 허용 오리진(쉼표 분리)
    request_timeout: int = Field(default=10, alias="REQUEST_TIMEOUT_S") # optional 외부 호출 타임아웃
    log_level: str = Field(default="INFO", alias="LOG_LEVEL") # optional

    # HA 프록시 SSO 헤더
    ha_sso_header: str = Field(default="X-Remote-User", alias="HA_SSO_HEADER") # optional
    ha_sso_groups_header: Optional[str] = Field(default="X-Remote-Groups", alias="HA_SSO_GROUPS_HEADER") # optional
    ha_sso_default_groups: str = Field(default="users", alias="HA_SSO_DEFAULT_GROUPS") # optional

    # 실행/디버그
    force_stub: bool = Field(default=False, alias="FORCE_STUB") # optional SSL 없어도 Stub ASGI로 기동
    simulate_no_ssl: bool = Field(default=False, alias="SIMULATE_NO_SSL") # optional SSL 부재 상황 시뮬레이션

    @staticmethod
    def _split_csv(v: Optional[str]) -> List[str]:
        return [s.strip() for s in v.split(",")] if v else []

    @staticmethod
    def load() -> "Settings":
        data = {
            "HA_BASE_URL": os.getenv("HA_BASE_URL"),
            "HA_TOKEN": os.getenv("HA_TOKEN"),
            "HA_NOTIFY_SERVICES": os.getenv("HA_NOTIFY_SERVICES"),

            "OIDC_ISSUER_URL": os.getenv("OIDC_ISSUER_URL"),
            "OIDC_CLIENT_ID": os.getenv("OIDC_CLIENT_ID"),

            "JWT_SECRET": os.getenv("JWT_SECRET"),
            "JWT_ISSUER": os.getenv("JWT_ISSUER"),
            "JWT_AUDIENCE": os.getenv("JWT_AUDIENCE"),
            "ACCESS_TTL": int(os.getenv("ACCESS_TTL", "900")),
            "REFRESH_TTL": int(os.getenv("REFRESH_TTL", "1209600")),

            "API_KEYS": os.getenv("API_KEYS"),
            "RATE_LIMIT": int(os.getenv("RATE_LIMIT", "60")),
            "RATE_WINDOW_SEC": int(os.getenv("RATE_WINDOW_SEC", "60")),
            "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS"),
            "REQUEST_TIMEOUT_S": int(os.getenv("REQUEST_TIMEOUT_S", "10")),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),

            "HA_SSO_HEADER": os.getenv("HA_SSO_HEADER", "X-Remote-User"),
            "HA_SSO_GROUPS_HEADER": os.getenv("HA_SSO_GROUPS_HEADER", "X-Remote-Groups"),
            "HA_SSO_DEFAULT_GROUPS": os.getenv("HA_SSO_DEFAULT_GROUPS", "users"),

            "FORCE_STUB": os.getenv("FORCE_STUB", "0") == "1",
            "SIMULATE_NO_SSL": os.getenv("SIMULATE_NO_SSL", "0") == "1",
        }
        
        return Settings(
            **{k: v for k, v in data.items() if k not in ("HA_NOTIFY_SERVICES","API_KEYS","ALLOWED_ORIGINS")},
            HA_NOTIFY_SERVICES=Settings._split_csv(data["HA_NOTIFY_SERVICES"]),
            API_KEYS=Settings._split_csv(data["API_KEYS"]),
            ALLOWED_ORIGINS=Settings._split_csv(data["ALLOWED_ORIGINS"]),
        )