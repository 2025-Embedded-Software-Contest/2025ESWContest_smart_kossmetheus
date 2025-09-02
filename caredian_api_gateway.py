"""
CareDian API Gateway (FastAPI) — SSL-safe app factory + self-tests
=================================================================
문제: `ssl` 모듈 부재 환경에서 FastAPI/Starlette/AnyIO import 단계에서 크래시.
해결: **지연 임포트 + Stub ASGI**로 임포트 실패 회피, 환경 준비 시 전체 기능 활성화.

Env Vars
--------
HA_BASE_URL         : https://caredian.gleeze.com   # ← API 루트(*/lovelace/* 아님)
HA_TOKEN            : Home Assistant long-lived token

JWT_SECRET          : HS256 shared secret (if JWT used)
JWT_ISSUER          : expected iss (optional)
JWT_AUDIENCE        : expected aud (optional)

API_KEYS            : comma-separated opaque keys (optional)

RATE_LIMIT          : requests per window (default: 60)
RATE_WINDOW_SEC     : size of window seconds (default: 60)

ALLOWED_ORIGINS     : comma-separated CORS origins

LOG_LEVEL           : DEBUG|INFO|WARNING|ERROR (default: INFO)
REQUEST_TIMEOUT_S   : outbound HTTP timeout (default: 10)

RUN_SERVER          : 1=서버 실행(직접 실행 시)
RUN_TESTS           : 1=셀프 테스트 실행(기본 1)
SIMULATE_NO_SSL     : 1=ssl 부재 상황 가상(테스트용)
FORCE_STUB          : 1=강제 Stub 모드(디버그)

Run
---
# 권장: 앱 팩토리 사용 (ssl 부재 시 Stub ASGI로 자동 전환)
uvicorn "gateway:create_app" --host 0.0.0.0 --port 8080

# 셀프 테스트만 수행
python gateway.py  # 또는 RUN_TESTS=1 python gateway.py
"""
from __future__ import annotations

import base64 # base64 인코딩/디코딩
import hashlib # 해시 함수 제공
import hmac # 비밀 키와 해싱 기술을 사용해 송수신자 간 메시지 변조 확인
import json # json 데이터
import logging # 로그 출력
import os
import time
from collections import defaultdict, deque # 자료형
from dataclasses import dataclass # 데이터 클래스 
from typing import Any, Deque, Dict, List, Optional, Tuple, Callable # 타입 힌트

# =====================
# SSL availability util
# =====================

def ssl_available() -> bool: # ssl 사용 여부
    if os.getenv("SIMULATE_NO_SSL") == "1":
        return False
    try:
        import ssl  # noqa: F401
        return True
    except ModuleNotFoundError:
        return False


# ===============
# JWT (HS256) util
# ===============
class JWTError(Exception):
    pass


def _b64url_decode(b64: str) -> bytes: # base64 디코딩
    padding = "=" * (-len(b64) % 4)
    return base64.urlsafe_b64decode(b64 + padding)


def _b64url_encode(raw: bytes) -> str: # base64 인코딩
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def jwt_decode_hs256(token: str, secret: str, *, iss: Optional[str] = None, aud: Optional[str] = None) -> Dict[str, Any]:
    # JWT HS256(JWT 서명 생성용 대칭키 암호화 알고리즘) 디코딩
    try:
        header_b64, payload_b64, sig_b64 = token.split(".")
    except ValueError as e:
        raise JWTError("Malformed token") from e

    try:
        header = json.loads(_b64url_decode(header_b64))
        payload = json.loads(_b64url_decode(payload_b64))
    except Exception as e:  # noqa: BLE001
        raise JWTError("Invalid base64 or JSON in token") from e

    if header.get("alg") != "HS256":
        raise JWTError("Unsupported alg; expected HS256")

    signing_input = f"{header_b64}.{payload_b64}".encode()
    expected_sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(_b64url_decode(sig_b64), expected_sig):
        raise JWTError("Invalid signature")

    now = int(time.time())
    if "exp" in payload and int(payload["exp"]) < now:
        raise JWTError("Token expired")
    if "nbf" in payload and int(payload["nbf"]) > now:
        raise JWTError("Token not yet valid")
    if iss is not None and payload.get("iss") != iss:
        raise JWTError("Invalid issuer")
    if aud is not None and payload.get("aud") != aud:
        raise JWTError("Invalid audience")

    return payload

