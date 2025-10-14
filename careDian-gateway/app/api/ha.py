from fastapi import APIRouter, HTTPException
import httpx
from app.core.config import settings

router = APIRouter(prefix="/ha", tags=["homeassistant"])

@router.get("/notify_devices")
async def list_notify_devices():
    """
    Home Assistant에 등록된 notify.mobile_app_* 서비스 목록 조회
    """
    url = f"{settings.ha_base_url.rstrip('/')}/api/services"
    headers = {"Authorization": f"Bearer {settings.ha_token}"}

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, headers=headers)
            if r.status_code != 200:
                raise HTTPException(status_code=r.status_code, detail=r.text)

            services = r.json()
            notify_services = [
                s for s in services if s["domain"] == "notify"
            ]

            # notify.mobile_app_* 형태만 반환
            mobile_services = []
            if notify_services:
                mobile_services = [
                    srv for srv in notify_services[0]["services"].keys()
                    if srv.startswith("mobile_app_")
                ]

            return {"mobile_notify_devices": mobile_services}

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch HA devices: {e}")
