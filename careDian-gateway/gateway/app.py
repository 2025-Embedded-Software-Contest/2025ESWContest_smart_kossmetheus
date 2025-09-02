from __future__ import annotations # 타입 힌트 평가 X, 문자열로 저장
import os, time, json, logging, base64
from pydantic import BaseModel # 데이터 모델 정의
from pydantic import Field # 데이터 모델의 Field 정의
from typing import Any, Dict, Optional, Callable # 타입 힌트

from .settings import Settings
from .ssl_util import ssl_available
from .jwt_util import jwt_decode_hs256, jwt_encode_hs256, claims_access, claims_refresh, RefreshStore, JWTError
from .rate_limit import MemoryRateLimiter, RateConfig
from .ha_client import HAClient


_logger = logging.getLogger("gateway")

# pydantic models 
class ServiceCall(BaseModel):
    domain: str
    service: str
    entity_id: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class ExchangeRequest(BaseModel):
    api_key: str
    sub: str

class RefreshRequest(BaseModel):
    refresh_token: str

# 공통 설정
def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )

def _stub_app(message: str) -> Callable:
    async def app(scope, receive, send):
        assert scope["type"] == "http"
        path = scope.get("path", "/")

        if path == "/healthz":
            body, code = b'{"status":"ok"}', 200
        elif path == "/readyz":
            body, code = ("{" f"\"status\":\"down\",\"reason\":{json.dumps(message)!r}" "}").encode(), 503
        else:
            body, code = ("{" f"\"detail\":\"FastAPI unavailable: {message}. Install OpenSSL & Python ssl.\"" "}").encode(), 503

        await send({
            "type": "http.response.start",
            "status": code,
            "headers": [(b"content-type", b"application/json")],
        })
        await send({
            "type": "http.response.body",
            "body": body
        })

    return app

# ---- App factory ----