def jwt_encode_hs256(payload: Dict[str, Any], secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    h = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    p = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    sig = hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{_b64url_encode(sig)}"


def _utcnow() -> int:
    return int(time.time())


def make_access_claims(sub: str, *, exp_sec: int, iss: Optional[str], aud: Optional[str]) -> Dict[str, Any]:
    now = _utcnow()
    claims = {"sub": sub, "iat": now, "nbf": now, "exp": now + exp_sec, "typ": "access"}
    if iss: claims["iss"] = iss
    if aud: claims["aud"] = aud
    return claims


def make_refresh_claims(sub: str, *, exp_sec: int, iss: Optional[str], aud: Optional[str], jti: str) -> Dict[str, Any]:
    now = _utcnow()
    claims = {"sub": sub, "iat": now, "nbf": now, "exp": now + exp_sec, "typ": "refresh", "jti": jti}
    if iss: claims["iss"] = iss
    if aud: claims["aud"] = aud
    return claims


class RefreshStore:
    """
    간단한 인메모리 리프레시 저장소 (회전/블랙리스트 지원).
    운영 시 Redis/DB로 교체 권장.
    """
    def __init__(self):
        # jti -> {"sub": str, "exp": int, "revoked": bool, "used": bool}
        self._store: Dict[str, Dict[str, Any]] = {}

    def add(self, jti: str, sub: str, exp: int):
        self._store[jti] = {"sub": sub, "exp": exp, "revoked": False, "used": False}

    def revoke(self, jti: str):
        if jti in self._store:
            self._store[jti]["revoked"] = True

    def use_once(self, jti: str) -> Optional[str]:
        item = self._store.get(jti)
        now = _utcnow()
        if not item:
            return None
        if item["revoked"] or item["used"] or item["exp"] <= now:
            return None
        item["used"] = True  # 회전(1회용)
        return item["sub"]

# ==========================
# Sliding-window rate limiter
# ==========================
@dataclass
class RateConfig:
    limit: int = 60
    window_sec: int = 60


class MemoryRateLimiter:
    def __init__(self, cfg: RateConfig):
        self.cfg = cfg
        self._buckets: Dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, identity: str, now: Optional[float] = None) -> Tuple[bool, int, int]:
        now = now if now is not None else time.time()
        window_start = now - self.cfg.window_sec
        dq = self._buckets[identity]

        while dq and dq[0] <= window_start:
            dq.popleft()

        if len(dq) < self.cfg.limit:
            dq.append(now)
            remaining = self.cfg.limit - len(dq)
            reset_in = int(self.cfg.window_sec - (now - (dq[0] if dq else now)))
            return True, remaining, reset_in
        
        remaining = 0
        reset_in = int(self.cfg.window_sec - (now - dq[0])) if dq else self.cfg.window_sec

        return False, remaining, reset_in


# ========
# Settings
# ========
# 데이터 유효성 검사 및 설정 관리를 위한 라이브러리
from pydantic import BaseModel, Field

