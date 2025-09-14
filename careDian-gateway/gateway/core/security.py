import base64, hashlib, hmac, json, time # base64 인코더/디코더, 해시 함수, 메시지 변조, JSON, 시간 모듈
from typing import Any, Dict, Optional, Sequence # 타입 힌트


# 세션 쿠키
SESSION_COOKIE = "cd_session"

class JWTError(Exception): pass

# URL-safe Base64 Decode
def _b64url_decode(b64: str) -> bytes:
    pad = "=" * (-len(b64) % 4)
    return base64.urlsafe_b64decode(b64 + pad)

# URL-safe Base64 Encode
def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()

# 현재 시간 반환
def now_s() -> int:
    return int(time.time())

# 고정 헤더로 HS256 서명 생성
def jwt_encode_hs256(payload: Dict[str, Any], secret: str) -> str:
    if not secret:
        raise JWTError("Empty secret not allowed")
    header = {"alg": "HS256", "typ": "JWT"}
    h = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    p = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    sig = hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{_b64url_encode(sig)}"

# int형 타입 변환
def _to_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default

# 구조/서명/시간(exp, nbf)/발급자(iss)/대상(aud) 검증
def jwt_decode_hs256(
    token: str,
    secret: str,
    *,
    iss: Optional[str] = None,
    aud: Optional[Sequence[str] | str] = None,
    leeway: int = 5,  # seconds
) -> Dict[str, Any]:
    if not secret:
        raise JWTError("Empty secret not allowed")

    # 1) 구조 파싱
    try:
        hb, pb, sb = token.split(".")
    except ValueError:
        raise JWTError("Malformed token: expected 3 segments")

    try:
        header = json.loads(_b64url_decode(hb))
        payload = json.loads(_b64url_decode(pb))
        sig = _b64url_decode(sb)
    except Exception:
        raise JWTError("Malformed token: invalid base64/json")

    # 2) 헤더 검증
    if header.get("alg") != "HS256":
        raise JWTError("Unsupported alg: expected HS256")
    typ = header.get("typ")
    if typ not in (None, "JWT"):
        raise JWTError("Unsupported typ")

    # 3) 서명 검증
    calc = hmac.new(secret.encode(), f"{hb}.{pb}".encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(sig, calc):
        raise JWTError("Invalid signature")

    # 4) 표준 클레임 검증 (leeway 반영)
    now = now_s()
    exp = _to_int(payload.get("exp"))
    nbf = _to_int(payload.get("nbf"))
    if exp and exp < (now - leeway):
        raise JWTError("Token expired")
    if nbf and nbf > (now + leeway):
        raise JWTError("Token not yet valid")

    if iss is not None and payload.get("iss") != iss:
        raise JWTError("Invalid issuer")

    if aud:
        aud_claim = payload.get("aud")
        # aud 설정값을 시퀀스로 정규화
        want = [aud] if isinstance(aud, str) else list(aud)
        if isinstance(aud_claim, list):
            if not any(x in aud_claim for x in want):
                raise JWTError("Invalid audience")
        else:
            if aud_claim not in want:
                raise JWTError("Invalid audience")

    return payload