from __future__ import annotations
from urllib.parse import urlparse
from typing import Any, Dict
import logging

from influxdb import InfluxDBClient  # 1.x client
from app.core.config import settings


class InfluxServiceV1:
    def __init__(
        self,
        url: str,
        database: str,
        username: str | None = None,
        password: str | None = None,
        timeout_sec: int = 5,
        verify_ssl: bool = False,
    ):
        self.url = url
        self.database = database
        self.username = username
        self.password = password
        self.timeout = timeout_sec
        self.verify_ssl = verify_ssl
        self._client: InfluxDBClient | None = None
        self._ensure_client()

    def _ensure_client(self) -> InfluxDBClient:
        # for logging
        logger = logging.getLogger(__name__)
        logger.info(
            "InfluxDB connect: url=%s, db=%s, verify_ssl=%s, timeout_sec=%s",
            self.url, self.database, self.verify_ssl, self.timeout
        )

        if self._client:
            return self._client
        
        parsed = urlparse(self.url)
        scheme = parsed.scheme or "http"
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or (443 if scheme == "https" else 8086)
        use_ssl = scheme == "https"

        self._client = InfluxDBClient(
            host=host,
            port=port,
            username=self.username,
            password=self.password,
            database=self.database,
            ssl=use_ssl,
            verify_ssl=self.verify_ssl if use_ssl else False,
            timeout=self.timeout,
        )

        # 데이터베이스가 없으면 생성 (권한 필요)
        try:
            dbs = [d.get('name') for d in self._client.get_list_database()]
            if self.database not in dbs:
                self._client.create_database(self.database)
            self._client.switch_database(self.database)
        except Exception:
            # 읽기 전용이거나 권한 부족한 환경이면 생성은 스킵
            self._client.switch_database(self.database)
        return self._client

    def write_fall_event(
        self,
        camera_id: str,
        prob: float,
        location: str | None = None,
        extra_tags: Dict[str, str] | None = None,
        extra_fields: Dict[str, Any] | None = None,
        measurement: str | None = None,
    ) -> bool:
        cli = self._ensure_client()
        tags = {"camera_id": camera_id}
        if location:
            tags["location"] = location
        if extra_tags:
            tags.update({k: str(v) for k, v in extra_tags.items()})

        fields: Dict[str, Any] = {"prob": float(prob)}
        if extra_fields:
            fields.update(extra_fields)

        point = [{
            "measurement": measurement or settings.influx_measurement,
            "tags": tags,
            "fields": fields,
        }]

        return cli.write_points(point)
    
    def healthy(self) -> bool:
        try:
            cli = self._ensure_client()
            cli.ping() # ping이 성공하면 정상
            return True
        except Exception:
            return False
        
    def close(self) -> None:
        if self._client is not None:
            try:
                self._client.close()
            finally:
                self._client = None
