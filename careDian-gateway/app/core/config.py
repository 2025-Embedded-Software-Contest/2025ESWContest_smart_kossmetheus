from __future__ import annotations
from pydantic import Field # 데이터 모델의 Field 정의
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Any


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # app
    app_name: str = Field("CareDian Gateway", alias="APP_NAME")
    env: str = Field("dev", alias="ENV")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    log_json: bool = Field(False, alias="LOG_JSON")
    allowed_origins: list[str] = Field("[]", alias="ALLOWED_ORIGINS")

    # InfluxDB 1.x
    influx_proto: str = Field("http", alias="INFLUX_PROTO")
    influx_host: str = Field(..., alias="INFLUX_HOST")
    influx_port: int = Field("8086", alias="INFLUX_PORT")
    influxdb_url: Optional[str] = Field(None, alias="INFLUXDB_URL")
    influx_db: str = Field(..., alias="INFLUX_DB")
    influx_username: str = Field(..., alias="INFLUX_USERNAME")
    influx_password: str = Field(..., alias="INFLUX_PASSWORD")
    influx_timeout_sec: int = Field("5", alias="INFLUX_TIMEOUT_SEC")
    influx_verify_tls: bool = Field("0", alias="INFLUX_VERIFY_TLS")
    influx_measurement: str = Field("fall_events", alias="INFLUX_MEASUREMENT")

    # HA
    ha_base_url: str = Field(..., alias="HA_BASE_URL")
    ha_token: str = Field(..., alias="HA_TOKEN")
    request_timeout: int = Field(10, alias="REQUEST_TIMEOUT_S")

    # Notify targets
    ha_notify_mobile: str = Field("", alias="HA_NOTIFY_MOBILE")
    ha_notify_persist: str = Field("persistent_notification.create", alias="HA_NOTIFY_PERSIST")
    location_default: str = Field("home", alias="LOCATION_DEFAULT")
    
    @property
    def influxdb_url(self) -> str:
        return f"{self.influx_proto}://{self.influx_host}:{self.influx_port}"

settings = Settings()
