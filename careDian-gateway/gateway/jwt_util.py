from __future__ import annotations
import base64, hashlib, hmac, json, time, os
from typing import Any, Dict, Optional # 타입 힌트


class JWTError(Exception):
    pass

# --- base64 url ---
_defpad = lambda s: s + "=" * (-len(s) % 4)

def b64u_d(s: str) -> bytes: # base64 url decode
    return base64.urlsafe_b64decode(_defpad(s))

def b64u_e(b: bytes) -> str: # base64 url encode
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()

# --- decode ---
def jwt_decode_hs256(token: str, secret: str, *, iss: Optional[str] = None, aud: Optional[str] = None) -> Dict[str, Any]:
    try:
        h_b64, p_b64, s_b64 = token.split(".")
        header = json.loads(b64u_d(h_b64))
        payload = json.loads(b64u_d(p_b64))
    except Exception as e:
        raise JWTError("Malformed token") from e
    
    if header.get("alg") != "HS256": # header의 알고리즘이 HS256이 아닐 경우
        raise JWTError("Unsupported alg; expected HS256")
    
    signing = f"{h_b64}.{p_b64}".encode()
    expect = hmac.new(secret.encode(), signing, hashlib.sha256).digest()

    if not hmac.compare_digest(b64u_d(s_b64), expect):
        raise JWTError("Invalid signature")
    
    # confirm this block
    now = int(time.time())
    if int(payload.get("exp", now+1)) < now:
        raise JWTError("Token expired")
    if int(payload.get("nbf", 0)) > now:
        raise JWTError("Token not yet valid")
    
    if iss is not None and payload.get("iss") != iss:
        raise JWTError("Invalid issuer")
    if aud is not None and payload.get("aud") != aud:
        raise JWTError("Invalid audience")
    
    return payload

# --- encode & claims ---
def jwt_encode_hs256(payload: Dict[str, Any], secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"} # header
    
    h = b64u_e(json.dumps(header, separators=(",", ":")).encode()) # encoded header
    p = b64u_e(json.dumps(payload, separators=(",", ":")).encode()) # encoded payload
    sig = hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()

    return f"{h}.{p}.{b64u_e(sig)}"

def utcnow_s() -> int:
    return int(time.time())

def claims_access(sub: str, *, exp_sec: int, iss: Optional[str], aud: Optional[str]):
    now = utcnow_s()
    claims = {"sub": sub, "iat": now, "nbf": now, "exp": now + exp_sec, "typ": "access"}

    if iss:
        claims["iss"] = iss
    if aud:
        claims["aud"] = aud

    return claims

def claims_refresh(sub: str, *, exp_sec: int, iss: Optional[str], aud: Optional[str], jti: str):
    now = utcnow_s()
    claims = {"sub": sub, "iat": now, "nbf": now, "exp": now + exp_sec, "typ": "refresh", "jti": jti}

    if iss:
        claims["iss"] = iss
    if aud:
        claims["aud"] = aud

    return claims

class RefreshStore:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def add(self, jti: str, sub: str, exp: int):
        self._store[jti] =  {
                                "sub": sub,
                                "exp": exp,
                                "revoked": False,
                                "used": False,
                            }

    def revoke(self, jti: str):
        if jti in self._store:
            self._store[jti]["revoked"] = True

    def use_once(self, jti: str) -> Optional[str]:
        item = self._store.get(jti)
        now = utcnow_s()

        if not item or item["revoked"] or item["used"] or item["exp"] <= now:
            return None
        
        item["used"] = True

        return item["sub"]