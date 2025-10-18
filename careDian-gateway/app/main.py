from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.core.logging import setup_logging
from app.api import fall as fall_router
# from app.api.secure_influx import router as secure_influx_router
from app.api.influx_routes import router as influx_router
from app.services import influx
from app.api import ha  

def create_app() -> FastAPI:
    setup_logging(level=settings.log_level, json_mode=settings.log_json)

    app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",            # Swagger UI
    redoc_url="/redoc",          # ReDoc 문서
    openapi_url="/openapi.json"  # OpenAPI 스펙
)

    if settings.allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # app.include_router(secure_influx_router)
    app.include_router(fall_router.router)
    app.include_router(influx_router)
    app.include_router(ha.router)

    @app.get("/healthz")
    async def healthz():
        return {"status": "ok"}

    @app.get("/readyz")
    async def readyz():
        return {"status": "ready" if influx.healthy() else "not-ready"}

    @app.get("/diag/influx")
    def diag_influx():
        out = {
            "url": settings.influx_url,
            "verify_tls": settings.influx_verify_tls,
        }
        try:
            influx._ensure_client().ping()
            out["ping"] = "ok"
        except Exception as e:
            out["ping"] = "fail"
            out["error"] = repr(e)
        return out

    @app.get("/debug/measurements")
    def list_measurements(limit: int = 50):
        # DB에 존재하는 측정값(Measurement)들 확인
        q = f"SHOW MEASUREMENTS LIMIT {int(limit)}"
        return influx.query_raw(q)
    
    @app.on_event("startup")
    async def on_startup():
        try:
            influx._ensure_client()
            logging.getLogger(__name__).info(
                settings.influx_url
            )
        except Exception:
            # Influx가 죽어 있어도 앱은 뜨고 /readyz로 구분
            logging.getLogger(__name__).warning("Influx client init failed", exc_info=True)

    @app.on_event("shutdown")
    async def on_shutdown():
        influx.close()

    return app

setup_logging(settings.log_level)

app = create_app()
