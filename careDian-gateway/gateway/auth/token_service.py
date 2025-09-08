import os # os 모듈
from typing import Any, Dict, Optional # 타입 힌트
from pydantic import BaseModel, Field # 데이터 모델과 모델의 Field 정의

from gateway.core.security import jwt_encode_hs256, now_s


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="access TTL (sec)")

class TokenService:
    def __init__(self, *, secret: str, issuer: Optional[str], audience: Optional[str], access_ttl: int, refresh_ttl: int):
        self.secret = secret
        self.issuer = issuer
        self.audience = audience
        self.access_ttl = access_ttl
        self.refresh_ttl = refresh_ttl

    def _claims_access(self, sub: str) -> Dict[str, Any]:
        now = now_s()
        c = {"sub":sub, "iat":now, "nbf":now, "exp": now + self.access_ttl, "typ":"access"}
        if self.issuer: c["iss"] = self.issuer
        if self.audience: c["aud"] = self.audience

        return c

    def _claims_refresh(self, sub: str, jti: str) -> Dict[str, Any]:
        now = now_s()
        c = {"sub":sub, "iat":now, "nbf":now, "exp": now + self.refresh_ttl, "typ":"refresh", "jti": jti}
        if self.issuer: c["iss"] = self.issuer
        if self.audience: c["aud"] = self.audience

        return c

    def issue_pair(self, sub: str) -> TokenPair:
        access = jwt_encode_hs256(self._claims_access(sub), self.secret)
        jti = os.urandom(16).hex()
        refresh = jwt_encode_hs256(self._claims_refresh(sub, jti), self.secret)
        
        return TokenPair(access_token=access, refresh_token=refresh, expires_in=self.access_ttl)
