import os, time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from app.core.config import settings


router = APIRouter(prefix="/auth/cc", tags=["auth"])
_basic = HTTPBasic()
_bearer = HTTPBearer(auto_error=True)

_PRIV: bytes | None = None
_PUB:  bytes | None = None

def _read_file(p: str) -> bytes:
    with open(p, "rb") as f:
        return f.read()

def _ensure_keys():
    global _PRIV, _PUB
    if _PRIV and _PUB:
        return
    
    if settings.jwt_private_pem_path and os.path.exists(settings.jwt_private_pem_path):
        _PRIV = _read_file(settings.jwt_private_pem_path)
    else:
        raise RuntimeError("No RS256 private key configured")

    if settings.jwt_public_pem_path and os.path.exists(settings.jwt_public_pem_path):
        _PUB = _read_file(settings.jwt_public_pem_path)
    else:
        raise RuntimeError("No RS256 public key configured")

@router.post("/token")
def token(creds: HTTPBasicCredentials = Depends(_basic), scope: str = "events:fall:ingest"):
    """
    Username: Password -> CC_CLIENTS_JSON
    """
    if settings.cc_clients_json.get(creds.username) != creds.password:
        raise HTTPException(401, "bad client credentials")
    try:
        _ensure_keys()
    except RuntimeError as e:
        raise HTTPException(503, f"signing keys unavailable: {e}")
    now = int(time.time())
    payload = {
        "iss": settings.jwt_iss,
        "sub": creds.username,
        "aud": settings.jwt_aud,
        "scope": scope,
        "iat": now,
        "exp": now + int(settings.jwt_ttl_seconds),
    }
    return {
        "access_token": jwt.encode(payload, _PRIV, algorithm="RS256"),
        "token_type": "Bearer",
        "expires_in": settings.jwt_ttl_seconds,
    }

def m2m_required(required_scopes: list[str] | None = None):
    required_scopes = required_scopes or []
    def _dep(token: HTTPAuthorizationCredentials = Depends(_bearer)):
        try:
            _ensure_keys()
        except RuntimeError as e:
            raise HTTPException(503, f"verification keys unavailable: {e}")
        try:
            data = jwt.decode(
                token.credentials, _PUB,
                algorithms=["RS256"],
                audience=settings.jwt_aud,
                issuer=settings.jwt_iss,
            )
        except JWTError:
            raise HTTPException(401, "invalid token")
        granted = set((data.get("scope") or "").split())
        if not set(required_scopes).issubset(granted):
            raise HTTPException(403, "insufficient scope")
        return data["sub"]
    return _dep
