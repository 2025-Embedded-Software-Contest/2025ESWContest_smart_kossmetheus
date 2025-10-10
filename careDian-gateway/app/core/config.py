from pydantic import BaseModel
import os, json


def str2bool(v: str) -> bool:
    return str(v).lower() in {"1","true","yes","on"}

def parse_list(s: str):
    try:
        return json.loads(s)
    except Exception:
        return [x.strip() for x in s.split(",") if x.strip()]
    
class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "CareDian Gateway")
    env: str = os.getenv("ENV", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_json: bool = str2bool(os.getenv("LOG_JSON","0"))
    allowed_origins: list[str] = parse_list(os.getenv("ALLOWED_ORIGINS","[]"))

    # InfluxDB 1.x
    influx_proto: str = os.getenv("INFLUX_PROTO","http")
    influx_host: str = os.getenv("INFLUX_HOST","localhost")
    influx_port: int = int(os.getenv("INFLUX_PORT","8086"))
    influx_db: str = os.getenv("INFLUX_DB","caredian")
    influx_username: str = os.getenv("INFLUX_USERNAME","")
    influx_password: str = os.getenv("INFLUX_PASSWORD","")
    influx_timeout_sec: int = int(os.getenv("INFLUX_TIMEOUT_SEC","5"))
    influx_verify_tls: bool = str2bool(os.getenv("INFLUX_VERIFY_TLS","0"))
    influx_measurement: str = os.getenv("INFLUX_MEASUREMENT","fall_events")

    # HA
    ha_base_url: str = os.getenv("HA_BASE_URL","")
    ha_token: str = os.getenv("HA_TOKEN","")
    request_timeout_s: int = int(os.getenv("REQUEST_TIMEOUT_S","10"))

    # Notify targets
    ha_notify_mobile: str = os.getenv("HA_NOTIFY_MOBILE","")
    ha_notify_persist: str = os.getenv("HA_NOTIFY_PERSIST","persistent_notification.create")
    location_default: str = os.getenv("LOCATION_DEFAULT","home")

settings = Settings()
