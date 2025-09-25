import time
import requests
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from app.rate_limit import should_alert

app = FastAPI(title="CareDian Fall Alert")

HA_URL = "https://caredian.gleeeze.com/api/services/notify/mobile_app_gimyeji_iphone" # 홈어시스턴트 -> 개발자도구 -> 서비스 -> notify.로 시작하는 서비스 목록에서 확인 가능.. 
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzMjNkNDQzMzI3YzQ0ZjQyYTFkNzI2Nzc4ZTMwYTRjMSIsImlhdCI6MTc1ODc5MDE1MSwiZXhwIjoyMDc0MTUwMTUxfQ.ZFbkRP-uq-xpvDAFyzahVRCqyyWDGTllxc53RBcl0vs"  #프로필 -> long-lived access tokens 메뉴에서 확인 -> create token 눌러서 토큰 생성

"""def send_ha_alert(title: str, message: str):
    print(f"[TEST ALERT] Title: {title} | Message: {message}")
"""

def send_ha_alert(title: str, message: str):
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "title": title,
        "message": message
    }
    try:
        r = requests.post(HA_URL, headers=headers, json=payload, timeout=5)
        print("HA Response:", r.status_code, r.text)
    except Exception as e:
        print("HA Error:", e)



# ---------- Pydantic 모델 ----------
class AlertReq(BaseModel):
    user_id: str
    score: float
    sensor_fall: int = 0
    ts: float | None = None

class EventIn(BaseModel):
    device_id: str
    presence: int
    movement: int
    moving_range: int
    fall_state: int
    dwell_state: int
    ts: int

# ---------- 엔드포인트 ----------
@app.get("/healthz")
def health():
    """서버 상태 확인"""
    return {"ok": True, "time": time.time()}


@app.post("/events")
def events(ev: EventIn, tasks: BackgroundTasks):
    print("Received Event:", ev.dict())

    if ev.fall_state == 1 and should_alert(ev.device_id, cooldown_sec=300):
        title = "🚨 낙상 감지"
        body = f"{ev.device_id} 에서 낙상 감지 (presence={ev.presence}, movement={ev.movement})"
        print("🚨 Sending HA alert:", body)
        tasks.add_task(send_ha_alert, title, body)

    return {"ok": True}