"""
모듈: services/ha_notify.py
역할:
  - Home Assistant(HA) REST API를 사용해 모바일앱 푸시(notify.mobile_app_* 등)와
    지속 알림(persistent_notification.create)을 전송하는 헬퍼.

구성:
  • _call_notify(service, payload) : HA 서비스 호출 공통 함수
  • send_fall_alert(...)          : 낙상 알림 패키징 + 대상 notify 서비스 탐색/필터링 + 전송

의존 설정(settings):
  - ha_base_url            : HA 베이스 URL (예: http://homeassistant.local:8123)
  - ha_token               : Long-Lived Access Token
  - request_timeout        : 외부 HTTP 타임아웃(초)
  - ha_notify_mobile       : 모바일앱 notify 서비스 강제 지정 시 사용(폴백)
  - ha_notify_persist      : 지속 알림 서비스 경로 (기본 persistent_notification.create)
  - location_default       : location 기본값

주의/운영:
  - 네트워크/HTTP 오류는 로그 출력 후 가능한 폴백 경로로 진행
  - 특정 기기 제외(exclude_devices) 목록은 운영 환경에 맞게 유지보수 필요
"""

from typing import Optional, Dict, Any
import httpx

from app.core.config import settings


async def _call_notify(service: str, payload: Dict[str, Any]) -> int:
    """HA REST API로 임의의 notify 서비스 호출

    Args:
      service: 'domain.service' 형태(예: 'notify.mobile_app_pixel_8' 또는 'persistent_notification.create')
      payload: 서비스별 요구 페이로드(JSON)

    Returns:
      int: HTTP 상태코드 (200계열 성공)

    동작:
      - service를 'domain/service'로 변환하여 /api/services/<domain>/<service> 로 POST
      - 실패 시 상태코드를 그대로 반환하며, 경고 로그 출력
    """
    # /api/services/<domain>/<service> 형태의 호출 URL 구성
    url = f"{settings.ha_base_url.rstrip('/')}/api/services/{service.replace('.', '/')}"
    headers = {
        "Authorization": f"Bearer {settings.ha_token}",
        "Content-Type": "application/json",
    }

    # httpx AsyncClient로 POST 호출 (타임아웃: settings.request_timeout)
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        r = await client.post(url, headers=headers, json=payload)
        print(f"[HA_NOTIFY] POST {url} → {r.status_code}")
        if r.status_code >= 400:
            print("⚠️ Home Assistant notify failed:", r.text)
        return r.status_code


async def send_fall_alert(
    *,
    device_id: str,
    title: str,
    message: str,
    location: str = "home",
    pred_prob: Optional[float] = None,
    moving_range: Optional[int] = None,
    dwell_state: Optional[int] = None,
    fall_state: Optional[int] = None,
    ts: Optional[int] = None,
) -> Dict[str, Any]:
    """낙상 알림을 모바일앱 + 지속 알림으로 전송

    Args:
      device_id    : 센서/기기 식별자
      title, message: 알림 제목/메시지
      location     : 위치(없으면 settings.location_default 사용)
      pred_prob    : (선택) 모델 예측 확률
      moving_range : (선택) 이동 범위 지표
      dwell_state  : (선택) 장시간 정지 상태 플래그
      fall_state   : (선택) 센서 낙상 판정(0/1)
      ts           : (선택) 이벤트 시각(epoch seconds)

    Returns:
      Dict[str, Any]: 서비스명→HTTP 상태코드 매핑 결과

    동작:
      1) 공통 payload(title/message/data)를 구성
      2) HA /api/services 로부터 notify 도메인의 mobile_app_* 서비스들을 조회
      3) exclude 목록을 적용해 필터링
      4) 대상 서비스가 없으면 settings.ha_notify_mobile 로 폴백 호출
      5) 항상 persistent_notification.create 를 추가로 호출
    """
    # location 값 보정(없으면 설정 기본값 사용)
    loc = location or settings.location_default

    # 모바일앱 푸시에 사용할 기본 payload 구성
    base_payload = {
        "message": message,
        "title": title,
        "data": {
            "tag": "fall_alert",            # 동일 태그로 알림 스택 관리 가능
            "location": loc,
            "device_id": device_id,
            "pred_prob": pred_prob,
            "moving_range": moving_range,
            "dwell_state": dwell_state,
            "fall_state": fall_state,
            "ts": ts,
        },
    }

    base_url = settings.ha_base_url.rstrip("/")
    headers = {
        "Authorization": f"Bearer {settings.ha_token}",
        "Content-Type": "application/json",
    }

    results: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # 1) 대상 notify 서비스 탐색: /api/services 에서 domain==notify 항목 조회
    # ------------------------------------------------------------------
    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            r = await client.get(f"{base_url}/api/services", headers=headers)
            r.raise_for_status()  # 상태코드 4xx/5xx 시 예외 발생 → except로 이동
            data = r.json()
            notify_services = [s for s in data if s["domain"] == "notify"]
            if notify_services:
                # 'mobile_app_*' 만 선택하여 'notify.<name>' 형태로 재조립
                all_notify = [
                    f"notify.{name}"
                    for name in notify_services[0]["services"].keys()
                    if name.startswith("mobile_app_")
                ]
            else:
                all_notify = []
    except Exception as e:
        # 조회 실패 시 폴백(지속 알림은 어쨌든 시도)
        print(f"⚠️ Failed to fetch notify services: {e}")
        all_notify = []

    # ------------------------------------------------------------------
    # 2) 운영 중 제외할 기기 필터링 (예: 테스트 단말 제외)
    # ------------------------------------------------------------------
    exclude_devices = {
        "mobile_app_paul_pad_pro_12_7",
        "mobile_app_paul_fold7",
    }

    filtered_notify = [
        service for service in all_notify
        if not any(excluded in service for excluded in exclude_devices)
    ]

    # ------------------------------------------------------------------
    # 3) 모바일앱 푸시 전송 (없으면 폴백 서비스 사용)
    # ------------------------------------------------------------------
    if not filtered_notify:
        print(f"⚠️ No valid mobile_app_* found, fallback to {settings.ha_notify_mobile}")
        status_mobile = await _call_notify(settings.ha_notify_mobile, base_payload)
        results[settings.ha_notify_mobile] = status_mobile
    else:
        for service in filtered_notify:
            status_code = await _call_notify(service, base_payload)
            results[service] = status_code

    # ------------------------------------------------------------------
    # 4) 지속 알림(persistent_notification.create) 추가 전송
    # ------------------------------------------------------------------
    persist_payload = {"title": title, "message": message}
    status_persist = await _call_notify(settings.ha_notify_persist, persist_payload)
    results["persistent_notification"] = status_persist

    return results
