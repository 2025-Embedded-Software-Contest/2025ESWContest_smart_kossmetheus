from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.ha_notify import send_fall_alert
from app.services import influx

router = APIRouter(prefix="/events", tags=["fall"])

class FallEvent(BaseModel):
    camera_id: str = Field(..., description="카메라/디바이스 ID")
    prob: float = Field(..., ge=0.0, le=1.0, description="낙상 확률(0~1)")
    timestamp_ns: Optional[int] = Field(None, description="나노초 타임스탬프(옵션)")
    location: Optional[str] = Field(None, description="장소명(예: home)")
    image_url: Optional[str] = Field(None, description="스냅샷 URL(옵션)")
    meta: Optional[Dict[str, Any]] = Field(default=None, description="추가 메타")

@router.post("/fall")
async def receive_fall(ev: FallEvent) -> Dict[str, Any]:
    # 1) Influx 기록(옵션)
    try:
        influx.write_point(
            "fall_event",
            tags={"camera_id": ev.camera_id, "location": ev.location or "home"},
            fields={"prob": ev.prob},
            ts_ns=ev.timestamp_ns,
        )
    except Exception as e:
        # 기록 실패는 알림을 막지 않음
        pass

    # 2) 알림 발송(FCM + persistent)
    title = "낙상 감지"
    msg = f"[{ev.location or 'home'}] {ev.camera_id}에서 낙상이 감지되었습니다. (p={ev.prob:.2f})"
    notify_result = await send_fall_alert(
        title=title,
        message=msg,
        location=ev.location,
        image_url=ev.image_url,
        extra={"camera_id": ev.camera_id, "prob": ev.prob},
    )

    if notify_result["mobile"] >= 400 and notify_result["persist"] >= 400:
        raise HTTPException(502, detail="HA notify failed")

    return {"ok": True, "notify": notify_result}
