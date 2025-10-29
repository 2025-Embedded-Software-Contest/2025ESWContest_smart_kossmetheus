"""
모듈: api/ha.py
기능: Home Assistant(HA)에 등록된 모바일 앱 알림 대상(notify.mobile_app_*)을 조회하는 읽기 전용 API 제공

요약 동작:
  1) HA의 /api/services 엔드포인트를 호출하여 전체 서비스 목록을 가져온다.
  2) domain == "notify" 인 항목을 찾는다.
  3) 그 안의 service 명 중 접두사가 "mobile_app_" 인 것만 추려서 리스트로 반환한다.

입출력:
  - 입력(쿼리/바디 없음). 내부적으로 settings.ha_base_url, settings.ha_token 사용
  - 출력: {"mobile_notify_devices": ["mobile_app_..."]}

보안:
  - HA Long-Lived Access Token을 Authorization: Bearer 헤더로 전송

에러 처리:
  - HA가 200 이외 코드 반환 시, 해당 상태코드로 FastAPI HTTPException 발생(detail=r.text)
  - 네트워크/타임아웃/파싱 등의 예외는 500으로 래핑

주의:
  - httpx.HTTPStatusError는 일반적으로 r.raise_for_status() 호출 시 발생한다.
    (현재 구현은 status 코드 직접 검사 → raise_for_status() 미사용)
"""

from fastapi import APIRouter, HTTPException
import httpx

from app.core.config import settings

# 라우터: /ha 프리픽스, 문서 태그 "homeassistant"
router = APIRouter(prefix="/ha", tags=["homeassistant"])


@router.get("/notify_devices")
async def list_notify_devices():
    """
    Home Assistant에 등록된 notify.mobile_app_* 서비스 목록 조회 API

    반환 예시:
    {
      "mobile_notify_devices": [
        "mobile_app_pixel_8",
        "mobile_app_ipad"
      ]
    }
    """
    # 1) 호출 URL 구성: 베이스 URL의 트레일링 슬래시를 제거하고 /api/services 를 붙인다.
    url = f"{settings.ha_base_url.rstrip('/')}/api/services"

    # 2) 인증 헤더: HA Long-Lived Token을 Bearer 토큰으로 전송
    headers = {"Authorization": f"Bearer {settings.ha_token}"}

    try:
        # 3) 비동기 HTTP 클라이언트로 호출 (타임아웃 5초)
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, headers=headers)

            # 4) 상태코드 검사: 200이 아니면 그대로 전달(패스스루)하는 HTTP 예외 발생
            if r.status_code != 200:
                raise HTTPException(status_code=r.status_code, detail=r.text)

            # 5) JSON 파싱: HA는 도메인/서비스 구조의 리스트를 반환한다.
            #    예: [{"domain":"notify","services": {"mobile_app_x":{...}, ...}}, ...]
            services = r.json()

            # 6) notify 도메인 필터링: domain == "notify" 인 항목만 추출
            notify_services = [s for s in services if s["domain"] == "notify"]

            # 7) 모바일앱 서비스만 추출: 서비스명(keys) 중 접두사 "mobile_app_" 인 것만 수집
            mobile_services = []
            if notify_services:
                mobile_services = [
                    srv for srv in notify_services[0]["services"].keys()
                    if srv.startswith("mobile_app_")
                ]

            # 8) 호출자가 바로 사용 가능하도록 dict 형태로 감싸서 반환
            return {"mobile_notify_devices": mobile_services}

    # 참고: 현재 구현은 r.raise_for_status()를 호출하지 않아 아래 예외에 잘 도달하지 않는다.
    except httpx.HTTPStatusError as e:
        # httpx가 상태코드를 예외로 변환한 경우(raise_for_status 사용 시)
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    except Exception as e:
        # 네트워크/타임아웃/파싱 등 일반 예외 → 500으로 래핑
        raise HTTPException(status_code=500, detail=f"Failed to fetch HA devices: {e}")
