"""
모듈: security/api_key.py (내부 API Key 인증 디펜던시)

역할:
  - 내부/관리용 엔드포인트 보호를 위해 요청 헤더의 API 키를 검증한다.
  - 기대 헤더: `X-API-Key: <kid>.<secret>`
      * kid: 키 식별자 (settings.api_keys_json의 key)
      * secret: 해당 식별자에 매핑된 실제 비밀값
  - 검증 성공 시 호출자 식별자(kid)를 반환하여 핸들러에서 감사 로깅/권한 분기 등에 활용한다.

보안 포인트:
  - hmac.compare_digest() 사용으로 타이밍 공격 완화(상수 시간 비교).
  - 키 원문은 절대로 로그로 남기지 않는다(이 모듈은 예외 detail도 일반 메시지로 제한).
  - 키 저장소(settings.api_keys_json)는 .env/시크릿 매니저에서 주입하며, 깃 커밋 금지.

사용 예(두 방식 모두 가능):
  1) 종속성으로 전역 보호
     @router.get("/internal", dependencies=[Depends(api_key_required)])
     async def internal():
         return {"ok": True}

  2) 호출자 id 활용
     @router.get("/internal")
     async def internal(caller: str = Depends(api_key_required)):
         # caller == kid (예: "svc_ingestor")
         return {"caller": caller, "ok": True}
"""

import hmac
from fastapi import Header, HTTPException

from app.core.config import settings


def api_key_required(x_api_key: str = Header(None)) -> str:
    """요청 헤더의 `X-API-Key`를 검증하는 FastAPI 의존성.

    기대 형식: "<kid>.<secret>"
      - kid: settings.api_keys_json의 키(식별자)
      - secret: 실제 비밀 문자열

    반환:
      - 검증 성공 시: kid(호출자 식별자)
      - 실패 시: HTTPException(401)
    """
    # 1) 헤더 존재/형식 확인 — 구분자 '.' 없으면 무효한 형식
    if not x_api_key or "." not in x_api_key:
        # detail은 일반 메시지로만 노출(민감정보 노출 방지)
        raise HTTPException(status_code=401, detail="missing api key")

    # 2) kid와 제공된 비밀값 분리 ('.' 첫 번째 구분까지만 split)
    kid, provided = x_api_key.split(".", 1)

    # 3) 서버 측 등록 비밀 조회 (.env의 API_KEYS_JSON={"svc_ingestor":"****"} 형태)
    secret = settings.api_keys_json.get(kid)

    # 4) 안전한 비교 — hmac.compare_digest는 시간 기반 사이드채널 위험 완화
    if not secret or not hmac.compare_digest(secret, provided):
        raise HTTPException(status_code=401, detail="invalid api key")

    # 5) 검증 성공 — 호출자 식별자 반환(로깅/권한 분기 등에 사용)
    return kid  # caller id