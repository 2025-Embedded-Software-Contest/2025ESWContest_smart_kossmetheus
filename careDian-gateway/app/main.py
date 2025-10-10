from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api import fall as fall_router
from app.services import influx_v1 as influx


def create_app() -> FastAPI:
    setup_logging(level=settings.log_level, json_mode=settings.log_json)

    app = FastAPI(title=settings.app_name, version="1.0.0")

    if settings.allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(fall_router.router)

    @app.get("/healthz")
    async def healthz():
        return {"status": "ok"}

    @app.get("/readyz")
    async def readyz():
        # 최소한 HA_BASE_URL만 확인 (외부 통신은 생략)
        return {"status": "ready"}

    @app.on_event("startup")
    async def on_startup():
        influx.init()

    @app.on_event("shutdown")
    async def on_shutdown():
        influx.close()

    return app

app = create_app()
