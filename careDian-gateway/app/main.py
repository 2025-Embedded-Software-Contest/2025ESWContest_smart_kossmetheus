"""
모듈: app/main.py — FastAPI 앱 엔트리포인트

목적
  - 게이트웨이 서버 인스턴스를 생성하고 미들웨어/라우터/헬스 엔드포인트를 등록한다.
  - 로깅, CORS, 세션, 라우터 묶음, 스타트업/셔트다운 훅을 한 곳에서 초기화한다.

핵심 구성
  • 로깅 초기화: JSON/텍스트 선택, 레벨/핸들러 구성(app.core.logging)
  • 미들웨어: SessionMiddleware(옵션), CORS(옵션)
  • 라우터: /events(fall), /influx(관리), /ha(HA 연동), /auth/cc(M2M 토큰)
  • 헬스체크: /healthz(liveness), /readyz(readiness — Influx 연결 상태 반영)
  • 루트 리다이렉트: "/" → "/docs"(Swagger UI)

주요 설정값(app.core.config.settings)
  - app_name, log_level, log_json
  - allowed_origins(CORS 허용 오리진)
  - session_secret, session_cookie_name
  - env(dev/prod) → Session https_only 동작에 영향
  - Influx 연결 설정은 app.services.influx (싱글턴)에서 참조
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, PlainTextResponse
import logging
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api import fall as fall_router          # 낙상 이벤트 수신/처리 라우터
from app.api.influx_routes import router as influx_router  # Influx 관리/진단 라우터
from app.services import influx                   # 공용 Influx 서비스 싱글턴
from app.api import ha                            # HA 연동 라우터(모바일앱 notify 목록 등)
from app.security.cc_jwt import router as cc_router  # Client-Credentials 토큰 발급/검증


def create_app() -> FastAPI:
    """애플리케이션 인스턴스를 생성하고 모든 구성을 적용한다."""
    # 1) 로깅 초기화 — .env의 LOG_LEVEL/LOG_JSON 반영
    setup_logging(level=settings.log_level, json_mode=settings.log_json)

    # 2) FastAPI 앱 생성 — 문서 경로 지정(운영 환경에서 /docs 비활성화 가능)
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url="/docs",            # Swagger UI
        redoc_url="/redoc",          # ReDoc 문서
        openapi_url="/openapi.json"  # OpenAPI 스펙(JSON)
    )

    # 3) 세션 미들웨어(옵션) — session_secret 설정된 경우에만 활성화
    #    - https_only: 개발 모드(dev)가 아니면 Secure 쿠키 강제
    if settings.session_secret:   # 값 있을 때만 활성화
        app.add_middleware(
            SessionMiddleware,
            secret_key=settings.session_secret,
            same_site="lax",
            https_only=(settings.env != "dev"),
            session_cookie=settings.session_cookie_name,
        )

    # 4) CORS(옵션) — 허용 오리진이 지정된 경우에만 등록
    if settings.allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_origins,  # ["https://example.com", ...]
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # 5) 라우터 등록 — 기능별 모듈 분리
    app.include_router(fall_router.router)  # /events/* (낙상 처리)
    app.include_router(cc_router) # /auth/cc/* (토큰 발급)
    
    # 6) 루트 경로: 문서로 리다이렉트(스키마에는 숨김)
    @app.get("/", include_in_schema=False)
    def root():
        # 루트로 들어오면 /docs로 보내기
        return RedirectResponse(url="/docs")

    # 7) 단순 라이브니스 체크 — 프로세스가 살아 있으면 OK
    @app.get("/healthz")
    async def healthz():
        return {"status": "ok"}

    # 8) 레디니스 체크 — Influx 연결 가능 여부를 반영
    @app.get("/readyz")
    async def readyz():
        return {"status": "ready" if influx.healthy() else "not-ready"}

    # 9) 파비콘 요청 무시(204) — 로그 오염 방지
    @app.get("/favicon.ico", include_in_schema=False)
    def favicon():
        return PlainTextResponse(status_code=204)
    
    # 10) 애플리케이션 라이프사이클 훅 — 외부 자원 선초기화/정리
    @app.on_event("startup")
    async def on_startup():
        try:
            # Influx 클라이언트 준비(실패해도 앱은 기동, /readyz로 구분)
            influx._ensure_client()
            logging.getLogger(__name__).info(
                settings.influx_url
            )
        except Exception:
            # Influx가 죽어 있어도 앱은 뜨고 /readyz로 구분
            logging.getLogger(__name__).warning("Influx client init failed", exc_info=True)

    @app.on_event("shutdown")
    async def on_shutdown():
        # 앱 종료 시 Influx 커넥션 정리
        influx.close()

    return app


# (선택) 모듈 임포트 시점에도 로깅 레벨을 한 번 적용
#  - uvicorn --reload 환경에서 서브프로세스 초기 출력 포맷을 안정화하는 데 유용
setup_logging(settings.log_level)

# ASGI 애플리케이션 객체 — uvicorn/gunicorn이 참조
app = create_app()
