import logging # 로그 기록
from fastapi import FastAPI # FastAPI 모듈

from gateway.core.settings import Settings
from gateway.utils.ssl_stub import ssl_available, build_stub_app


def create_app():
    s = Settings.load() # setting 불러오기
    logging.basicConfig(level=getattr(logging, s.log_level.upper(), logging.INFO),
                        format="%(asctime)s %(levelname)s %(message)s") # 로깅 초기화

    if s.force_stub or not ssl_available(s.simulate_no_ssl): ## SSL 모듈 확인
        return build_stub_app("ssl module not available")

    app = FastAPI(title="CareDian Gateway", version="1.3.0") # FastAPI 앱 생성

    # CORS 적용
    if s.allowed_origins:
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(CORSMiddleware, allow_origins=s.allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    # 라우터
    from gateway.auth import router as auth_router # OAuth2, JWT (재)발급
    from gateway.ha import proxy_router as ha_router # Home Assistant API Proxy
    from gateway.alerts import router as alerts_router # 낙상 알림: FCM + HomeAssistant Notify

    
    app.include_router(auth_router.router)
    app.include_router(ha_router.router)
    app.include_router(alerts_router.router)

    return app
