from __future__ import annotations
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, Optional, Tuple

@dataclass
class RateConfig:
    limit: int = 60
    window_sec: int = 60

class MemoryRateLimiter:
    def __init__(self, cfg: RateConfig):
        self.cfg = cfg
        self._buckets: Dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, identity: str, now: Optional[float] = None) -> Tuple[bool, int, int]:
        now = now if now is not None else time.time()
        window_start = now - self.cfg.window_sec
        dq = self._buckets[identity]
        while dq and dq[0] <= window_start:
            dq.popleft()
        if len(dq) < self.cfg.limit:
            dq.append(now)
            remaining = self.cfg.limit - len(dq)
            reset_in = int(self.cfg.window_sec - (now - (dq[0] if dq else now)))
            return True, remaining, reset_in
        remaining = 0
        reset_in = int(self.cfg.window_sec - (now - dq[0])) if dq else self.cfg.window_sec
        return False, remaining, reset_in


_last_alert_ts: Dict[str, float] = defaultdict(float)

def should_alert(device_id: str, cooldown_sec: int = 60) -> bool:
    now = time.time()
    if now - _last_alert_ts[device_id] >= cooldown_sec:
        _last_alert_ts[device_id] = now
        return True
    return False