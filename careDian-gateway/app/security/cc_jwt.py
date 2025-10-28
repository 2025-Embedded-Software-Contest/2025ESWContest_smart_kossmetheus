"""
모듈: security/cc_jwt.py — Client Credentials JWT 발급/검증

역할:
  - M2M(디바이스↔게이트웨이) 용 **Client-Credentials** 토큰 발급 엔드포인트 제공
  - RS256(private/public PEM)로 **서명/검증** 수행
  - FastAPI 의존성 `m2m_required(scopes)` 로 라우트 단위 **스코프 검사** 지원

설정 의존:
  - settings.cc_clients_json   : {client_id: client_secret}
  - settings.jwt_private_pem_path / settings.jwt_public_pem_path
  - settings.jwt_iss / settings.jwt_aud / settings.jwt_ttl_seconds

보안 포인트:
  - Basic 인증을 사용하여 /token 에서 client_id/secret 검증
  - JWT `aud`, `iss`, `exp`를 엄격 검증 (조세 `python-jose`)
  - scope 는 공백 구분 문자열로 저장/검사 → 최소권한 원칙
  - 키 파일은 프로세스 메모리에 캐시(_PRIV/_PUB)하여 I/O 최소화
"""

import os, time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from app.core.config import settings

# 라우터: /auth/cc 프리픽스, 문서 태그 "auth"
router = APIRouter(prefix="/auth/cc", tags=["auth"])

# 인증 스키마 준비
_basic = HTTPBasic()                 # /token 에서 Basic(client_id:client_secret)
_bearer = HTTPBearer(auto_error=True)  # 보호 라우트에서 Bearer 토큰 추출

# 키 캐시(프로세스 로컬)
_PRIV: bytes | None = None  # RS256 private key(서명용)
_PUB:  bytes | None = None  # RS256 public  key(검증용)


def _read_file(p: str) -> bytes:
    """바이너리 모드로 파일 전체를 읽어 바이트로 반환.
    - PEM 파일(private/public)을 메모리에 적재하는 데 사용."""
    with open(p, "rb") as f:
        return f.read()


def _ensure_keys():
    """서명/검증 키를 지연 로딩(lazy-load)하여 전역 캐시에 보관.

    예외:
      - 설정 누락/경로 없음 → RuntimeError
    """
    global _PRIV, _PUB
    if _PRIV and _PUB:
        return  # 이미 적재 완료
    
    # 개인키(private) 경로 검증 및 로드
    if settings.jwt_private_pem_path and os.path.exists(settings.jwt_private_pem_path):
        _PRIV = _read_file(settings.jwt_private_pem_path)
    else:
        # 운영 관점: 503(Service Unavailable)로 변환되어 클라이언트에 전달
        raise RuntimeError("No RS256 private key configured")

    # 공개키(public) 경로 검증 및 로드
    if settings.jwt_public_pem_path and os.path.exists(settings.jwt_public_pem_path):
        _PUB = _read_file(settings.jwt_public_pem_path)
    else:
        raise RuntimeError("No RS256 public key configured")


@router.post("/token")
def token(creds: HTTPBasicCredentials = Depends(_basic), scope: str = "events:fall:ingest"):
    """Client Credentials 토큰 발급 엔드포인트

    인증:
      - Authorization: Basic base64(client_id:client_secret)
      - settings.cc_clients_json 에 등록된 쌍만 허용

    파라미터:
      - scope: 문자열(공백 구분). 기본값은 "events:fall:ingest"

    응답(JSON):
      {
        "access_token": "<JWT>",
        "token_type": "Bearer",
        "expires_in": <초>
      }
    """
    # 1) 클라이언트 크리덴셜 검증(누락/불일치 시 401)
    if settings.cc_clients_json.get(creds.username) != creds.password:
        raise HTTPException(401, "bad client credentials")

    # 2) 키 준비(누락 시 503으로 변환)
    try:
        _ensure_keys()
    except RuntimeError as e:
        raise HTTPException(503, f"signing keys unavailable: {e}")

    # 3) 페이로드 구성: 표준 클레임 + 스코프
    now = int(time.time())
    payload = {
        "iss": settings.jwt_iss,                 # 토큰 발급자(검증 시 동일해야 함)
        "sub": creds.username,                   # 주체: client_id
        "aud": settings.jwt_aud,                 # 대상 서비스 식별자(검증 시 audience 체크)
        "scope": scope,                           # 공백 구분 스코프 문자열
        "iat": now,                              # 발급 시각
        "exp": now + int(settings.jwt_ttl_seconds),  # 만료 시각(초)
    }

    # 4) RS256 서명 후 액세스 토큰 반환
    return {
        "access_token": jwt.encode(payload, _PRIV, algorithm="RS256"),
        "token_type": "Bearer",
        "expires_in": settings.jwt_ttl_seconds,
    }


def m2m_required(required_scopes: list[str] | None = None):
    """라우트 보호용 의존성 팩토리

    사용 예:
      @router.post("/events/fall")
      async def ingest(..., sub: str = Depends(m2m_required(["events:fall:ingest"]))):
          ...

    동작:
      - Authorization: Bearer <JWT> 를 추출
      - RS256 공개키로 디코드(issuer/audience 엄격 검증)
      - 스코프 포함 여부 검사(부분집합)
      - 성공 시 토큰의 sub(client_id)을 반환
    """
    required_scopes = required_scopes or []

    def _dep(token: HTTPAuthorizationCredentials = Depends(_bearer)):
        # 1) 키 준비(누락 시 503)
        try:
            _ensure_keys()
        except RuntimeError as e:
            raise HTTPException(503, f"verification keys unavailable: {e}")

        # 2) 토큰 디코드/검증(발행자/대상/알고리즘)
        try:
            data = jwt.decode(
                token.credentials, _PUB,
                algorithms=["RS256"],
                audience=settings.jwt_aud,
                issuer=settings.jwt_iss,
            )
        except JWTError:
            # 서명 위조/만료/iss·aud 불일치 등 모든 조세 에러는 401 처리
            raise HTTPException(401, "invalid token")

        # 3) 스코프 부분집합 검사
        granted = set((data.get("scope") or "").split())  # 공백 구분 문자열 → 집합
        if not set(required_scopes).issubset(granted):
            raise HTTPException(403, "insufficient scope")

        # 4) 호출자 식별자 반환 (라우트에서 감사 로깅/소유권 확인에 활용)
        return data["sub"]

    return _dep
