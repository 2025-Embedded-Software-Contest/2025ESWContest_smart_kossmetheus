# app/api/influx_routes.py
from __future__ import annotations
from fastapi import APIRouter, Body, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
from app.services import influx
from app.core.config import settings

router = APIRouter(prefix="/influx", tags=["influx"])

# ---- 모델 ----
class WritePoint(BaseModel):
    measurement: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    fields: Dict[str, Union[int, float, str, bool]]
    time: Optional[Union[str, int]] = None  # ISO8601 또는 epoch(ns)

class WriteBody(BaseModel):
    points: List[WritePoint]
    default_measurement: Optional[str] = Field(None, description="없으면 settings.influx_measurement 사용")

# ---- 헬스 ----
@router.get("/ping")
def ping():
    return {"ok": influx.healthy()}

# ---- READ: 파라미터화 ----
@router.get("/read")
def read_points(
    measurement: str = Query(default=settings.influx_measurement),
    start_ago: str = Query(default="1h", pattern=r"^\d+[smhdw]$"),
    fields: Optional[str] = Query(default=None, description="CSV, 예: value,confidence"),
    tags: Optional[str] = Query(default=None, description='JSON, 예: {"device_id":"esp32"}'),
    limit: int = Query(default=100, ge=1, le=5000),
    desc: bool = Query(default=True),
):
    fields_list = [f.strip() for f in fields.split(",")] if fields else None
    tags_dict = None
    if tags:
        try:
            import json
            tags_dict = json.loads(tags)
        except Exception:
            raise HTTPException(status_code=400, detail="tags must be JSON")
    rows = influx.select_range(
        measurement=measurement,
        start_ago=start_ago,
        fields=fields_list,
        tags=tags_dict,
        limit=limit,
        desc=desc,
    )
    return rows

# ---- READ: InfluxQL raw (관리용) ----
class RawQuery(BaseModel):
    q: str

@router.post("/query")
def query_raw(body: RawQuery):
    return influx.query_raw(body.q)

# ---- WRITE: JSON 포맷 ----
@router.post("/write/json")
def write_json(body: WriteBody):
    pts: List[Dict] = []
    default_m = body.default_measurement or settings.influx_measurement
    for p in body.points:
        pts.append({
            "measurement": p.measurement or default_m,
            "tags": p.tags or {},
            "fields": p.fields,
            **({"time": p.time} if p.time is not None else {}),
        })
    n = influx.write_json(pts)
    return {"written": n}

# ---- WRITE: Line Protocol (text/plain) ----
@router.post("/write/line", summary="Line protocol")
def write_line(lines: str = Body(..., media_type="text/plain")):
    n = influx.write_line(lines)
    return {"written": n}
