from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import settings, origins
from app.core.logging import setup_logging
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.ha_proxy import router as ha_router
from app.api.alerts import router as alerts_router


security = HTTPBasic(auto_error=False)

def require_docs_auth(creds: HTTPBasicCredentials = Depends(security)):
    if not settings.enable_docs:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if settings.docs_username and settings.docs_password:
        if not creds or creds.username != settings.docs_username or creds.password != settings.docs_password:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                headers={"WWW-Authenticate": "Basic"},
                                detail="Unauthorized")
    return True

def create_app() -> FastAPI:
    setup_logging(settings.log_level, settings.log_json)
    app = FastAPI(title=settings.app_name, version="1.0.0")

    if origins():
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins(),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(health_router, include_in_schema=False)
    app.include_router(auth_router)
    app.include_router(ha_router)
    app.include_router(alerts_router)

    @app.get("/docs", include_in_schema=False)
    async def docs(_: bool = Depends(require_docs_auth)):
        from fastapi.openapi.docs import get_swagger_ui_html
        return get_swagger_ui_html(openapi_url=app.openapi_url, title=f"{settings.app_name} - Docs")

    @app.get("/redoc", include_in_schema=False)
    async def redoc(_: bool = Depends(require_docs_auth)):
        from fastapi.openapi.docs import get_redoc_html
        return get_redoc_html(openapi_url=app.openapi_url, title=f"{settings.app_name} - Redoc")

    return app

app = create_app()
