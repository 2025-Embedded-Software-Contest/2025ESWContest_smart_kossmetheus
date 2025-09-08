import base64, hashlib, hmac, json, time # base64 인코더/디코더, 해시 함수, 메시지 변조, JSON, 시간 모듈
from typing import Any, Dict, Optional # 타입 힌트


SESSION_COOKIE = "cd_session"

class JWTError(Exception): pass

def _b64url_decode(b64: str) -> bytes:
    pad = "=" * (-len(b64) % 4)
    return base64.urlsafe_b64decode(b64 + pad)

def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()

def now_s() -> int: return int(time.time())

def jwt_encode_hs256(payload: Dict[str, Any], secret: str) -> str:
    header = {"alg":"HS256", "typ":"JWT"}
    h = _b64url_encode(json.dumps(header, separators=(",",":")).encode())
    p = _b64url_encode(json.dumps(payload, separators=(",",":")).encode())
    sig = hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{_b64url_encode(sig)}"

def jwt_decode_hs256(token: str, secret: str, *, iss: Optional[str]=None, aud: Optional[str]=None) -> Dict[str, Any]:
    try:
        hb,pb,sb = token.split(".")
        header = json.loads(_b64url_decode(hb))
        payload = json.loads(_b64url_decode(pb))
        sig = _b64url_decode(sb)
    except Exception:
        raise JWTError("Malformed token")
    
    if header.get("alg") != "HS256": raise JWTError("Unsupported alg")

    calc = hmac.new(secret.encode(), f"{hb}.{pb}".encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(sig, calc): raise JWTError("Invalid signature")

    now = now_s()
    if int(payload.get("exp",0)) < now: raise JWTError("Token expired")
    if int(payload.get("nbf",0)) > now: raise JWTError("Token not yet valid")

    if iss and payload.get("iss") != iss: raise JWTError("Invalid issuer")
    
    if aud:
        aud_claim = payload.get("aud")
        if aud_claim != aud and (not isinstance(aud_claim, list) or aud not in aud_claim):
            raise JWTError("Invalid audience")
        
    return payload
