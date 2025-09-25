from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..fcm import send_multicast

router = APIRouter()

@router.post("/register")
def register_device(req: schemas.RegisterReq, db: Session = Depends(get_db)):
    # upsert 느낌으로 간단 처리
    token = db.query(models.DeviceToken).filter_by(token=req.token).first()
    if not token:
        token = models.DeviceToken(token=req.token, platform=req.platform)
        db.add(token)
        db.commit()
    return {"ok": True}

@router.post("/test-notify")
def test_notify(db: Session = Depends(get_db)):
    tokens = [t.token for t in db.query(models.DeviceToken).all()]
    send_multicast(
        title="테스트 알림",
        body="CareDian 서버에서 보낸 테스트 푸시",
        data={"type": "test"},
        tokens=tokens,
    )
    return {"ok": True, "tokens": len(tokens)}
