from __future__ import annotations

from pydantic import Field, field_validator # 데이터 모델의 Field 정의
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List, Any
from pathlib import Path
from dotenv import find_dotenv
import json


# .env 경로를 안정적으로 찾기 (CWD 우선 → 리로더/서브프로세스에서도 루트 폴백)
ENV_FILE = find_dotenv(usecwd=True) or str((Path(__file__).resolve().parents[2] / ".env"))

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # app
    app_name: str = Field("CareDian Gateway", alias="APP_NAME")
    env: str = Field("dev", alias="ENV")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    log_json: bool = Field(False, alias="LOG_JSON")
    allowed_origins: List[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")

    # InfluxDB 1.x
    influx_url: str = Field(..., alias="INFLUX_URL")
    influx_proto: str = Field("http", alias="INFLUX_PROTO")
    influx_host: str = Field("", alias="INFLUX_HOST")
    influx_port: int = Field(8086, alias="INFLUX_PORT")
    influx_db: str = Field(..., alias="INFLUX_DB")
    influx_username: str = Field(..., alias="INFLUX_USERNAME")
    influx_password: str = Field(..., alias="INFLUX_PASSWORD")
    influx_timeout_sec: int = Field(5, alias="INFLUX_TIMEOUT_SEC")
    influx_verify_tls: bool = Field(False, alias="INFLUX_VERIFY_TLS")
    influx_ca_cert: Optional[str] = Field(None, alias="INFLUX_CA_CERT")
    influx_measurement: str = Field("fall_events", alias="INFLUX_MEASUREMENT")

    # HA
    ha_base_url: str = Field(..., alias="HA_BASE_URL")
    ha_token: str = Field(..., alias="HA_TOKEN")
    request_timeout: int = Field(10, alias="REQUEST_TIMEOUT_SEC")

    # Notify targets
    ha_notify_mobile: str = Field("", alias="HA_NOTIFY_MOBILE")
    ha_notify_persist: str = Field("persistent_notification.create", alias="HA_NOTIFY_PERSIST")
    location_default: str = Field("home", alias="LOCATION_DEFAULT")

    # validators
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def _parse_allowed_origins(cls, v: Any):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        s = str(v).strip()
        if not s:
            return []
        if s.startswith("["):
            try:
                arr = json.loads(s)
                return arr if isinstance(arr, list) else []
            except Exception:
                pass
        return [t.strip() for t in s.split(",") if t.strip()]
    
    @field_validator("log_json", "influx_verify_tls", mode="before")
    @classmethod
    def _parse_bool_loose(cls, v: Any):
        if isinstance(v, bool):
            return v
        s = str(v).strip().lower()
        return s in {"1", "true", "yes", "on"}

settings = Settings()
