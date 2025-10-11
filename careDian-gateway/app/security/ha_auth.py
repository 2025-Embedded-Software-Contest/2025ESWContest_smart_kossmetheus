from fastapi import Depends, Header, HTTPException
import httpx
from app.core.config import settings

class HAUser(dict): pass

async def require_ha_user(authorization: str = Header(...)) -> HAUser:
    # Authorization: Bearer <HA_LONG_LIVED_TOKEN>
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = parts[1]
    # 토큰 검증: HA /api/config (200이면 유효)
    url = settings.ha_base_url.rstrip("/") + "/api/config"
    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_s) as c:
            r = await c.get(url, headers={"Authorization": f"Bearer {token}"})
    except Exception:
        raise HTTPException(status_code=502, detail="HA unreachable")

    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid HA token")

    info = r.json()  # {"location_name": "...", ...}
    return HAUser(info)
