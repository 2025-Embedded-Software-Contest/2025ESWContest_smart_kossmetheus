from fastapi import APIRouter, HTTPException # 라우터 모듈, 오류 처리
from pydantic import BaseModel, Field # 데이터 모델과 모델의 Field 정의
from fastapi.responses import JSONResponse, RedirectResponse # JSON 반환, 다른 URL로 리다이렉트

from gateway.core.settings import Settings
from gateway.core.security import SESSION_COOKIE
from gateway.auth.oidc_service import OIDCService
from gateway.auth.token_service import TokenService, TokenPair


router = APIRouter(prefix="/auth", tags=["auth"])

class OAuthVerifyRequest(BaseModel):
    provider: str = Field(..., description="e.g., google")
    id_token: str = Field(..., description="OIDC id token")

def _build_services(s: Settings):
    if not (s.oidc_issuer_url and s.oidc_client_id):
        raise HTTPException(500, "OIDC not configured")
    
    if not s.jwt_secret:
        raise HTTPException(500, "JWT not configured")
    
    oidc = OIDCService(issuer=s.oidc_issuer_url, client_id=s.oidc_client_id, timeout=s.request_timeout)
    tokens = TokenService(secret=s.jwt_secret, issuer=s.jwt_issuer, audience=s.jwt_audience,
                          access_ttl=s.access_ttl, refresh_ttl=s.refresh_ttl)
    
    return oidc, tokens

@router.post("/oauth/verify", response_model=TokenPair)
async def oauth_verify(body: OAuthVerifyRequest):
    s = Settings.load()
    oidc, tokens = _build_services(s)
    payload = await oidc.verify_id_token(body.id_token)
    sub = payload.get("sub")
    if not sub: raise HTTPException(400, "id_token missing sub")

    pair = tokens.issue_pair(sub)
    # 세션 쿠키도 함께 심어주고 싶으면 RedirectResponse로 대체 가능
    resp = JSONResponse(pair.model_dump())
    resp.set_cookie(key=SESSION_COOKIE, value=pair.access_token, httponly=True, secure=True, samesite="Lax", max_age=s.access_ttl)
    
    return resp
