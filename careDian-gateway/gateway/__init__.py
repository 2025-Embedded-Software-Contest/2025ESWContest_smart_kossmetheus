"""
gateway/
  __init__.py                 # ← 패키지 인식용(비어있어도 됨)
  main.py                     # robust 엔트리포인트(이미 있음)
  app.py                      # create_app (이미 있음)
  core/
    __init__.py
    settings.py               # 환경설정 로더 (이미 제시)
    logging.py                # 로깅 설정 (이미 제시)
    rate_limit.py             # 레이트리밋 (이미 제시)
    security.py               # JWT 유틸/세션쿠키 (이미 제시)
  auth/
    __init__.py
    router.py                 # /auth/oauth/verify (이미 제시)
    oidc_service.py           # OIDC(JWKS) 검증 (이미 제시)
    token_service.py          # 내부 JWT 발급 (이미 제시)
  ha/
    __init__.py
    proxy_router.py           # /ha/* 프록시+SSO 헤더 (이미 제시)
    sso_headers.py            # 헤더 구성 (이미 제시)
  alerts/
    __init__.py
    router.py                 # /v1/alerts/fall (이미 제시)
    models.py                 # FallAlert (이미 제시)
    notifier_service.py       # FCM/HA notify (이미 제시)
  utils/
    __init__.py
    ssl_stub.py               # ssl 없는 환경용 Stub (이미 제시)

"""

"""
/auth/oauth/verify: 클라이언트가 준 id_token(구글 등)을 OIDC(JWKS)로 검증 → 내부 JWT access/refresh 발급 → Access는 세션쿠키 저장

/ha/: 세션쿠키의 내부 JWT를 검증 → X-Remote-User 등 SSO 헤더를 붙여 HA로 프록시 → HA는 헤더 인증 컴포넌트로 자동 로그인

/v1/alerts/fall: 낙상 알림을 받아 FCM + HA notify 모두 발송
"""

"""
외부 의존성(필수 패키지)

fastapi, uvicorn[standard], httpx

pydantic>=2

python-jose[cryptography] (OIDC/JWKS 검증용)

(WebSocket 프록시 확장 시) websockets
"""

"""
Home Assistant 쪽 필수 설정(게이트웨이 SSO 전제)

http.use_x_forwarded_for: true + http.trusted_proxies에 게이트웨이 IP/대역 추가

헤더 기반 인증 컴포넌트(예: hass-auth-header) 설치 및 해당 헤더 이름(HA_SSO_HEADER)과 매핑 규칙 설정
→ 게이트웨이가 넣는 X-Remote-User 값을 신뢰하여 자동 로그인
"""

"""
# 필수
HA_BASE_URL=https://caredian.gleeze.com
HA_TOKEN=YOUR_HA_LONG_LIVED_TOKEN
OIDC_ISSUER_URL=https://accounts.google.com
OIDC_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
JWT_SECRET=your_strong_random_secret

# 선택
ALLOWED_ORIGINS=https://app.example.com
HA_NOTIFY_SERVICES=notify.notify
REQUEST_TIMEOUT_S=10
LOG_LEVEL=INFO

# 프록시 SSO 헤더
HA_SSO_HEADER=X-Remote-User
HA_SSO_GROUPS_HEADER=X-Remote-Groups
HA_SSO_DEFAULT_GROUPS=users
"""