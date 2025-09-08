import httpx # 비동기 HTTP 클라이언트 라이브러리
from typing import Dict, Any # 타입 힌트
from urllib.parse import urljoin # URL을 구성 요소로 구문 분석

from fastapi import APIRouter, Request, Response, HTTPException, Depends, status
from gateway.core.settings import Settings
from gateway.core.security import SESSION_COOKIE, jwt_decode_hs256, JWTError
from gateway.ha.sso_headers import build_sso_headers


router = APIRouter(prefix="/ha", tags=["ha-proxy"])

def _require_session(request: Request, s: Settings) -> Dict[str, Any]:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        return jwt_decode_hs256(token, s.jwt_secret or "", iss=s.jwt_issuer, aud=s.jwt_audience)
    except JWTError as e:
        raise HTTPException(401, str(e))

@router.api_route("/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS","HEAD"])
async def ha_proxy(request: Request, path: str):
    s = Settings.load()

    if not s.ha_base_url:
        raise HTTPException(500, "HA_BASE_URL not set")
    
    claims = _require_session(request, s)
    username = claims.get("sub") or "anonymous"

    # 목적지 URL
    target = urljoin(f"{s.ha_base_url.rstrip('/')}/", path)
    if request.url.query:
        target = f"{target}?{request.url.query}"

    # 헤더 구성
    headers = {k:v for k,v in request.headers.items()}
    for k in ["host","content-length","connection","keep-alive","proxy-authenticate","proxy-authorization","te","trailers","transfer-encoding","upgrade","authorization"]:
        headers.pop(k, None)
    headers.update(build_sso_headers(s, username))

    body = await request.body() if request.method in {"POST","PUT","PATCH"} else None

    async with httpx.AsyncClient(timeout=s.request_timeout, follow_redirects=False) as client:
        resp = await client.request(request.method, target, headers=headers, content=body)

    excluded = {"content-encoding","transfer-encoding","connection","keep-alive","proxy-authenticate",
                "proxy-authorization","te","trailers","upgrade"}
    out_headers = {k:v for k,v in resp.headers.items() if k.lower() not in excluded}
    
    return Response(content=resp.content, status_code=resp.status_code, headers=out_headers)
