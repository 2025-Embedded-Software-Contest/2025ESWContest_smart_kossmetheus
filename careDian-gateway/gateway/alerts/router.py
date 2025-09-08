import os # os 모듈
from fastapi import APIRouter, HTTPException # 라우터 모듈, 오류 처리

from gateway.alerts.models import FallAlert
from gateway.alerts.notifier_service import NotifierService
from gateway.core.settings import Settings


router = APIRouter(prefix="/v1/alerts", tags=["alerts"])

@router.post("/fall")
async def alert_fall(body: FallAlert):
    s = Settings.load()
    n = NotifierService(s)

    # 메시지
    title = "CareDian: 낙상 감지"
    who = f" 대상:{body.person_id}" if body.person_id else ""
    conf = f" (p={body.confidence:.2f})" if body.confidence is not None else ""
    msg = f"[낙상] location={body.location or 'home'}{who}{conf}"
    if body.note: msg += f" / {body.note}"
    payload = {
        "type":"fall","location": body.location or "home","person_id": body.person_id or "",
        "confidence": body.confidence or 0.0, "ts": body.ts or 0
    }
    delivered = {}
    # (원하면 FCM 환경변수도 Settings에 추가해 사용)

    try:
        fcm_res = await n.send_fcm(title, msg, payload,
                                   server_key=os.getenv("FCM_SERVER_KEY"),
                                   tokens=[t.strip() for t in (os.getenv("FCM_TOKENS","").split(",")) if t.strip()],
                                   topic=os.getenv("FCM_TOPIC"))
        if fcm_res: delivered["fcm"] = fcm_res
    except Exception as e:
        delivered["fcm_error"] = str(e)

    try:
        ha_res = await n.send_ha_notify(title, msg, payload)
        if ha_res: delivered["ha"] = ha_res
    except Exception as e:
        delivered["ha_error"] = str(e)

    if not delivered:
        raise HTTPException(500, "No notifier configured")
    
    return {"status":"ok", "delivered": delivered}
