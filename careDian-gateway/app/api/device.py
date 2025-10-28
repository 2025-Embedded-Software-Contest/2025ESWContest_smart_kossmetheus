"""
모듈: /ha/notify_devices (Home Assistant 모바일 알림 대상 조회)
목적:
  - Home Assistant의 서비스 목록(/api/services)에서 'notify' 도메인을 찾고,
    모바일앱 푸시 서비스 이름들(notify.mobile_app_*)만 추출하여 반환한다.
입출력:
  - 입력: 없음(내부적으로 settings.ha_base_url, settings.ha_token 사용)
  - 출력: {"mobile_notify_devices": ["mobile_app_..."]}
의존성:
  - httpx(비동기 HTTP 클라이언트), FastAPI, pydantic 설정(app.core.config.settings)
보안:
  - Home Assistant Long-Lived Access Token을 Bearer 토큰으로 전송한다.
오류 처리:
  - HA가 200을 반환하지 않으면 해당 상태코드로 FastAPI HTTPException을 발생시킨다.
  - 네트워크/타임아웃/파싱 오류 등 기타 예외는 500으로 래핑한다.
주의:
  - httpx.HTTPStatusError는 r.raise_for_status()를 호출할 때 주로 발생한다.
    (현재 코드는 명시적으로 raise_for_status를 호출하지 않으므로 실질적으로는 도달하지 않을 수 있다.)
"""

from fastapi import APIRouter, HTTPException
import httpx

from app.core.config import settings

# 라우터: /ha 프리픽스, 문서 태그 "homeassistant"
router = APIRouter(prefix="/ha", tags=["homeassistant"])


@router.get("/notify_devices")
async def list_notify_devices():
    """
    Home Assistant에 등록된 notify.mobile_app_* 서비스 목록 조회

    반환 예시:
    {
      "mobile_notify_devices": [
        "mobile_app_pixel_8",
        "mobile_app_ipad",
        ...
      ]
    }
    """
    # 1) 요청 대상 URL 구성: 베이스 URL의 트레일링 슬래시를 제거하고 /api/services를 붙인다.
    url = f"{settings.ha_base_url.rstrip('/')}/api/services"

    # 2) 인증 헤더 구성: Home Assistant Long-Lived Token을 Bearer로 보낸다.
    headers = {"Authorization": f"Bearer {settings.ha_token}"}

    try:
        # 3) 비동기 HTTP GET 호출: 서비스 목록을 요청한다. (타임아웃 5초)
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, headers=headers)

            # 4) 상태코드 확인: 200이 아니면 r.text를 detail로 담아 그대로 예외를 올린다.
            if r.status_code != 200:
                raise HTTPException(status_code=r.status_code, detail=r.text)

            # 5) JSON 파싱: Home Assistant는 도메인/서비스 구조의 리스트를 반환한다.
            #    예: [{"domain":"notify","services":{ "mobile_app_phone":{...}, ... }}, ...]
            services = r.json()

            # 6) notify 도메인 필터링: domain가 "notify"인 엔트리만 추린다.
            notify_services = [s for s in services if s["domain"] == "notify"]

            # 7) 모바일앱 서비스만 추출: 서비스명(keys) 중 접두사가 'mobile_app_'인 항목만 수집한다.
            mobile_services = []
            if notify_services:
                mobile_services = [
                    srv for srv in notify_services[0]["services"].keys()
                    if srv.startswith("mobile_app_")
                ]

            # 8) 호출자가 바로 사용할 수 있도록 dict 형태로 래핑하여 반환한다.
            return {"mobile_notify_devices": mobile_services}

    # 9) httpx가 상태코드를 예외로 던진 경우 (raise_for_status 사용 시)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    # 10) 그 외 네트워크 오류/타임아웃/파싱 오류 등 일반 예외는 500으로 래핑한다.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch HA devices: {e}")
