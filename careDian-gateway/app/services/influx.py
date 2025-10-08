from typing import Optional, Dict, Any
from app.core.config import settings

_client = None
_write_api = None

def _enabled() -> bool:
    return bool(settings.influx_url and settings.influx_token and settings.influx_org and settings.influx_bucket)

def init() -> None:
    global _client, _write_api
    if not _enabled():
        return
    from influxdb_client import InfluxDBClient
    _client = InfluxDBClient(url=settings.influx_url, token=settings.influx_token, org=settings.influx_org)
    _write_api = _client.write_api()

def close() -> None:
    global _client, _write_api
    if _write_api:
        _write_api.close()
    if _client:
        _client.close()
    _client = None
    _write_api = None

def write_point(measurement: str, tags: Dict[str, str], fields: Dict[str, Any], ts_ns: Optional[int] = None) -> None:
    """ts_ns: 나노초 타임스탬프(옵션)"""
    if not _enabled():
        return
    from influxdb_client import Point
    p = Point(measurement)
    for k, v in tags.items():
        p = p.tag(k, v)
    for k, v in fields.items():
        p = p.field(k, v)
    if ts_ns is not None:
        p = p.time(ts_ns, write_precision="ns")
    _write_api.write(bucket=settings.influx_bucket, record=p)
