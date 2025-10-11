from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.core.logging import setup_logging
from app.api import fall as fall_router
from app.services import influx


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
        return {"status": "ready" if influx.healthy() else "not-ready"}

    @app.get("/diag/influx")
    def diag_influx():
        out = {
            "url": settings.influxdb_url,
            "host": settings.influx_host,
            "port": settings.influx_port,
            "verify_tls": settings.influx_verify_tls,
        }
        try:
            influx._ensure_client().ping()
            out["ping"] = "ok"
        except Exception as e:
            out["ping"] = "fail"
            out["error"] = repr(e)
        return out

    @app.on_event("startup")
    async def on_startup():
        try:
            influx._ensure_client()
            logging.getLogger(__name__).info(
                "Influx target -> %s://%s:%s",
                settings.influx_proto, settings.influx_host, settings.influx_port
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
