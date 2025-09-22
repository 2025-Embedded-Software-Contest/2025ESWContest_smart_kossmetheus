import os
from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
from app.core.config import settings
from app.core.security import jwt_encode_hs256, jwt_decode_hs256, now_s, SESSION_COOKIE, JWTError
from app.models.auth import TokenPair, ExchangeRequest, RefreshRequest

router = APIRouter(prefix="/auth", tags=["auth"])

def _issue_tokens(sub: str) -> TokenPair:
    now = now_s()
    access = jwt_encode_hs256(
        {"sub": sub, "iat": now, "nbf": now, "exp": now + settings.access_ttl, "typ": "access",
         **({"iss": settings.jwt_issuer} if settings.jwt_issuer else {}),
         **({"aud": settings.jwt_audience} if settings.jwt_audience else {})},
        settings.jwt_secret,
    )
    refresh = jwt_encode_hs256(
        {"sub": sub, "iat": now, "nbf": now, "exp": now + settings.refresh_ttl, "typ": "refresh",
         **({"iss": settings.jwt_issuer} if settings.jwt_issuer else {}),
         **({"aud": settings.jwt_audience} if settings.jwt_audience else {})},
        settings.jwt_secret,
    )
    return TokenPair(access_token=access, refresh_token=refresh, expires_in=settings.access_ttl)

@router.post("/exchange", response_model=TokenPair)
async def exchange(body: ExchangeRequest, resp: Response):
    keys_env = os.getenv("API_KEYS", "")
    keys = [k.strip() for k in keys_env.split(",") if k.strip()]
    if keys and body.api_key not in keys:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    pair = _issue_tokens(body.sub)
    # 세션 쿠키 설정 (게이트웨이 자체 세션)
    resp.set_cookie(SESSION_COOKIE, pair.access_token, httponly=True, secure=True, samesite="Lax", max_age=settings.access_ttl)
    return pair

@router.post("/refresh", response_model=TokenPair)
async def refresh(body: RefreshRequest, resp: Response):
    try:
        claims = jwt_decode_hs256(body.refresh_token, settings.jwt_secret, iss=settings.jwt_issuer, aud=settings.jwt_audience)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
    if claims.get("typ") != "refresh":
        raise HTTPException(401, "Not a refresh token")
    pair = _issue_tokens(claims["sub"])
    resp.set_cookie(SESSION_COOKIE, pair.access_token, httponly=True, secure=True, samesite="Lax", max_age=settings.access_ttl)
    return pair

@router.post("/logout")
async def logout(resp: Response):
    resp.delete_cookie(SESSION_COOKIE)
    return {"status":"ok"}
