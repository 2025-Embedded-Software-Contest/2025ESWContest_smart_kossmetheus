"""
모듈: security/ha_auth.py (Home Assistant 토큰 검증 디펜던시)

목적:
  - 클라이언트가 제공한 Home Assistant Long-Lived Access Token을 검증하여
    보호된 엔드포인트에 대한 접근을 허용/차단한다.

핵심 동작:
  1) Swagger(또는 클라이언트)로부터 Authorization: Bearer <token> 추출
  2) HA의 /api/config 엔드포인트를 호출하여 200이면 유효 토큰으로 간주
  3) 유효 시 config JSON을 간단한 사용자 컨텍스트(HAUser)로 반환

보안/운영 메모:
  - 이 검증은 HA가 토큰을 수락하는지 여부만 확인한다(권한 범위/역할까지는 확인하지 않음).
  - settings.request_timeout으로 네트워크 타임아웃을 제어한다.
  - 멀티 호출 최적화를 위해 캐시(예: TTL 캐시) 도입 가능.

사용 예:
  @router.get("/admin", dependencies=[Depends(require_ha_user)])
  async def admin_area(): ...

  @router.get("/me")
  async def me(ha: HAUser = Depends(require_ha_user)):
      return {"ha": ha}
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx

from app.core.config import settings


# Bearer 토큰 스킴 선언
#  - auto_error=True 이므로 토큰이 없거나 형식이 틀리면 FastAPI가 자동으로 401 처리 시도
bearer = HTTPBearer(auto_error=True)


class HAUser(dict):
    """Home Assistant /api/config 응답을 담는 간단한 컨테이너.
    - dict를 상속하여 필요 시 키 접근을 지원한다."""
    pass


async def require_ha_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
) -> HAUser:
    """HA Long‑Lived Token을 검증하는 FastAPI 의존성.

    입력:
      - Authorization: Bearer <HA_LONG_LIVED_TOKEN>
        (Swagger UI에서는 "Authorize"에 토큰만 입력하면 "Bearer " 접두사는 자동으로 붙음)

    처리:
      1) 토큰 누락 시 401
      2) {HA_BASE_URL}/api/config 로 GET 호출
      3) 200 이외면 401(잘못된 토큰)로 간주, 네트워크 오류는 502로 변환
      4) 200이면 응답 JSON을 HAUser로 감싸 반환
    """
    # 1) Swagger 등에서 전달된 Bearer 토큰 문자열 추출
    token = creds.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Missing HA token")

    # 2) 검증용 엔드포인트 구성: /api/config
    url = settings.ha_base_url.rstrip("/") + "/api/config"

    try:
        # 3) HTTP 호출: 타임아웃은 settings.request_timeout 사용
        async with httpx.AsyncClient(timeout=settings.request_timeout) as c:
            r = await c.get(url, headers={"Authorization": f"Bearer {token}"})
    except Exception:
        # 네트워크/타임아웃/해결 불가 등 → 게이트웨이 관점에서 상류 시스템 불가
        raise HTTPException(status_code=502, detail="HA unreachable")

    # 4) 상태코드 확인: 200 외에는 인증 실패로 간주
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid HA token")

    # 5) 유효: /api/config JSON을 그대로 컨텍스트로 제공
    info = r.json()  # 예: {"location_name": "Home", ...}
    return HAUser(info)
