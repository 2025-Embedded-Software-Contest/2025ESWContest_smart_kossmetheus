import httpx
import asyncio
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.rate_limit import should_alert
from app.services.ha_notify import send_fall_alert
from app.services import influx_v1 as influx
from app.core.config import settings  
from app.services.influx_v1 import InfluxServiceV1

influx = InfluxServiceV1(
    url=settings.influx_url,
    database=settings.influx_db,
    username=settings.influx_username,
    password=settings.influx_password
)


router = APIRouter(prefix="/events", tags=["fall"])

async def get_notify_device() -> Optional[str]:
    """Home Assistant에서 notify.mobile_app_* 서비스 중 첫 번째를 반환"""
    url = f"{settings.ha_base_url.rstrip('/')}/api/services"
    headers = {"Authorization": f"Bearer {settings.ha_token}"}

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, headers=headers)
            if r.status_code != 200:
                print(f"Failed to fetch notify devices: {r.status_code}")
                return None

            data = r.json()
            notify_services = [s for s in data if s["domain"] == "notify"]
            if not notify_services:
                return None

            for name in notify_services[0]["services"].keys():
                if name.startswith("mobile_app_"):
                    return f"notify.{name}"  
    except Exception as e:
        print(f"Error fetching HA devices: {e}")
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

async def check_post_fall_motion(ev: FallEvent):
    await asyncio.sleep(15)  # 30초 대기
    try:
        # 30초 후 Influx에서 최근 movement 데이터 가져오기
        query = f"""
        from(bucket: "{settings.influx_db}")
          |> range(start: -40s)
          |> filter(fn: (r) => r["_measurement"] == "fall_event")
          |> filter(fn: (r) => r["device_id"] == "{ev.device_id}")
          |> last()
        """
        # Influx v1 클라이언트가 있으면 직접 get_recent_movement 구현해도 OK
        last_data = influx.query_last_movement(ev.device_id) if hasattr(influx, "query_last_movement") else None
        movement_val = None

        if last_data:
            movement_val = last_data.get("movement", None)

        print(f"[CHECK] 30초 후 movement 상태: {movement_val}")

        if movement_val in (0,1) :
            print(f"🚨 [ALERT] {ev.device_id} - 30초간 움직임 없음, 추가 알림 전송")
            await send_fall_alert(
                device_id=ev.device_id,
                title="⚠️ 장시간 움직임 없음",
                message=f"{ev.location}에서 낙상 후 30초간 움직임이 없습니다.",
                location=ev.location,
                moving_range=ev.moving_range,
                dwell_state=ev.dwell_state,
                ts=ev.ts,
            )
        else:
            print(f"[INFO] 30초 내 움직임 감지됨 ({movement_val}), 추가 알림 생략")
    except Exception as e:
        print(f"[ERROR] post-fall motion check 실패: {e}")

async def record_fall_event(ev: FallEvent) -> bool:
    """
    InfluxDB에 낙상 포인트 1건 기록.
    실패해도 예외는 올리지 않고 False 반환.
    """
    try:
        ts_ns = int(ev.ts) * 1_000_000_000 if getattr(ev, "ts", None) else None
        if getattr(ev, "timestamp_ns", None) is not None:
            ts_ns = int(ev.timestamp_ns)

        # predicted_prob/ prob 호환
        prob = float(getattr(ev, "prob", getattr(ev, "predicted_prob", 0.0)))

        ok = influx.write_point(
            measurement=settings.influx_measurement,           # ✅ env 사용
            tags={
                "device_id": ev.device_id,                     # ✅ camera_id → device_id
                "location": ev.location or settings.location_default,
            },
            fields={
                "prob": prob,
                "fall_state": int(ev.fall_state),
                "moving_range": int(getattr(ev, "moving_range", 0) or 0),
                "dwell_state": int(getattr(ev, "dwell_state", 0) or 0),
                "presence": int(getattr(ev, "presence", 0) or 0),
                "movement": int(getattr(ev, "movement", 0) or 0),
            },
            ts_ns=ts_ns,                                       # 없으면 서버시간 사용
            rp=getattr(settings, "influx_rp", None),           # 예: autogen
        )
        return bool(ok)
    except Exception:
        # log.exception("Influx write failed for fall_event")
        return False
    
@router.post("/fall")
async def receive_fall(ev: FallEvent) -> Dict[str, Any]:
    print("[RECEIVED] Fall event data:", ev.dict())  
    success = await record_fall_event(ev)

    notify_result = None

    if int(ev.fall_state) == 1 and should_alert(ev.device_id, cooldown_sec=300):
        ha_device = await get_notify_device()
        if not ha_device:
            print("No HA mobile notify device found")
            raise HTTPException(status_code=500, detail="No HA mobile notify device found")

        print(f"🚨 [ALERT] Sending fall alert to {ha_device}")

        notify_result = await send_fall_alert(
            device_id=ev.device_id,
            title="🚨 낙상 감지",
            message=f"{ev.location or 'home'}에서 낙상이 감지되었습니다.",
            location=ev.location,
            moving_range=ev.moving_range,
            dwell_state=ev.dwell_state,
            ts=ev.ts,
        )

        print("HA RESPONSE] =>", notify_result)
        #낙상 후 일정 시간 지나면 태스크 실행
        asyncio.create_task(check_post_fall_motion(ev))
    else:
        print(f"[INFO] No fall detected (fall_state={ev.fall_state})") 

    if notify_result:
        if any(code >= 400 for code in notify_result.values() if isinstance(code, int)):
            print("[HA ERROR] Notify failed:", notify_result)
            raise HTTPException(status_code=502, detail=f"HA notify failed: {notify_result}")
        
    return {"ok": True, "fall_state": ev.fall_state, "recorded": success, "notify_result": notify_result}
