"""
모듈: core/rate_limit.py
역할:
  - (1) 단순 슬라이딩 윈도우 레이트리미터 (in-memory)
  - (2) 디바이스별 쿨다운 기반 알림 억제 유틸리티

설계 특징:
  • 프로세스 메모리(deque, dict) 기반 → 멀티 프로세스/멀티 인스턴스(예: gunicorn 워커) 간에는 **상태가 공유되지 않음**.
  • 각 identity(예: device_id, IP, 토큰 등) 별로 타임스탬프 큐를 유지하며 슬라이딩 윈도우 방식으로 허용 여부를 판단.
  • should_alert()는 마지막 알림 시각을 기록하여 일정 시간(cooldown) 내 중복 알림을 억제.

주의:
  - 분산 환경(여러 컨테이너/호스트)에서는 Redis 등 외부 저장소로의 확장이 필요.
  - 현재 구현은 GC(오래된 identity 제거) 정책이 없어 장시간 런 시 메모리 증가 가능 → 주기적 청소 로직을 상위에서 고려.

사용 예시:
  >>> limiter = MemoryRateLimiter(RateConfig(limit=10, window_sec=60))
  >>> allowed, remaining, reset_in = limiter.allow("esp32-01")
  >>> if should_alert("esp32-01", cooldown_sec=300):
  ...     send_alert(...)
"""

from __future__ import annotations
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, Optional, Tuple


@dataclass
class RateConfig:
    """레이트리미터 설정 값

    Attributes:
        limit: 윈도우 내 허용 가능한 최대 호출 수.
        window_sec: 슬라이딩 윈도우 길이(초). window_sec 동안의 호출 수가 limit를 넘으면 차단.
    """
    limit: int = 60
    window_sec: int = 60


class MemoryRateLimiter:
    """간단한 메모리 기반 슬라이딩 윈도우 레이트리미터.

    구현 개요:
      - identity(문자열 키)별로 호출 시각(epoch seconds)을 기록하는 deque를 보유.
      - allow() 호출 시 현재 시각 기준으로 윈도우 밖(현재-윈도우길이 이전)의 항목을 큐 앞에서 제거.
      - 큐 길이가 limit 미만이면 허용(True)하고 현재 시각을 push; 아니면 거부(False).

    제약/주의:
      - 스레드 세이프티: CPython의 GIL로 기본 동작은 안전한 편이나, 멀티프로세스에선 상태가 분리됨.
      - 장시간 서비스 시 identity 수가 증가할 수 있음 → 상위에서 주기적 cleanup 전략 고려.
    """

    def __init__(self, cfg: RateConfig):
        self.cfg = cfg
        # identity -> 최근 호출 타임스탬프 큐
        self._buckets: Dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, identity: str, now: Optional[float] = None) -> Tuple[bool, int, int]:
        """호출 허용 여부를 판단.

        Args:
            identity: 레이트리밋 키(예: device_id, 사용자 ID, IP 등)
            now: 현재 시각(epoch seconds). None이면 time.time() 사용.

        Returns:
            (allowed, remaining, reset_in)
              - allowed(bool): 허용 여부
              - remaining(int): 현재 윈도우에서 남은 허용 횟수
              - reset_in(int): 윈도우가 초기화(첫 이벤트가 윈도우 밖으로 사라짐)되기까지 남은 초

        동작 상세:
          1) 현재 시각(now) 기준 윈도우 시작 시각 계산: window_start = now - window_sec
          2) deque 앞단에서 window_start 이하(윈도우 밖) 이벤트를 제거
          3) 남은 이벤트 개수가 limit 미만이면 허용하고 now를 push, 남은 횟수/리셋 시간 계산
          4) limit 이상이면 거부하고 리셋 시간(가장 오래된 이벤트가 윈도우 밖으로 나갈 때까지의 초)을 계산
        """
        now = now if now is not None else time.time()
        window_start = now - self.cfg.window_sec
        dq = self._buckets[identity]

        # (정리) 윈도우 밖의 오래된 타임스탬프 제거
        while dq and dq[0] <= window_start:
            dq.popleft()

        if len(dq) < self.cfg.limit:
            # 허용: 현재 호출 시각을 기록
            dq.append(now)
            remaining = self.cfg.limit - len(dq)
            # reset_in: 첫 이벤트가 윈도우 밖으로 밀려나기까지 남은 시간
            reset_in = int(self.cfg.window_sec - (now - (dq[0] if dq else now)))
            return True, remaining, reset_in

        # 거부: 남은 횟수는 0, 리셋까지의 시간은 맨 앞 타임스탬프 기준으로 계산
        remaining = 0
        reset_in = int(self.cfg.window_sec - (now - dq[0])) if dq else self.cfg.window_sec
        return False, remaining, reset_in


# -----------------------------------------------------------------------------
# 단순 쿨다운 기반 알림 억제: should_alert
#   - 디바이스별 마지막 알림 송신 시각을 저장하고, cooldown_sec 이 경과했을 때만 True 반환.
#   - 레이트리밋과 달리 복잡한 윈도우 계산 없이 마지막 시각만 본다.
# -----------------------------------------------------------------------------
_last_alert_ts: Dict[str, float] = defaultdict(float)


def should_alert(device_id: str, cooldown_sec: int = 60) -> bool:
    """디바이스별 쿨다운 로직.

    Args:
        device_id: 알림 식별 키(일반적으로 센서/디바이스 ID)
        cooldown_sec: 마지막 알림 이후 다시 알림을 허용하기까지의 최소 대기 시간(초)

    Returns:
        True  - 마지막 알림으로부터 cooldown_sec 이상 지남(이번에 알림 허용)
        False - 아직 쿨다운 진행 중(이번 알림 억제)

    주의:
      - 프로세스 메모리 기반이므로 워커 간 공유되지 않음.
      - 장시간 서비스 시 상태 초기화가 필요할 수 있음.
    """
    now = time.time()
    # 마지막 알림 시각과 현재 시각 차이가 쿨다운보다 크거나 같으면 허용
    if now - _last_alert_ts[device_id] >= cooldown_sec:
        _last_alert_ts[device_id] = now  # 이번 호출을 마지막 알림 시각으로 갱신
        return True
    return False
