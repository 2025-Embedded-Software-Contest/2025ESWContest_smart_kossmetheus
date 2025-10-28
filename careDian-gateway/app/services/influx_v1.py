"""
모듈: services/influx_v1.py — InfluxDB 1.x 서비스 어댑터

역할:
  • InfluxDB 1.x 서버 연결/생성 및 읽기·쓰기 유틸 제공
  • query_raw / select_range 로 조회, write_point 로 단일 포인트 쓰기
  • (보조) write_fall_event: 낙상 이벤트 전용 쓰기 헬퍼(라인/JSON 프로토콜)

설계 포인트:
  - URL 파싱 → 호스트/포트/SSL 여부 자동 결정
  - 클라이언트 지연 생성(_ensure_client) + DB 존재 시 스위치, 없으면 생성 시도
  - healthy(), close() 로 연결 상태 확인 및 정리
  - query_raw(): InfluxQL 결과를 평탄화(list[dict])로 변환
  - select_range(): 태그/기간/정렬/limit 만으로 간단 조회 구성
  - write_point(): 타입 안전 보정(int/float/bool/str) + ns 타임스탬프 지원

주의:
  - InfluxDB 1.x 클라이언트(influxdb.InfluxDBClient) 사용
  - DB 생성은 권한이 없을 수 있으므로 예외 시 switch_database 로 폴백
"""

from __future__ import annotations
from urllib.parse import urlparse
from typing import Any, Dict, List, Optional, Union, Mapping
from influxdb import InfluxDBClient  # 1.x client

from app.core.config import settings


# 타입 별칭: 수치/필드 값/JSON 포인트 표현
Number = Union[int, float]
FieldValue = Union[Number, str, bool]
JsonPoint = Dict[str, Any]


def _is_int(x):
    """bool 은 int 의 서브클래스이므로 분리하여 '진짜 정수'만 식별.
    - Influx field 타입 보정 시 사용.
    """
    return isinstance(x, bool) is False and isinstance(x, int)


