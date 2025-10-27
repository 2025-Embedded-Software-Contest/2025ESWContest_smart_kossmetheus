from __future__ import annotations
from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Any

from app.services import influx
from app.core.config import settings
from app.security.ha_auth import require_ha_user


router = APIRouter(prefix="/influx", tags=["influx"])

# 모델
class WritePoint(BaseModel):
    measurement: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    fields: Dict[str, Union[int, float, str, bool]]
    time: Optional[Union[str, int]] = None  # ISO8601 또는 epoch(ns)

class WriteBody(BaseModel):
    points: List[WritePoint]
    default_measurement: Optional[str] = Field(settings.influx_measurement)

# 헬스
@router.get("/ping")
def ping():
    return {"ok": influx.healthy()}

# READ: 낙상 목록
@router.get("/falls", dependencies=[Depends(require_ha_user)])
def list_falls(
    hours: int = Query(24, ge=1, le=720),
    limit: int = Query(100, ge=1, le=1000),
    device_id: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    desc: bool = Query(True),
) -> List[Dict[str, Any]]:
    """
    최근 N시간의 낙상 raw 레코드 조회.
    """

    if not influx.healthy():
        raise HTTPException(status_code=503, detail="InfluxDB unreachable")

    tags: Dict[str, str] = {}
    if device_id:
        tags["device_id"] = device_id
    if location:
        tags["location"] = location

    try:
        rows = influx.select_range(
            measurement=settings.influx_measurement,
            start_ago=f"{hours}h",
            fields=None,  # 전체 필드
            tags=tags or None,
            limit=limit,
            desc=desc,
        )

        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

# READ: InfluxQL raw (관리용)
class RawQuery(BaseModel):
    q: str

@router.post("/query")
def query_raw(body: RawQuery):
    return influx.query_raw(body.q)

# WRITE: JSON points
@router.post("/write/point", summary="Point")
def write_point(body: WriteBody):
    default_m = body.default_measurement or settings.influx_measurement
    written = 0

    for p in body.points:
        ok = influx.write_point(
            measurement=(p.measurement or default_m),
            tags=(p.tags or {}),
            fields=p.fields,
            ts_ns=(p.time if isinstance(p.time, int) else None),
            rp=getattr(settings, "influx_rp", None),
        )
        if ok:
            written += 1

    return {"written": written}
