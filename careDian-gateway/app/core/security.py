from __future__ import annotations

import base64, hashlib, hmac, json, time
from typing import Any, Dict, Optional, Sequence

from app.core.config import settings


SESSION_COOKIE = settings.session_cookie

class JWTError(Exception): pass

def _b64url_decode(b64: str) -> bytes:
    pad = "=" * (-len(b64) % 4);  return base64.urlsafe_b64decode(b64 + pad)
def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()
def now_s() -> int: return int(time.time())

def jwt_encode_hs256(payload: Dict[str, Any], secret: str) -> str:
    if not secret:
        raise JWTError("Empty secret not allowed")
    header = {"alg": "HS256", "typ": "JWT"}
    h = _b64url_encode(json.dumps(header, separators=(",",":")).encode())
    p = _b64url_encode(json.dumps(payload, separators=(",",":")).encode())
    sig = hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{_b64url_encode(sig)}"

def _to_int(x: Any, default: int = 0) -> int:
    try: return int(x)
    except Exception: return default

def jwt_decode_hs256(token: str, secret: str, *, iss: Optional[str]=None,
                     aud: Optional[Sequence[str] | str]=None, leeway: int=5) -> Dict[str, Any]:
    if not secret: raise JWTError("Empty secret not allowed")
    try:
        hb, pb, sb = token.split(".")
        header = json.loads(_b64url_decode(hb))
        payload = json.loads(_b64url_decode(pb))
        sig = _b64url_decode(sb)
    except Exception: raise JWTError("Malformed token")

    if header.get("alg") != "HS256": raise JWTError("Unsupported alg")
    calc = hmac.new(secret.encode(), f"{hb}.{pb}".encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(sig, calc): raise JWTError("Invalid signature")

    now = now_s()
    exp = _to_int(payload.get("exp"));  nbf = _to_int(payload.get("nbf"))
    if exp and exp < (now - leeway): raise JWTError("Token expired")
    if nbf and nbf > (now + leeway): raise JWTError("Token not yet valid")

    if iss is not None and payload.get("iss") != iss: raise JWTError("Invalid issuer")
    if aud:
        aud_claim = payload.get("aud");  want = [aud] if isinstance(aud, str) else list(aud)
        if isinstance(aud_claim, list):
            if not any(x in aud_claim for x in want): raise JWTError("Invalid audience")
        else:
            if aud_claim not in want: raise JWTError("Invalid audience")
    return payload
