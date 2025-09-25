#중복알림방지
import time
from collections import defaultdict

COOLDOWN = 60  # 초 단위

_last_alert_ts = defaultdict(float)

def can_alert(device_id: str) -> bool:
    now = time.time()
    if now - _last_alert_ts[device_id] >= COOLDOWN:
        _last_alert_ts[device_id] = now
        return True
    return False
