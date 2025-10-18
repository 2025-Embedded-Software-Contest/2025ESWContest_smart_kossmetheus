from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx

from app.core.config import settings


bearer = HTTPBearer(auto_error=True)

class HAUser(dict): pass

async def require_ha_user(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> HAUser:
    # Authorization: Bearer <HA_LONG_LIVED_TOKEN>
    token = creds.credentials  # ← Swagger에선 토큰만 입력(“Bearer ” 자동)
    if not token:
        raise HTTPException(status_code=401, detail="Missing HA token")
    
    # 토큰 검증: HA /api/config (200이면 유효)
    url = settings.ha_base_url.rstrip("/") + "/api/config"
    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout) as c:
            r = await c.get(url, headers={"Authorization": f"Bearer {token}"})
    except Exception:
        raise HTTPException(status_code=502, detail="HA unreachable")

    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid HA token")

    info = r.json()  # {"location_name": "...", ...}
    return HAUser(info)
