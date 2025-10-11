from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.rate_limit import should_alert
from app.services.ha_notify import send_fall_alert
from app.services import influx_v1 as influx


router = APIRouter(prefix="/events", tags=["fall"])

class FallEvent(BaseModel):
    device_id: str = Field(..., description="ESP32 또는 센서 디바이스 ID")
    presence: int = Field(..., description="사람 존재 여부 (0: 없음, 1: 있음)")
    movement: int = Field(..., description="움직임 상태 (0: 없음, 1: 정지, 2: 활동)")
    moving_range: int = Field(..., description="움직임 거리/범위")
    fall_state: int = Field(..., description="낙상 상태 (0: 정상, 1: 낙상 감지)")
    dwell_state: int = Field(..., description="정지 상태 (0: 없음, 1: 장시간 정지)")
    ts: int = Field(..., description="타임스탬프 (초 단위)")
    location: str = Field("livingroom", description="센서 위치 (기본: 거실)")
    predicted_prob: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="(선택) LSTM 예측 낙상 확률"
    )
    meta: Optional[Dict[str, Any]] = Field(
        default=None,
        description="(선택) 추가 메타 정보"
    )

@router.post("/fall")
async def receive_fall(ev: FallEvent) -> Dict[str, Any]:
    # 1) Influx 기록(옵션)
    try:
        influx.write_point(
            "fall_event",
            tags={"device_id": ev.camera_id, "location": ev.location or "home"},
            fields={"prob": ev.prob},
            ts_ns=ev.timestamp_ns,
        )
    except Exception as e:
        pass

    # 2) 알림 발송(FCM + persistent)
    if int(ev.fall_state) == 1 and should_alert(ev.device_id, cooldown_sec=300):
        notify_result = await send_fall_alert(
            device_id=ev.device_id,
            title="🚨 낙상 감지",
            message=f"[{ev.location or 'home'}] {ev.device_id}에서 낙상이 감지되었습니다.)",
            location=ev.location,
            moving_range=ev.moving_range,
            dwell_state=ev.dwell_state,
            ts=ev.ts,
        )
    notify_result = None

    if notify_result:
        if notify_result["mobile"] >= 400 and notify_result["persist"] >= 400:
            raise HTTPException(status_code=502, detail="HA notify failed")

    return {"ok": True, "fall_state": ev.fall_state}
