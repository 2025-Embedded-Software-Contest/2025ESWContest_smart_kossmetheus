from __future__ import annotations

import httpx
from typing import Any, Dict
from urllib.parse import urljoin

from fastapi import APIRouter, Request, Response, HTTPException, status, Depends

from app.core.config import settings
from app.core.security import SESSION_COOKIE, jwt_decode_hs256, JWTError


router = APIRouter(prefix="/ha", tags=["ha-proxy"])

def _require_session(request: Request) -> Dict[str, Any]:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        return jwt_decode_hs256(token, settings.jwt_secret, iss=settings.jwt_issuer, aud=settings.jwt_audience)
    except JWTError as e:
        raise HTTPException(401, str(e))

def _build_sso_headers(username: str) -> Dict[str, str]:
    headers = {settings.ha_sso_header: username}
    if settings.ha_sso_groups_header and settings.ha_sso_default_groups:
        headers[settings.ha_sso_groups_header] = settings.ha_sso_default_groups
    return headers

@router.api_route("/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS","HEAD"])
async def ha_proxy(request: Request, path: str, _: Dict[str, Any] = Depends(_require_session)):
    claims = request.state.claims if hasattr(request.state, "claims") else _
    username = claims.get("sub") or "anonymous"

    if not settings.ha_base_url:
        raise HTTPException(500, "HA_BASE_URL not set")

    target = urljoin(f"{settings.ha_base_url.rstrip('/')}/", path)
    if request.url.query:
        target = f"{target}?{request.url.query}"

    # 클라이언트가 보낸 위험 헤더 제거 + SSO 헤더 삽입
    headers = {k: v for k, v in request.headers.items()}
    for k in ["host","content-length","connection","keep-alive","proxy-authenticate",
              "proxy-authorization","te","trailers","transfer-encoding","upgrade",
              "authorization","x-remote-user","x-remote-groups","x-remote-email","x-remote-name"]:
        headers.pop(k, None)
    headers.update(_build_sso_headers(username))

    body = await request.body() if request.method in {"POST","PUT","PATCH"} else None

    async with httpx.AsyncClient(timeout=settings.request_timeout, follow_redirects=False) as client:
        resp = await client.request(request.method, target, headers=headers, content=body)

    excluded = {"content-encoding","transfer-encoding","connection","keep-alive","proxy-authenticate",
                "proxy-authorization","te","trailers","upgrade"}
    out_headers = {k:v for k,v in resp.headers.items() if k.lower() not in excluded}
    return Response(content=resp.content, status_code=resp.status_code, headers=out_headers)