class InfluxServiceV1:
    """InfluxDB 1.x용 경량 서비스 래퍼.

    Args:
      url: "http://host:8086" 또는 "https://host:8086"
      database: 기본 DB 이름
      rp: 기본 Retention Policy(선택)
      username/password: 인증 정보
      timeout_sec: HTTP 타임아웃(초)
      verify_ssl: https 시 서버 인증서 검증 여부
    """

    def __init__(
        self,
        url: str,
        database: str,
        rp: str | None = None,
        username: str | None = None,
        password: str | None = None,
        timeout_sec: int = 5,
        verify_ssl: bool = False,
    ):
        self.url = url
        self.database = database
        self.rp = rp
        self.username = username
        self.password = password
        self.timeout = timeout_sec
        self.verify_ssl = verify_ssl
        self._client: InfluxDBClient | None = None  # 지연 로딩된 실제 클라이언트 캐시
        self._ensure_client()  # 초기 연결 확인/DB 스위치

    # ------------------------------------------------------------------
    # 내부: 클라이언트 준비/DB 생성 보장
    # ------------------------------------------------------------------
    def _ensure_client(self) -> InfluxDBClient:
        """InfluxDBClient 인스턴스를 생성/캐시하고, 기본 DB로 스위치.
        - DB 미존재 시 create_database 시도(권한 없으면 무시하고 switch만 시도)
        - url 파싱으로 scheme/host/port/ssl 자동 계산
        """
        if self._client:
            return self._client
        
        parsed = urlparse(self.url)
        scheme = parsed.scheme or "http"
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or (443 if scheme == "https" else 8086)
        use_ssl = scheme == "https"

        # InfluxDBClient 구성: ssl/verify_ssl/timeout 등 옵션 반영
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

        # 데이터베이스 보장: 존재하지 않으면 생성(권한 없으면 예외 무시하고 스위치만)
        try:
            dbs = [d.get('name') for d in self._client.get_list_database()]
            if self.database not in dbs:
                self._client.create_database(self.database)
            self._client.switch_database(self.database)
        except Exception:
            # 읽기 전용/권한 부족 환경일 수 있음
            self._client.switch_database(self.database)
        return self._client
    
    def healthy(self) -> bool:
        """핑 호출로 연결상태 점검(성공 시 True)."""
        try:
            self._ensure_client().ping()
            return True
        except Exception:
            return False

    def close(self) -> None:
        """클라이언트 연결 종료 및 캐시 해제."""
        if self._client is not None:
            try:
                self._client.close()
            finally:
                self._client = None

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def query_raw(self, q: str) -> List[Dict[str, Any]]:
        """임의 InfluxQL 실행 결과를 평탄화(list[dict])로 반환.

        InfluxDBClient.query 의 결과(result.raw.series[*])를 순회하며
        각 시리즈의 columns/values 를 zip → dict 로 만들고, series.tags 가 있으면 병합한다.
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
        """기간/태그/필드/정렬/limit 만으로 간단 조회를 구성하여 실행.
        - 식별자(identifier) 이스케이프, 태그 값 이스케이프 보장
        - 내부적으로 query_raw 를 사용
        """
        def ident(x: str) -> str:
            # 식별자 이스케이프: 백슬래시/쌍따옴표 이스케이프 후 ""로 감싸기
            x = x.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{x}"'
        def tag_val(v: str) -> str:
            # 태그 값 이스케이프: 백슬래시/홑따옴표 이스케이프 후 ''로 감싸기
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
    
    # ------------------------------------------------------------------
    # WRITE
    # ------------------------------------------------------------------
    def write_point(
        self,
        measurement: str,
        tags: Mapping[str, str] | None,
        fields: Mapping[str, FieldValue],
        ts_ns: int | None = None,
        rp: str | None = None,
    ) -> bool:
        """단일 포인트 쓰기.

        특징:
          - fields 의 값 타입을 Influx가 기대하는 형태(int/float/bool/str)로 보정
          - ts_ns 제공 시 나노초 정밀도로 기록(time_precision="n"), 미지정 시 서버시간
          - retention_policy 지정 지원(없으면 self.default_rp 또는 None)
        """
        self._ensure_client()
        point = [{
            "measurement": measurement,
            "tags": {k: str(v) for k, v in (tags or {}).items()},
            "fields": {},
        }]

        # 타입 보정: int/float/bool/str 외에는 str 로 캐스팅하는 대신 원본 유지
        for k, v in fields.items():
            if _is_int(v):
                point[0]["fields"][k] = int(v)
            elif isinstance(v, float):
                point[0]["fields"][k] = float(v)
            else:
                point[0]["fields"][k] = v

        time_precision = None
        if ts_ns is not None:
            point[0]["time"] = int(ts_ns)  # epoch ns
            time_precision = "n"           # ns 정밀도로 전송

        ok = self._client.write_points(
            point,
            retention_policy=(rp or getattr(self, "default_rp", None)),
            time_precision=time_precision,
            protocol="json",
        )
        return bool(ok)


# ----------------------------------------------------------------------
# 보조 함수: 낙상 이벤트 전용 쓰기 헬퍼
#   - self: InfluxServiceV1 인스턴스를 기대(메서드처럼 호출 가능)
#   - ns 타임스탬프가 있으면 line protocol, 없으면 json protocol 사용
# ----------------------------------------------------------------------
def write_fall_event(
    self,
    device_id: str,
    prob: float,
    location: str | None = None,
    extra_tags: Dict[str, str] | None = None,
    extra_fields: Dict[str, Any] | None = None,
    measurement: str | None = None,
    ts_ns: int | None = None,
    rp: str | None = None
) -> bool:
    """낙상(fall) 이벤트를 편리하게 기록하는 헬퍼.

    - measurement 미지정 시 settings.influx_measurement 사용
    - tags: device_id (+ location/extra_tags)
    - fields: prob (+ extra_fields)
    - ts_ns 제공 시 line protocol 로 ns 정밀 기록, 없으면 json protocol
    """
    cli = self._ensure_client()
    m = measurement or settings.influx_measurement

    # 태그/필드 구성
    tags = {"device_id": device_id}
    if location:
        tags["location"] = location
    if extra_tags:
        tags.update({k: str(v) for k, v in extra_tags.items()})

    fields: Dict[str, Any] = {"prob": float(prob)}
    if extra_fields:
        fields.update(extra_fields)

    if ts_ns is not None:
        # --- line protocol (ns 정밀) ---
        def esc_tag(v: str) -> str:
            # 태그값 이스케이프: 백슬래시/쉼표/공백
            return v.replace("\\", "\\\\").replace(",", "\\,").replace(" ", "\\ ")

        tag_str = ",".join([f"{k}={esc_tag(str(v))}" for k, v in tags.items()]) if tags else ""

        # 필드 시리얼라이즈: bool/정수/실수/문자열별 다른 포맷
        field_parts = []
        for k, v in fields.items():
            if isinstance(v, bool):
                field_parts.append(f'{k}={"true" if v else "false"}')
            elif isinstance(v, (int, float)):
                # 정수는 1i, 실수는 그대로
                if isinstance(v, int):
                    field_parts.append(f"{k}={v}i")
                else:
                    field_parts.append(f"{k}={v}")
            else:
                s = str(v).replace("\\", "\\\\").replace('"', '\\"')
                field_parts.append(f'{k}="{s}"')
        field_str = ",".join(field_parts)

        line = f"{m}{(',' + tag_str) if tag_str else ''} {field_str} {int(ts_ns)}"
        return cli.write_points([line], protocol="line", retention_policy=(rp or self.rp))

    else:
        # --- json protocol (서버시간) ---
        point = [{
            "measurement": m,
            "tags": tags,
            "fields": fields,
        }]
        return cli.write_points(point)
