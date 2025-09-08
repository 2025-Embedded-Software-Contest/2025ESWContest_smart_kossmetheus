import logging # 로그 기록
from fastapi import FastAPI # FastAPI 모듈

from gateway.core.settings import Settings
from gateway.utils.ssl_stub import ssl_available, build_stub_app


def create_app():
    s = Settings.load()
    logging.basicConfig(level=getattr(logging, s.log_level.upper(), logging.INFO),
                        format="%(asctime)s %(levelname)s %(message)s")

    if s.force_stub or not ssl_available(s.simulate_no_ssl):
        return build_stub_app("ssl module not available")

    app = FastAPI(title="CareDian Gateway", version="1.3.0")

    # CORS
    if s.allowed_origins:
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(CORSMiddleware, allow_origins=s.allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    # 라우터
    from gateway.auth import router as auth_router
    from gateway.ha import proxy_router as ha_router
    from gateway.alerts import router as alerts_router

    
    app.include_router(auth_router.router)
    app.include_router(ha_router.router)
    app.include_router(alerts_router.router)

    @app.get("/healthz")
    async def health(): return {"status":"ok"}

    return app
