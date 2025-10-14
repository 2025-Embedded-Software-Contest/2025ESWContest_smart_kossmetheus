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

    base_payload = {
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

    base_url = settings.ha_base_url.rstrip("/")
    headers = {
        "Authorization": f"Bearer {settings.ha_token}",
        "Content-Type": "application/json",
    }

    results: Dict[str, Any] = {}

    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            r = await client.get(f"{base_url}/api/services", headers=headers)
            r.raise_for_status()
            data = r.json()
            notify_services = [s for s in data if s["domain"] == "notify"]
            if notify_services:
                all_notify = [
                    f"notify.{name}"
                    for name in notify_services[0]["services"].keys()
                    if name.startswith("mobile_app_")
                ]
            else:
                all_notify = []
    except Exception as e:
        print(f"⚠️ Failed to fetch notify services: {e}")
        all_notify = []

    if not all_notify:
        print(f"⚠️ No mobile_app_* found, fallback to {settings.ha_notify_mobile}")
        status_mobile = await _call_notify(settings.ha_notify_mobile, base_payload)
        results[settings.ha_notify_mobile] = status_mobile
    else:
        for service in all_notify:
            status_code = await _call_notify(service, base_payload)
            results[service] = status_code

    persist_payload = {"title": title, "message": message}
    status_persist = await _call_notify(settings.ha_notify_persist, persist_payload)
    results["persistent_notification"] = status_persist

    return results
