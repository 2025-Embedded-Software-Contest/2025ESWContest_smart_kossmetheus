# File Tree
```
careDian-gateway/
├─ app/
│  ├─ main.py
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ health.py
│  │  ├─ auth.py
│  │  ├─ ha_proxy.py
│  │  └─ alerts.py
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  ├─ logging.py
│  │  ├─ security.py
│  │  └─ rate_limit.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ auth.py
│  │  └─ alerts.py
│  └─ services/
│     ├─ __init__.py
│     ├─ ha_client.py
│     ├─ fcm.py
│     └─ notify.py
├─ tests/
│  ├─ __init__.py
│  ├─ test_health.py
│  └─ test_auth_flow.py
├─ .env
├─ gunicorn.conf.py
├─ requirements.txt
└─ README.md
```

# 파일 동작 개요
## app/main.py
* FastAPI 앱 엔트리포인트.
* 공통 로깅 초기화, CORS 설정 적용.
* 각 라우터(api/*.py) 등록.
* 운영에서 /docs, /redoc 접근 보호(기본 BasicAuth 가드).

## app/api/*
### health.py
* 헬스체크 엔드포인트(/healthz).
* 배포/모니터링에서 liveness 확인용.

### auth.py
* 인증 관련 엔드포인트(/auth/*).
* /auth/exchange: API Key → 내부 JWT(액세스/리프레시) 발급 + 세션 쿠키 설정.
* /auth/refresh: 리프레시 토큰 검증 → 새 토큰 재발급.
* /auth/logout: 세션 쿠키 제거.
* 게이트웨이 내부 세션 수립의 시작점.

### ha_proxy.py
* Home Assistant 프록시(/ha/**).
* 세션 쿠키(JWT) 검증 → 사용자 식별.
* 원본 위험 헤더 제거 후 SSO 헤더(X-Remote-User, X-Remote-Groups 등) 삽입.
* HA로 요청을 전달하고 응답을 클린하게 되돌려줌.

### alerts.py
* 낙상 알림 전용 API(/alerts/fall).
* 요구사항 반영:
    * location이 "home"인지 검증.
    * HA의 notify. <service> 호출(FCM은 필요 시 services/fcm.py 사용).

## app/core/*
### config.py
* pydantic-settings 기반 환경설정 로더.
* .env 값을 구조화: 로그, JWT, CORS, HA URL/토큰, SSO 헤더명, 레이트리밋 등.
* settings 싱글턴으로 전역에서 참조.

### logging.py
* JSON/텍스트 로그 포맷터 & 핸들러 구성.
* 콘솔/순환파일 로깅 지원.
* setup_logging() 한 번으로 루트 로거 초기화.

### security.py
* 경량 JWT 유틸 (HS256 직접 구현).
* jwt_encode_hs256, jwt_decode_hs256, 만료/nbf/iss/aud 검증.
* 세션 쿠키 이름 상수 관리(SESSION_COOKIE).

### rate_limit.py
* 인메모리 슬라이딩 윈도우 레이트리미터.
* allow(identity)로 허용/잔여/리셋까지 반환.
* 필요 시 미들웨어에서 활용(추가 확장 지점).

## app/models/*
### auth.py
* 인증 관련 Pydantic 모델:
* TokenPair(응답), ExchangeRequest, RefreshRequest(요청).

### alerts.py
* 낙상 알림 요청 모델 FallAlert:
* user_id, severity(low|medium|high), location("home"), meta(옵션).

## app/services/*
### ha_client.py
* Home Assistant REST 클라이언트(httpx).
* get_state(), call_service() 등 API 호출 래퍼.
* 토큰/타임아웃/에러 처리 일원화.

### fcm.py (선택)
* Firebase Admin SDK 래퍼(있으면 사용).
* 실제 푸시 발송 구현 위치.

### notify.py
* HA 알림 호출 헬퍼(notify.<service>).
* alerts.py에서 호출해 낙상 알림 라우트와 분리.

## tests/*
### test_health.py
* /healthz 기본 동작 확인.

### test_auth_flow.py
* /auth/exchange → /auth/refresh 토큰 흐름 검증(최소 E2E).

## 환경/런타임 파일
### .env
* 실행 환경별 설정값 보관(개발/운영은 파일 분리 권장).
* 예: JWT_SECRET, HA_BASE_URL, HA_TOKEN, ALLOWED_ORIGINS, ENABLE_DOCS 등.

### requirements.txt
* 의존성 목록(FastAPI, httpx, pydantic-settings, uvicorn 등).

### gunicorn.conf.py
* 운영 실행 파라미터(워커 수, 타임아웃, 로그 레벨 등).

### README.md
* 로컬 실행, 운영 배포, 환경변수 표 등 사용 설명서

# 안 쓰는 파일
test_jwt_util.py
test_rate_limit.py
test_ssl_stub.py

# 실행
```
$env:PYTHONPATH = (Get-Location).Path
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# dev
export PYTHONPATH=.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# prod
export PYTHONPATH=.
gunicorn -k uvicorn.workers.UvicornWorker app.main:app -c gunicorn.conf.py
```