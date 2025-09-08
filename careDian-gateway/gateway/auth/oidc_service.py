import httpx, json # 비동기 HTTP 클라이언트 라이브러리, json 처리
from typing import Any, Dict # 타입 힌트
from fastapi import HTTPException # 오류 처리
from jose import jwk # JSON Web Keys
from jose.utils import base64url_decode # JWT Token 디코딩

from gateway.core.security import _b64url_decode, now_s


class OIDCService:
    def __init__(self, *, issuer: str, client_id: str, timeout: int = 10):
        self.issuer = issuer.rstrip("/")
        self.client_id = client_id
        self.timeout = timeout

    async def verify_id_token(self, id_token: str) -> Dict[str, Any]:
        try:
            hb, pb, sb = id_token.split(".")
            header = json.loads(_b64url_decode(hb))
            payload = json.loads(_b64url_decode(pb))
            signature = base64url_decode(sb.encode())
        except Exception:
            raise HTTPException(400, "Malformed id_token")
        
        if header.get("alg") != "RS256":
            raise HTTPException(400, "Unsupported alg")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            disc = await client.get(f"{self.issuer}/.well-known/openid-configuration")
            disc.raise_for_status()
            jwks_uri = disc.json().get("jwks_uri")
            if not jwks_uri: raise HTTPException(502, "jwks_uri not found")
            jwks = await client.get(jwks_uri)
            jwks.raise_for_status()
            keys = jwks.json().get("keys", [])

        kid = header.get("kid")
        key = next((k for k in keys if not kid or k.get("kid") == kid), None)
        if not key: raise HTTPException(401, "No matching JWK")

        public_key = jwk.construct(key)
        if not public_key.verify(f"{hb}.{pb}".encode(), signature):
            raise HTTPException(401, "Invalid id_token signature")

        now = now_s()
        if payload.get("iss") != self.issuer: raise HTTPException(401, "Invalid issuer")
        aud = payload.get("aud")
        if isinstance(aud, list):
            if self.client_id not in aud: raise HTTPException(401, "Invalid audience")
        else:
            if aud != self.client_id: raise HTTPException(401, "Invalid audience")
        if int(payload.get("exp", 0)) < now: raise HTTPException(401, "id_token expired")
        if int(payload.get("nbf", 0)) > now: raise HTTPException(401, "id_token not yet valid")
        
        return payload
