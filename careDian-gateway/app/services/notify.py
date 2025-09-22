from typing import Optional, Dict, Any
from app.services.ha_client import HAClient

async def ha_notify(service: str, title: str, message: str, data: Optional[Dict[str, Any]] = None):
    # Home Assistant notify.xxx 서비스 호출
    client = HAClient()
    payload = {"title": title, "message": message}
    if data: payload["data"] = data
    return await client.call_service("notify", service, payload)
