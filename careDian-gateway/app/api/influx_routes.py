"""
모듈: api/influx_routes.py
역할:
  - InfluxDB(v1) 관련 관리/진단용 API 제공
    * /influx/ping : Influx 연결 헬스 체크
    * /influx/query : InfluxQL RAW 질의 실행(관리 전용, 신중히 사용)
    * /influx/write/point : JSON 포인트 쓰기(배치 지원)

주의/보안:
  - /query 는 임의 InfluxQL 실행이 가능하므로 외부 노출 금지(관리자 보호 필수)
  - InfluxService의 healthy()/write_point()/query_raw() 동작에 의존
  - settings.*(influx_measurement, influx_rp 등) 환경값을 기본값으로 사용
"""

from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union

from app.services import influx  # Influx v1 서비스 어댑터 (healthy/query_raw/write_point 등 제공)
from app.core.config import settings  # 환경설정(기본 measurement, RP 등)


# 라우터: /influx 프리픽스, 문서 태그 "influx"
router = APIRouter(prefix="/influx", tags=["influx"])


# ----------------------------------------------------------------------------
# 요청/응답 모델 정의
# ----------------------------------------------------------------------------
class WritePoint(BaseModel):
    """InfluxDB Line Protocol 1건에 해당하는 JSON 표현

    - measurement: 미지정 시 상위 default_measurement를 사용
    - tags: 태그 key/value (str->str)
    - fields: 필드 key/value (int/float/str/bool 허용)
    - time: 타임스탬프 (ISO8601 or epoch(ns)); int(ns)만 직접 전달됨
    """
    measurement: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    fields: Dict[str, Union[int, float, str, bool]]
    time: Optional[Union[str, int]] = None  # ISO8601 또는 epoch(ns)


class WriteBody(BaseModel):
    """여러 포인트를 한 번에 쓰기 위한 래퍼 바디"""
    points: List[WritePoint]
    # 기본 measurement: .env에 지정된 influx_measurement 사용(없으면 서비스 내부 기본값)
    default_measurement: Optional[str] = Field(settings.influx_measurement)


# ----------------------------------------------------------------------------
# 헬스 체크: /influx/ping
# ----------------------------------------------------------------------------
@router.get("/ping")
def ping():
    """Influx 서비스 헬스 상태를 boolean으로 반환"""
    return {"ok": influx.healthy()}


# ----------------------------------------------------------------------------
# READ(관리용): 임의 InfluxQL RAW 실행
#  - 위험: 외부 노출 금지/관리자 보호 필수
# ----------------------------------------------------------------------------
class RawQuery(BaseModel):
    """임의 InfluxQL 실행을 위한 쿼리 래퍼"""
    q: str


@router.post("/query")
def query_raw(body: RawQuery):
    """InfluxQL RAW를 실행하고 결과를 그대로 반환(서비스 어댑터에 위임)

    보안 노트:
      - 관리 콘솔/내부망에서만 호출되도록 구성
      - 요청/응답 로깅 시 민감 정보 마스킹 권장
    """
    return influx.query_raw(body.q)


# ----------------------------------------------------------------------------
# WRITE: JSON 포인트 쓰기 (배치)
# ----------------------------------------------------------------------------
@router.post("/write/point", summary="Point")
def write_point(body: WriteBody):
    """여러 개의 포인트를 한 번에 InfluxDB에 기록

    처리 흐름:
      1) body.default_measurement 를 기본 측정명으로 결정
      2) 각 포인트에 대해 measurement/tags/fields/ts_ns/rp를 구성
      3) write_point(...) 성공 건 수를 카운트하여 반환

    주의:
      - time이 int(ns)일 때만 ts_ns로 전달; ISO 문자열은 현재 어댑터에서 직접 파싱하지 않음
      - settings.influx_rp(보존정책)가 설정되어 있으면 해당 값 사용
    """
    default_m = body.default_measurement or settings.influx_measurement
    written = 0

    for p in body.points:
        ok = influx.write_point(
            measurement=(p.measurement or default_m),  # 포인트별 측정명 우선, 없으면 기본값
            tags=(p.tags or {}),                       # None 허용 → 빈 딕셔너리로 대체
            fields=p.fields,                           # 유효 타입: int/float/str/bool
            ts_ns=(p.time if isinstance(p.time, int) else None),  # epoch(ns)만 직접 지정
            rp=getattr(settings, "influx_rp", None),  # 설정에 정의된 Retention Policy 사용
        )
        if ok:
            written += 1

    return {"written": written}
