from app.core.config import settings
from .influx_v1 import InfluxServiceV1


influx = InfluxServiceV1(
    url=settings.influxdb_url,
    database=settings.influxdb_db,
    username=settings.influxdb_user,
    password=settings.influxdb_password,
    timeout_ms=settings.influxdb_timeout_ms,
    verify_ssl=settings.influxdb_verify_ssl,
)
