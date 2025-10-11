from typing import Optional, Dict, Any
import httpx
from app.core.config import settings


async def _call_notify(service: str, payload: Dict[str, Any]) -> int:
    """HA REST API로 notify 서비스 호출"""
    url = f"{settings.ha_base_url.rstrip('/')}/api/services/{service.replace('.', '/')}"
    headers = {
        "Authorization": f"Bearer {settings.ha_token}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        r = await client.post(url, headers=headers, json=payload)
        print(f"[HA_NOTIFY] POST {url} → {r.status_code}")
        if r.status_code >= 400:
            print("⚠️ Home Assistant notify failed:", r.text)
        return r.status_code


async def send_fall_alert(
    *,
    device_id: str,
    title: str,
    message: str,
    location: str = "home",
    pred_prob: Optional[float] = None,
    moving_range: Optional[int] = None,
    dwell_state: Optional[int] = None,
    fall_state: Optional[int] = None,
    ts: Optional[int] = None,
) -> Dict[str, Any]:
    loc = location or settings.location_default

    mobile_payload = {
        "message": message,   
        "title": title,       
        "data": {
            "tag": "fall_alert",
            "location": loc,
            "device_id": device_id,
            "pred_prob": pred_prob,
            "moving_range": moving_range,
            "dwell_state": dwell_state,
            "fall_state": fall_state,
            "ts": ts,
        },
    }

    status_mobile = await _call_notify(settings.ha_notify_mobile, mobile_payload)
    persist_payload = {
        "title": title,
        "message": message,
        #"notification_id": "fall_alert",
    }

    status_persist = await _call_notify(settings.ha_notify_persist, persist_payload)

    return {"mobile": status_mobile, "persist": status_persist}