def create_app():
    settings = Settings.load_from_env()
    _setup_logging(settings.log_level)

    if os.getenv("FORCE_STUB") == "1" or not ssl_available():
        reason = "ssl module is not available. Install libssl-dev/openssl-dev or use official python image."
        _logger.warning("Starting in STUB mode: %s", reason)
        return _stub_app(reason)

    # Lazy FastAPI imports (ssl 없어도 상단 임포트 실패 방지)
    from fastapi import Depends, FastAPI, HTTPException, Request, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

    refresh_store = RefreshStore()
    rate = MemoryRateLimiter(RateConfig(limit=settings.rate_limit, window_sec=settings.rate_window_sec))
    security = HTTPBearer(auto_error=False)

    app = FastAPI(title="CareDian API Gateway", version="1.2.0")

    if settings.allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    ha = HAClient(
        settings.ha_base_url,
        settings.ha_token,
        timeout=settings.request_timeout
    )

    @app.on_event("shutdown")
    async def _shutdown():
        await ha.close()

    @app.middleware("http")
    async def _log(request: Request, call_next):
        t0 = time.time()
        resp = await call_next(request)
        _logger.info(
            "%s %s -> %s (%.1fms)",
            request.method,
            request.url.path,
            getattr(resp, "status_code", "-"),
            (time.time()-t0)*1000,
        )

        return resp
    
    async def auth_and_limit(request: Request, creds: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
        api_key = request.headers.get("X-API-Key")
        identity = None

        if api_key:
            if settings.api_keys and api_key not in settings.api_keys:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid API key"
                )
            identity = f"key:{api_key[:4]}"

        if identity is None and creds and creds.scheme.lower() == "bearer":
            if not settings.jwt_secret:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="JWT not configured"
                )
            try:
                claims = jwt_decode_hs256(
                    creds.credentials,
                    settings.jwt_secret,
                    iss=settings.jwt_issuer,
                    aud=settings.jwt_audience
                )

                if claims.get("typ") != "access":
                    raise JWTError("Not an access token")
                
                identity = f"jwt:{claims.get('sub','anon')}"
            except JWTError as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=str(e)
                )
            
        if identity is None:
            ip = request.client.host if request.client else "0.0.0.0"
            identity = f"ip:{ip}"

        ok, remain, reset = rate.allow(identity)

        if not ok:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={"Retry-After": str(max(1, reset)), "X-RateLimit-Remaining": str(remain)}
            )
        
        request.state.rate_remaining, request.state.rate_reset = remain, reset
        request.state.identity = identity

        return identity
    
    @app.middleware("http")
    async def _rate_headers(request: Request, call_next):
        resp = await call_next(request)
        rem = getattr(request.state, "rate_remaining", None)
        rst = getattr(request.state, "rate_reset", None)

        if rem is not None:
            resp.headers["X-RateLimit-Remaining"] = str(rem)
        if rst is not None:
            resp.headers["X-RateLimit-Reset"] = str(rst)

        return resp
    
    # ---- Auth ----
    def _issue(sub: str) -> TokenPair:
        if not settings.jwt_secret:
            raise HTTPException(500, "JWT not configured")
        
        access = jwt_encode_hs256(
            claims_access(
                sub,
                exp_sec=settings.access_ttl,
                iss=settings.jwt_issuer,
                aud=settings.jwt_audience
            ),
            settings.jwt_secret,
        )

        jti = base64.urlsafe_b64encode(os.urandom(16)).rstrip(b"=").decode()
        refresh_claims = claims_refresh(
            sub,
            exp_sec=settings.refresh_ttl,
            iss=settings.jwt_issuer,
            aud=settings.jwt_audience,
            jti=jti,
        )
        refresh = jwt_encode_hs256(refresh_claims, settings.jwt_secret)
        refresh_store.add(jti, sub, refresh_claims["exp"])

        return TokenPair(access_token=access, refresh_token=refresh, expires_in=settings.access_ttl)
    
    @app.post("/auth/exchange", response_model=TokenPair, tags=["auth"])
    async def exchange(body: ExchangeRequest):
        if settings.api_keys and body.api_key not in settings.api_keys:
            raise HTTPException(401, "Invalid API key")
        return _issue(body.sub)

    @app.post("/auth/refresh", response_model=TokenPair, tags=["auth"])
    async def refresh(body: RefreshRequest):
        if not settings.jwt_secret:
            raise HTTPException(500, "JWT not configured")
        try:
            c = jwt_decode_hs256(
                body.refresh_token,
                settings.jwt_secret,
                iss=settings.jwt_issuer,
                aud=settings.jwt_audience
            )
        except JWTError as e:
            raise HTTPException(401, str(e))
        
        if c.get("typ") != "refresh" or not c.get("jti"):
            raise HTTPException(401, "Invalid refresh token")
        
        sub = refresh_store.use_once(c["jti"])

        if not sub:
            raise HTTPException(401, "Refresh token invalid or used")
        
        return _issue(sub)
    
    @app.post("/auth/logout", tags=["auth"])
    async def logout(body: RefreshRequest):
        try:
            c = jwt_decode_hs256(
                body.refresh_token,
                settings.jwt_secret,
                iss=settings.jwt_issuer,
                aud=settings.jwt_audience
            )
        except JWTError as e:
            raise HTTPException(401, str(e))
        
        if c.get("typ") != "refresh" or not c.get("jti"):
            raise HTTPException(400, "Invalid refresh token")
        
        refresh_store.revoke(c["jti"])

        return {"status": "ok"}
    
    # ---- Health ----
    @app.get("/healthz")
    async def health() -> Dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz")
    async def ready() -> Dict[str, str]:
        try:
            import httpx

            async with httpx.AsyncClient(timeout=settings.request_timeout) as c:
                r = await c.head(f"{ha.base_url}/api/")

                if r.status_code >= 400:
                    return JSONResponse(status_code=503, content={"status": "degraded"})
        except Exception:
            return JSONResponse(status_code=503, content={"status": "down"})
        
        return {"status": "ready"}
    
    # ---- HA proxy ----
    # @app.get("/v1/states/{entity_id}")
    # async def get_state(entity_id: str, identity: str = Depends(auth_and_limit)) -> Dict[str, Any]:
    #     return {
    #         "identity": identity,
    #         "state": await ha.get_state(entity_id)
    #     }

    # @app.post("/v1/service")
    # async def call_service(body: ServiceCall, identity: str = Depends(auth_and_limit)) -> Dict[str, Any]:
    #     payload = dict(body.data)

    #     if body.entity_id and "entity_id" not in payload:
    #         payload["entity_id"] = body.entity_id

    #     return {
    #         "identity": identity,
    #         "result": await ha.call_service(body.domain, body.service, payload)
    #     }

    # @app.post("/v1/devices/aircon/{entity_id}/{action}")
    # async def aircon(entity_id: str, action: str, identity: str = Depends(auth_and_limit)) -> Dict[str, Any]:
    #     if action.lower() not in {"on", "off"}:
    #         raise HTTPException(400, "action must be 'on' or 'off'")
        
    #     svc = "turn_on" if action.lower()=="on" else "turn_off"
        
    #     return {
    #         "identity": identity,
    #         "result": await ha.call_service("climate", svc, {"entity_id": entity_id})
    #     }

    return app