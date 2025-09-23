from __future__ import annotations

from pydantic import BaseModel, Field


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="access token TTL (sec)")

class ExchangeRequest(BaseModel):
    api_key: str
    sub: str = Field(..., description="subject(user id)")

class RefreshRequest(BaseModel):
    refresh_token: str
