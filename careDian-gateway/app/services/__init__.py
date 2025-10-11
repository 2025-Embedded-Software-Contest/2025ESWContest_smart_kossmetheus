from app.core.config import settings
from .influx_v1 import InfluxServiceV1


influx = InfluxServiceV1(
    url=settings.influxdb_url,
    database=settings.influx_db,
    username=settings.influx_username,
    password=settings.influx_password,
    timeout_ms=int(settings.influx_timeout_sec * 1000),
    verify_ssl=settings.influx_verify_tls,
)
