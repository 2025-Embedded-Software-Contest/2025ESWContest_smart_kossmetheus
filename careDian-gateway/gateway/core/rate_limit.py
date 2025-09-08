from __future__ import annotations # 타입 힌트 평가 X, 문자열로 저장
import time # 시간 모듈
from collections import defaultdict, deque # 컨테이너 데이터형
from dataclasses import dataclass # 데이터 클래스
from typing import Deque, Dict, Optional, Tuple # 타입 힌트

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