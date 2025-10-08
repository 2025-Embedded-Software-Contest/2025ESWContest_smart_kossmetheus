from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional

class Settings(BaseSettings):
    app_name: str = Field(default="CareDian Fall Gateway", alias="APP_NAME")
    env: str = Field(default="dev", alias="ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_json: bool = Field(default=False, alias="LOG_JSON")
    allowed_origins: List[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")

    # Influx (옵션)
    influx_url: Optional[str] = Field(default=None, alias="INFLUX_URL")
    influx_token: Optional[str] = Field(default=None, alias="INFLUX_TOKEN")
    influx_org: Optional[str] = Field(default=None, alias="INFLUX_ORG")
    influx_bucket: Optional[str] = Field(default=None, alias="INFLUX_BUCKET")

    # HA
    ha_base_url: str = Field(..., alias="HA_BASE_URL")
    ha_token: str = Field(..., alias="HA_TOKEN")
    request_timeout: int = Field(default=10, alias="REQUEST_TIMEOUT_S")

    # Notify targets
    ha_notify_mobile: str = Field(default="notify.mobile_app_device", alias="HA_NOTIFY_MOBILE")
    ha_notify_persist: str = Field(default="notify.persistent_notification", alias="HA_NOTIFY_PERSIST")
    location_default: str = Field(default="home", alias="LOCATION_DEFAULT")

    class Config:
        env_file = ".env"

settings = Settings()