class Settings(BaseModel):
    ha_base_url: str = Field(..., alias="HA_BASE_URL")
    ha_token: str = Field(..., alias="HA_TOKEN")

    jwt_secret: Optional[str] = Field(default=None, alias="JWT_SECRET")
    jwt_issuer: Optional[str] = Field(default=None, alias="JWT_ISSUER")
    jwt_audience: Optional[str] = Field(default=None, alias="JWT_AUDIENCE")
    access_ttl: int = Field(default=900, alias="ACCESS_TTL")          # 15분
    refresh_ttl: int = Field(default=1209600, alias="REFRESH_TTL")     # 14일

    api_keys: List[str] = Field(default_factory=list, alias="API_KEYS")
    rate_limit: int = Field(default=60, alias="RATE_LIMIT")
    rate_window_sec: int = Field(default=60, alias="RATE_WINDOW_SEC")
    allowed_origins: List[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    request_timeout: int = Field(default=10, alias="REQUEST_TIMEOUT_S")

    @staticmethod
    def _split(v: Optional[str]) -> List[str]:
        return [s.strip() for s in v.split(",")] if v else []

    @staticmethod
    def load_from_env() -> "Settings":
        data = {
            "HA_BASE_URL": os.getenv("HA_BASE_URL", ""),
            "HA_TOKEN": os.getenv("HA_TOKEN", ""),
            "JWT_SECRET": os.getenv("JWT_SECRET"),
            "JWT_ISSUER": os.getenv("JWT_ISSUER"),
            "JWT_AUDIENCE": os.getenv("JWT_AUDIENCE"),
            "API_KEYS": os.getenv("API_KEYS"),
            "RATE_LIMIT": int(os.getenv("RATE_LIMIT", "60")),
            "RATE_WINDOW_SEC": int(os.getenv("RATE_WINDOW_SEC", "60")),
            "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            "REQUEST_TIMEOUT_S": int(os.getenv("REQUEST_TIMEOUT_S", "10")),
            "ACCESS_TTL": int(os.getenv("ACCESS_TTL", "900")),
            "REFRESH_TTL": int(os.getenv("REFRESH_TTL", "1209600")),
        }

        return Settings(
            **{k: v for k, v in data.items() if k not in ("API_KEYS", "ALLOWED_ORIGINS")},
            API_KEYS=Settings._split(data["API_KEYS"]),
            ALLOWED_ORIGINS=Settings._split(data["ALLOWED_ORIGINS"]),
        )


# ============
# HA HTTP 클라이언트 (httpx 지연 임포트)
# ============
class HAClient:
    def __init__(self, base_url: str, token: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        self._timeout = timeout
        self._client = None

    async def _ensure(self):
        if self._client is None:
            import httpx  # lazy
            self._httpx = httpx
            self._client = httpx.AsyncClient(timeout=self._timeout)

    async def get_state(self, entity_id: str) -> Dict[str, Any]:
        await self._ensure()
        url = f"{self.base_url}/api/states/{entity_id}"
        r = await self._client.get(url, headers=self._headers)
        if r.status_code == 404:
            raise RuntimeError("Entity not found")
        r.raise_for_status()
        return r.json()

    async def call_service(self, domain: str, service: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        await self._ensure()
        url = f"{self.base_url}/api/services/{domain}/{service}"
        r = await self._client.post(url, headers=self._headers, json=payload)
        r.raise_for_status()
        try:
            data = r.json()
            if isinstance(data, list) and data:
                return data[0]
            return data if isinstance(data, dict) else {"result": data}
        except Exception:  # noqa: BLE001
            return {"status": "ok"}

    async def close(self):
        if self._client is not None:
            await self._client.aclose()


# ==============================
# ASGI app factory (FastAPI/Stub)
# ==============================
_logger = logging.getLogger("gateway")


def _setup_logging(level: str) -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format="%(asctime)s %(levelname)s %(message)s")


def _build_stub_app(message: str) -> Callable:
    async def app(scope, receive, send):
        assert scope["type"] == "http"
        path = scope.get("path", "/")
        if path == "/healthz":
            body = b'{"status":"ok"}'
            code = 200
        elif path == "/readyz":
            body = ("{" f"\"status\":\"down\",\"reason\":{json.dumps(message)!r}" "}").encode()
            code = 503
        else:
            body = (
                "{" f"\"detail\":\"FastAPI unavailable: {message}. "
                "Install system OpenSSL and a Python build with ssl module.\"" "}"
            ).encode()
            code = 503
        await send({"type": "http.response.start", "status": code, "headers": [(b"content-type", b"application/json")]})
        await send({"type": "http.response.body", "body": body})

    return app


def create_app():
    settings = Settings.load_from_env()
    _setup_logging(settings.log_level)

    if os.getenv("FORCE_STUB") == "1" or not ssl_available():
        reason = (
            "ssl module is not available. Install OpenSSL dev libs and rebuild Python "
            "(Deb/Ubuntu: libssl-dev, Alpine: openssl-dev) or use an official Python image."
        )
        _logger.warning("Starting in STUB mode: %s", reason)
        return _build_stub_app(reason)

    # ---- FastAPI 본 앱 (지연 임포트) ----
    from fastapi import Depends, FastAPI, HTTPException, Request, status  # lazy
    from fastapi.middleware.cors import CORSMiddleware  # lazy
    from fastapi.responses import JSONResponse  # lazy
    from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # lazy
    from pydantic import BaseModel, Field  # lazy for request models

    # 토큰 유틸/스토어
    refresh_store = RefreshStore()

    # Pydantic 모델
    class TokenPair(BaseModel):
        access_token: str
        refresh_token: str
        token_type: str = "bearer"
        expires_in: int = Field(..., description="access token TTL (sec)")

    class ExchangeRequest(BaseModel):
        """API Key -> JWT 교환 (실서비스에선 ID/비밀번호 등으로 대체)"""
        api_key: str
        sub: str = Field(..., description="subject(user id)")

    class RefreshRequest(BaseModel):
        refresh_token: str

    rate_cfg = RateConfig(limit=settings.rate_limit, window_sec=settings.rate_window_sec)
    rate_limiter = MemoryRateLimiter(rate_cfg)
    security = HTTPBearer(auto_error=False)

    app = FastAPI(title="CareDian API Gateway", version="1.1.0")

    if settings.allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    ha_client = HAClient(settings.ha_base_url, settings.ha_token, timeout=settings.request_timeout)

    @app.on_event("shutdown")
    async def on_shutdown():
        await ha_client.close()

    class ServiceCall(BaseModel):
        domain: str
        service: str
        entity_id: Optional[str] = None
        data: Dict[str, Any] = Field(default_factory=dict)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        resp = await call_next(request)
        _logger.info("%s %s -> %s (%.1fms)", request.method, request.url.path, getattr(resp, "status_code", "-"), (time.time() - start) * 1000)
        return resp
    
    async def auth_and_limit(request: Request, creds: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
        api_key = request.headers.get("X-API-Key")
        identity = None

        if api_key:
            if settings.api_keys and api_key not in settings.api_keys:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
            identity = f"key:{api_key[:4]}"

        if identity is None and creds and creds.scheme.lower() == "bearer":
            if not settings.jwt_secret:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT not configured")
            token = creds.credentials
            try:
                claims = jwt_decode_hs256(token, settings.jwt_secret, iss=settings.jwt_issuer, aud=settings.jwt_audience)
                if claims.get("typ") != "access":
                    raise JWTError("Not an access token")
                identity = f"jwt:{claims.get('sub', 'anon')}"
            except JWTError as e:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

        if identity is None:
            client_ip = request.client.host if request.client else "0.0.0.0"
            identity = f"ip:{client_ip}"

        allowed, remaining, reset_in = rate_limiter.allow(identity)
        if not allowed:
            headers = {"Retry-After": str(max(1, reset_in)), "X-RateLimit-Remaining": str(remaining)}
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded", headers=headers)

        request.state.rate_remaining = remaining
        request.state.rate_reset = reset_in
        request.state.identity = identity
        return identity
    
    # 응답 헤더 삽입용 미들웨어 추가
    @app.middleware("http")
    async def rate_headers(request: Request, call_next):
        resp = await call_next(request)
        try:
            rem = getattr(request.state, "rate_remaining", None)
            rst = getattr(request.state, "rate_reset", None)
            if rem is not None:
                resp.headers["X-RateLimit-Remaining"] = str(rem)
            if rst is not None:
                resp.headers["X-RateLimit-Reset"] = str(rst)
        except Exception:
            pass
        return resp

    # 토큰 생성기
    def _issue_tokens(sub: str) -> TokenPair:
        if not settings.jwt_secret:
            raise HTTPException(status_code=500, detail="JWT not configured")
        # access
        access_claims = make_access_claims(
            sub,
            exp_sec=settings.access_ttl,
            iss=settings.jwt_issuer,
            aud=settings.jwt_audience,
        )
        access = jwt_encode_hs256(access_claims, settings.jwt_secret)
        # refresh (jti 회전형)
        jti = _b64url_encode(os.urandom(16))
        refresh_claims = make_refresh_claims(
            sub,
            exp_sec=settings.refresh_ttl,
            iss=settings.jwt_issuer,
            aud=settings.jwt_audience,
            jti=jti,
        )
        refresh = jwt_encode_hs256(refresh_claims, settings.jwt_secret)
        refresh_store.add(jti, sub, refresh_claims["exp"])
        return TokenPair(access_token=access, refresh_token=refresh, expires_in=settings.access_ttl)

    # ---- Auth 라우트 ----
    @app.post("/auth/exchange", response_model=TokenPair, tags=["auth"])
    async def auth_exchange(body: ExchangeRequest):
        # 운영에서는 비밀번호/OTP 등으로 인증한 다음 토큰 발급
        if settings.api_keys and body.api_key not in settings.api_keys:
            raise HTTPException(401, "Invalid API key")
        return _issue_tokens(body.sub)

    @app.post("/auth/refresh", response_model=TokenPair, tags=["auth"])
    async def auth_refresh(body: RefreshRequest):
        if not settings.jwt_secret:
            raise HTTPException(500, "JWT not configured")
        try:
            claims = jwt_decode_hs256(body.refresh_token, settings.jwt_secret, iss=settings.jwt_issuer, aud=settings.jwt_audience)
        except JWTError as e:
            raise HTTPException(401, str(e))
        if claims.get("typ") != "refresh":
            raise HTTPException(401, "Not a refresh token")
        jti = claims.get("jti")
        if not jti:
            raise HTTPException(401, "Missing jti")
        sub = refresh_store.use_once(jti)
        if not sub:
            raise HTTPException(401, "Refresh token invalid or used")
        # 회전: 새 토큰 페어 발급
        return _issue_tokens(sub)

    @app.post("/auth/logout", tags=["auth"])
    async def auth_logout(body: RefreshRequest):
        # 클라이언트가 보유한 refresh 를 블랙리스트 처리
        try:
            claims = jwt_decode_hs256(body.refresh_token, settings.jwt_secret, iss=settings.jwt_issuer, aud=settings.jwt_audience)
        except JWTError as e:
            raise HTTPException(401, str(e))
        if claims.get("typ") != "refresh" or not claims.get("jti"):
            raise HTTPException(400, "Invalid refresh token")
        refresh_store.revoke(claims["jti"])
        return {"status": "ok"}
    
    @app.get("/healthz")
    async def health() -> Dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz")
    async def ready() -> Dict[str, str]:
        try:
            import httpx  # lazy
            async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
                r = await client.head(f"{ha_client.base_url}/api/")
                if r.status_code >= 400:
                    return JSONResponse(status_code=503, content={"status": "degraded"})
        except Exception:  # noqa: BLE001
            return JSONResponse(status_code=503, content={"status": "down"})
        return {"status": "ready"}

    @app.get("/v1/states/{entity_id}")
    async def get_state(entity_id: str, identity: str = Depends(auth_and_limit)) -> Dict[str, Any]:
        data = await ha_client.get_state(entity_id)
        return {"identity": identity, "state": data}

    @app.post("/v1/service")
    async def call_service(body: ServiceCall, identity: str = Depends(auth_and_limit)) -> Dict[str, Any]:
        payload = dict(body.data)
        if body.entity_id and "entity_id" not in payload:
            payload["entity_id"] = body.entity_id
        result = await ha_client.call_service(body.domain, body.service, payload)
        return {"identity": identity, "result": result}

    @app.post("/v1/devices/aircon/{entity_id}/{action}")
    async def aircon_action(entity_id: str, action: str, identity: str = Depends(auth_and_limit)) -> Dict[str, Any]:
        action = action.lower()
        if action not in {"on", "off"}:
            raise HTTPException(400, detail="action must be 'on' or 'off'")
        svc = "turn_on" if action == "on" else "turn_off"
        res = await ha_client.call_service("climate", svc, {"entity_id": entity_id})
        return {"identity": identity, "result": res}

    return app


# ============
# Self tests
# ============

def _gen_jwt(secret: str, payload: Dict[str, Any]) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    h = _b64url_encode(json.dumps(header).encode())
    p = _b64url_encode(json.dumps(payload).encode())
    sig = hmac.new(secret.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{_b64url_encode(sig)}"


def run_self_tests() -> None:
    print("[SelfTest] start")
    secret = "s3cr3t"
    now = int(time.time())

    good = _gen_jwt(secret, {"sub": "u1", "exp": now + 60, "iss": "me", "aud": "you"})
    assert jwt_decode_hs256(good, secret, iss="me", aud="you")["sub"] == "u1"

    try:
        jwt_decode_hs256(_gen_jwt(secret, {"exp": now - 1}), secret)
        raise AssertionError("expired should fail")
    except JWTError:
        pass

    try:
        jwt_decode_hs256(_gen_jwt("other", {"exp": now + 60}), secret)
        raise AssertionError("wrong signature should fail")
    except JWTError:
        pass

    try:
        jwt_decode_hs256(good, secret, iss="x")
        raise AssertionError("wrong iss should fail")
    except JWTError:
        pass
    try:
        jwt_decode_hs256(good, secret, aud="z")
        raise AssertionError("wrong aud should fail")
    except JWTError:
        pass

    rl = MemoryRateLimiter(RateConfig(limit=3, window_sec=1))
    ident = "t:abc"
    assert rl.allow(ident)[0]
    assert rl.allow(ident)[0]
    assert rl.allow(ident)[0]
    assert not rl.allow(ident)[0]
    time.sleep(1.1)
    assert rl.allow(ident)[0]

    os.environ["SIMULATE_NO_SSL"] = "1"
    assert not ssl_available()
    del os.environ["SIMULATE_NO_SSL"]

    print("[SelfTest] all passed")


if __name__ == "__main__":
    if os.getenv("RUN_TESTS", "1") == "1":
        run_self_tests()
    if os.getenv("RUN_SERVER") == "1":
        try:
            import uvicorn
            uvicorn.run("gateway:create_app", host="0.0.0.0", port=8080, reload=False)
        except Exception as e:  # noqa: BLE001
            print("[Run] failed:", e)
