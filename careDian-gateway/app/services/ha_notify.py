from typing import Optional, Dict, Any
import httpx
from app.core.config import settings

async def _call_notify(service: str, payload: Dict[str, Any]) -> int:
    url = f"{settings.ha_base_url.rstrip('/')}/api/services/{service.replace('.','/')}"
    headers = {
        "Authorization": f"Bearer {settings.ha_token}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        r = await client.post(url, headers=headers, json=payload)
        return r.status_code

async def send_fall_alert(
    title: str,
    message: str,
    *,
    location: Optional[str] = None,
    image_url: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """FCM(모바일앱) + persistent_notification 둘 다 전송."""
    loc = location or settings.location_default

    # 1) 모바일(Firebase via HA 모바일앱 notify)
    mobile_payload = {
        "title": title,
        "message": message,
        "data": {
            "tag": "fall_alert",
            "channel": "alarm_stream",
            "clickAction": "/lovelace/home",
            "actions": [
                {"action": "URI", "title": "열기", "uri": f"/lovelace/home"},
            ],
            "image": image_url,
            "location": loc,
        },
    }
    if extra:
        mobile_payload["data"].update(extra)
    status_mobile = await _call_notify(settings.ha_notify_mobile, mobile_payload)

    # 2) 고정 알림
    persist_payload = {
        "message": message,
        "title": title,
        "notification_id": "fall_alert",
    }
    status_persist = await _call_notify(settings.ha_notify_persist, persist_payload)

    return {"mobile": status_mobile, "persist": status_persist}
