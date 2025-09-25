from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas import EventIn
from .. import models
from ..fcm import send_multicast

router = APIRouter()

@router.post("/")
def receive_event(ev: EventIn, db: Session = Depends(get_db)):
    # (FCM 테스트 집중 버전: 토큰만 조회해서 바로 알림. 이벤트 DB 저장은 추후 확장)
    if ev.fall_state == 1:
        tokens = [t.token for t in db.query(models.DeviceToken).all()]
        send_multicast(
            title="긴급 알림: 낙상 감지",
            body=f"디바이스 {ev.device_id} 에서 낙상 발생",
            data={
                "device_id": ev.device_id,
                "presence": ev.presence,
                "movement": ev.movement,
                "moving_range": ev.moving_range,
                "fall_state": ev.fall_state,
                "dwell_state": ev.dwell_state,
                "ts": ev.ts,
            },
            tokens=tokens,
        )
    return {"ok": True}
