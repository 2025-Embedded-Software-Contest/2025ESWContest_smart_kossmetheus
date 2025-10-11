from app.core.config import settings
from .influx_v1 import InfluxServiceV1


verify_arg = settings.influx_ca_cert or settings.influx_verify_tls

influx = InfluxServiceV1(
    url=settings.influx_url,
    database=settings.influx_db,
    username=settings.influx_username,
    password=settings.influx_password,
    timeout_sec=settings.influx_timeout_sec,
    verify_ssl=verify_arg,
)
