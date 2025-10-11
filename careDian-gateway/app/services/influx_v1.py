from __future__ import annotations
from urllib.parse import urlparse
from typing import Any, Dict, List, Optional, Union

from influxdb import InfluxDBClient  # 1.x client
from app.core.config import settings


Number = Union[int, float]
FieldValue = Union[Number, str, bool]
JsonPoint = Dict[str, Any]

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

    # internal
    def _ensure_client(self) -> InfluxDBClient:
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
    
    def healthy(self) -> bool:
        try:
            self._ensure_client().ping() # ping이 성공하면 정상
            return True
        except Exception:
            return False

    def close(self) -> None:
        if self._client is not None:
            try:
                self._client.close()
            finally:
                self._client = None

    # read
    def query_raw(self, q: str) -> List[Dict[str, Any]]:
        """
        InfluxQL 실행 결과(series) -> 평탄화된 dict 리스트로 반환
        """
        client = self._ensure_client()
        result = client.query(q)
        out: List[Dict[str, Any]] = []
        raw = getattr(result, "raw", {}) or {}
        for series in raw.get("series", []) or []:
            cols = series.get("columns", []) or []
            tags = series.get("tags", {}) or {}
            for row in series.get("values", []) or []:
                item = dict(zip(cols, row))
                if tags:
                    item.update(tags)
                out.append(item)
        return out
    
    def select_range(
        self,
        measurement: str,
        start_ago: str = "1h",                 # "5m", "1h", "24h", "7d" 등
        fields: Optional[List[str]] = None,    # None이면 *
        tags: Optional[Dict[str, str]] = None, # {"device_id":"esp32-01"}
        limit: int = 100,
        desc: bool = True,
    ) -> List[Dict[str, Any]]:
        def ident(x: str) -> str:
            return f'"{x.replace("\"", "\\\"")}"'
        def tag_val(v: str) -> str:
            return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"

        fields_sql = "*" if not fields else ", ".join(ident(f) for f in fields)
        where = [f"time >= now() - {start_ago}"]
        if tags:
            for k, v in tags.items():
                where.append(f"{ident(k)} = {tag_val(v)}")
        where_sql = " WHERE " + " AND ".join(where) if where else ""
        order_sql = " ORDER BY time DESC" if desc else ""
        limit_sql = f" LIMIT {int(limit)}" if limit else ""
        q = f"SELECT {fields_sql} FROM {ident(measurement)}{where_sql}{order_sql}{limit_sql}"
        return self.query_raw(q)
    
    # write
    def write_json(self, points: List[JsonPoint], time_precision: str = "ms") -> int:
        """
        points 예시:
        [{"measurement":"fall_events","tags":{"device_id":"esp32"},"fields":{"value":1,"conf":0.91},"time":"2025-10-10T12:34:56Z"}]
        """
        if not points:
            return 0
        ok = self._ensure_client().write_points(
            points, database=self._database, time_precision=time_precision, protocol="json"
        )
        return len(points) if ok else 0
    
    def write_line(self, lines: Union[str, List[str]]) -> int:
        """
        line protocol: "m,tag=v field=1i 1696930000000000000"
        """
        data: List[str]
        if isinstance(lines, str):
            data = [l for l in lines.splitlines() if l.strip()]
        else:
            data = [l for l in lines if l and l.strip()]
        if not data:
            return 0
        ok = self._ensure_client().write_points(
            data, database=self._database, protocol="line"
        )
        return len(data) if ok else 0
    
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