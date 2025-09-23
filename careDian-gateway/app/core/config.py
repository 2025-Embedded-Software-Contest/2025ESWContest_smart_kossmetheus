from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field # 데이터 모델의 Field 정의
from typing import List, Optional # 타입 힌트


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,       # 대소문자 혼용 허용
        extra="ignore",             # 여분 키 무시 (향후 strict로 변경 가능)
    )

    # app
    app_name: str = Field("CareDian Gateway", alias="APP_NAME")
    env: str = Field("dev", alias="ENV")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    log_json: bool = Field(False, alias="LOG_JSON")
    enable_docs: bool = Field(True, alias="ENABLE_DOCS")

    # docs basic auth (prod에서만 쓰면 됨)
    docs_username: Optional[str] = Field(None, alias="DOCS_USERNAME")
    docs_password: Optional[str] = Field(None, alias="DOCS_PASSWORD")

    # CORS
    allowed_origins: List[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")

    # OIDC
    oidc_issuer: Optional[str] = None              # e.g. https://auth.example.com/realms/main
    oidc_client_id: Optional[str] = None
    oidc_client_secret: Optional[str] = None
    oidc_redirect_uri: Optional[str] = None        # e.g. https://gw.example.com/auth/oidc/callback
    oidc_scopes: List[str] = ["openid", "profile", "email"]

    # JWT / 세션
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_issuer: Optional[str] = Field(None, alias="JWT_ISSUER")
    jwt_audience: Optional[str] = Field(None, alias="JWT_AUDIENCE")
    access_ttl: int = Field(900, alias="ACCESS_TTL")          # 15m
    refresh_ttl: int = Field(1209600, alias="REFRESH_TTL")    # 14d
    session_cookie: str = Field("cd_session", alias="SESSION_COOKIE")

    # HA
    ha_base_url: str = Field(..., alias="HA_BASE_URL")
    ha_token: str = Field(..., alias="HA_TOKEN")
    request_timeout: int = Field(10, alias="REQUEST_TIMEOUT_S")

    # SSO header (게이트웨이 -> HA 프록시 시 삽입)
    sso_base_url: Optional[str] = Field(default=None, alias="SSO_BASE_URL")
    ha_sso_header: str = Field("X-Remote-User", alias="HA_SSO_HEADER")
    ha_sso_groups_header: Optional[str] = Field("X-Remote-Groups", alias="HA_SSO_GROUPS_HEADER")
    ha_sso_default_groups: Optional[str] = Field("ha-users", alias="HA_SSO_DEFAULT_GROUPS")

    # Rate limit
    rate_limit: int = Field(60, alias="RATE_LIMIT")
    rate_window_sec: int = Field(60, alias="RATE_WINDOW_SEC")

    # api keys list
    api_keys: List[str] = [] # .env: API_KEYS=["k1","k2"] 또는 CSV

settings = Settings()

def origins() -> List[str]:
    return [o.strip() for o in settings.allowed_origins if o and o.strip()]
