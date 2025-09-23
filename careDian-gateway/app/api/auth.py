from __future__ import annotations

import os, time, httpx, secrets

from fastapi import APIRouter, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse

from app.core.config import Settings, settings
from app.core.security import jwt_encode_hs256, jwt_decode_hs256, now_s, SESSION_COOKIE, JWTError
from app.models.auth import TokenPair, ExchangeRequest, RefreshRequest


router = APIRouter(prefix="/auth", tags=["auth"])

def _enabled(s: Settings) -> bool:
    return bool(s.oidc_issuer and s.oidc_client_id and s.oidc_client_secret and s.oidc_redirect_uri)

async def _discover(issuer: str) -> dict:
    """OIDC discovery (권장: 간단한 in-memory 캐시)"""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(issuer.rstrip("/") + "/.well-known/openid-configuration")
        r.raise_for_status()
        return r.json()
    
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

@router.get("/login")
async def oidc_login():
    s = Settings()
    if not _enabled(s):
        raise HTTPException(501, "OIDC not configured")

    conf = await _discover(s.oidc_issuer)
    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)

    # NOTE: 필요하면 서버 세션/서명쿠키에 state/nonce를 보관해서 CSRF/Replay 방지 강화
    resp = RedirectResponse(
        url=(f"{conf['authorization_endpoint']}?"
             f"response_type=code&client_id={s.oidc_client_id}"
             f"&redirect_uri={s.oidc_redirect_uri}"
             f"&scope={' '.join(s.oidc_scopes)}"
             f"&state={state}&nonce={nonce}")
    )
    resp.set_cookie("oidc_state", state, httponly=True, secure=True, samesite="lax")
    resp.set_cookie("oidc_nonce", nonce, httponly=True, secure=True, samesite="lax")
    return resp

@router.get("/callback")
async def oidc_callback(request: Request, code: str | None = None, state: str | None = None):
    s = Settings()
    if not _enabled(s):
        raise HTTPException(501, "OIDC not configured")

    # state 검증
    cs = request.cookies.get("oidc_state")
    if not code or not state or state != cs:
        raise HTTPException(400, "Invalid state")

    conf = await _discover(s.oidc_issuer)
    token_endpoint = conf["token_endpoint"]

    # code -> (access_token, id_token, refresh_token ...) 교환
    async with httpx.AsyncClient(timeout=10) as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": s.oidc_redirect_uri,
            "client_id": s.oidc_client_id,
            "client_secret": s.oidc_client_secret,
        }
        r = await client.post(token_endpoint, data=data)
        if r.status_code >= 400:
            raise HTTPException(401, f"OIDC token exchange failed: {r.text}")
        tok = r.json()

    # (선택) id_token을 JWKS로 서명 검증 — jose/pyjwt 사용 가능
    # 여기선 최소안: /userinfo로 프로필 조회
    userinfo = {}
    if "userinfo_endpoint" in conf and tok.get("access_token"):
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(conf["userinfo_endpoint"], headers={"Authorization": f"Bearer {tok['access_token']}"})
            if r.status_code < 400:
                userinfo = r.json()

    # 게이트웨이 세션(JWT) 발급 — /ha 프록시에 쓰일 쿠키
    now = int(time.time())
    sub = userinfo.get("preferred_username") or userinfo.get("email") or userinfo.get("sub") or "user"
    claims = {
        "sub": sub,
        "iat": now, "nbf": now, "exp": now + 60*15,
        "iss": s.jwt_issuer, "aud": s.jwt_audience, "typ": "access",
        "name": userinfo.get("name"), "email": userinfo.get("email"),
        "roles": userinfo.get("roles") or userinfo.get("groups") or []
    }
    session_jwt = jwt_encode_hs256(claims, s.jwt_secret)

    resp = RedirectResponse(url="/")
    # 개발환경이면 secure=False 가능; 운영 TLS면 반드시 secure=True
    resp.set_cookie(SESSION_COOKIE, session_jwt, httponly=True, secure=True, samesite="lax", max_age=60*15)
    # 임시 state/nonce 쿠키 정리
    resp.delete_cookie("oidc_state")
    resp.delete_cookie("oidc_nonce")
    return resp

@router.post("/logout")
async def logout(resp: Response):
    resp.delete_cookie(SESSION_COOKIE)
    resp.delete_cookie("oidc_state")
    resp.delete_cookie("oidc_nonce")
    return resp
