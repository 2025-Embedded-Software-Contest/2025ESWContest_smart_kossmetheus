import time
from collections import defaultdict

_last_alert_ts = defaultdict(float)

def should_alert(user_id: str, cooldown_sec: int = 300) -> bool:
    """유저별 쿨다운 확인 (기본 5분)"""
    now = time.time()
    if now - _last_alert_ts[user_id] >= cooldown_sec:
        _last_alert_ts[user_id] = now
        return True
    return False
