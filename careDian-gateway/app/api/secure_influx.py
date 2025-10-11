from fastapi import APIRouter, Depends, Query
from app.security.ha_auth import require_ha_user, HAUser
from app.services import influx
from app.core.config import settings

router = APIRouter(prefix="/secure/influx", tags=["secure-influx"])

@router.get("/falls")
async def list_falls(
    hours: int = Query(24, ge=1, le=24*30),
    limit: int = Query(100, ge=1, le=5000),
    user: HAUser = Depends(require_ha_user),  # ← HA 로그인 필수
):
    rows = influx.select_range(
        measurement=settings.influx_measurement,
        start_ago=f"{hours}h",
        fields=None,
        tags=None,
        limit=limit,
        desc=True,
    )
    return {"user": user, "rows": rows}
