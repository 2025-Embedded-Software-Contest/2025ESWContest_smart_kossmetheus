from fastapi import APIRouter, HTTPException, status

from app.models.alerts import FallAlert
from app.services.notify import ha_notify


router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("/fall")
async def fall(alert: FallAlert):
    # FCM + HA notify를 둘 다 보내려면 여기서 FCMClient 사용해도 됨
    if alert.location != "home":
        # 요구사항: location은 "home"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="location must be 'home'")
    # Home Assistant notify.<service_name> 예: mobile_app_xxx
    # 운영에 맞게 service 이름만 바꿔 주세요.
    ha_res = await ha_notify(service="mobile_app_phone", title="Fall detected", message=f"{alert.user_id} - {alert.severity}", data=alert.meta)
    return {"ok": True, "ha": ha_res}
