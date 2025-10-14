import httpx
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.rate_limit import should_alert
from app.services.ha_notify import send_fall_alert
from app.services import influx_v1 as influx
from app.core.config import settings  

router = APIRouter(prefix="/events", tags=["fall"])

async def get_notify_device() -> Optional[str]:
    """Home Assistant에서 notify.mobile_app_* 서비스 중 첫 번째를 반환"""
    url = f"{settings.ha_base_url.rstrip('/')}/api/services"
    headers = {"Authorization": f"Bearer {settings.ha_token}"}

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, headers=headers)
            if r.status_code != 200:
                print(f"⚠️ Failed to fetch notify devices: {r.status_code}")
                return None

            data = r.json()
            notify_services = [s for s in data if s["domain"] == "notify"]
            if not notify_services:
                return None

            for name in notify_services[0]["services"].keys():
                if name.startswith("mobile_app_"):
                    return f"notify.{name}"  
    except Exception as e:
        print(f"⚠️ Error fetching HA devices: {e}")
        return None
    

class FallEvent(BaseModel):
    device_id: str = Field(..., description="ESP32 또는 센서 디바이스 ID")
    presence: int = Field(..., description="사람 존재 여부 (0: 없음, 1: 있음)")
    movement: int = Field(..., description="움직임 상태 (0: 없음, 1: 정지, 2: 활동)")
    moving_range: int = Field(..., description="움직임 거리/범위")
    fall_state: int = Field(..., description="낙상 상태 (0: 정상, 1: 낙상 감지)")
    dwell_state: int = Field(..., description="정지 상태 (0: 없음, 1: 장시간 정지)")
    ts: int = Field(..., description="타임스탬프 (초 단위)")
    location: str = Field("거실", description="센서 위치 (기본: 거실)")
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

    notify_result = None

    # 2) 알림 발송(FCM + persistent)
    if int(ev.fall_state) == 1 and should_alert(ev.device_id, cooldown_sec=300):
        ha_device = await get_notify_device()
        if not ha_device:
            raise HTTPException(status_code=500, detail="No HA mobile notify device found")

        print(f"🚨 Sending fall alert to {ha_device}")

        notify_result = await send_fall_alert(
            device_id=ev.device_id,
            title="🚨 낙상 감지",
            message=f"{ev.location or 'home'}에서 낙상이 감지되었습니다.",
            location=ev.location,
            moving_range=ev.moving_range,
            dwell_state=ev.dwell_state,
            ts=ev.ts,
        )
        

    if notify_result:
        if any(code >= 400 for code in notify_result.values() if isinstance(code, int)):
            raise HTTPException(status_code=502, detail=f"HA notify failed: {notify_result}")

    return {"ok": True, "fall_state": ev.fall_state}
  