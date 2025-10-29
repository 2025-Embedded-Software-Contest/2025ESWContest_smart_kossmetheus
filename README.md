<<<<<<< HEAD
# CareDian Gateway – FastAPI 서버

고령자 친화 스마트홈 프로젝트 **CareDian**의 백엔드 게이트웨이입니다.
센서/가전 이벤트를 수집·검증하고, InfluxDB로 기록하며, 인증 토큰 발급과 권한 검사를 제공합니다.

---

## 주요 기능

* **Client-Credentials(OAuth2 유사) 토큰 발급**: `/auth/cc/token` (RS256 서명, Audience/Issuer 검증)
* **낙상 등 이벤트 수집 API**: `/events/fall` (스코프 기반 권한, InfluxDB 기록, 알림 연계 선택)
* **운영 편의**: `/health`, `/ready`(옵션), OpenAPI 문서(`/docs`, `/redoc`)
* **보안 옵션**: CORS, HTTPS(리버스 프록시 권장), mTLS(선택), API Key(내부 엔드포인트용)

---

## 디렉토리 구조

```bash
CAREDIAN-GATEWAY
├── .caredian
├── app
│   ├── main.py
│   ├── server_tls.py
│   └── __init__.py      
├── api
│   ├── device.py
│   ├── fall.py
│   ├── ha.py
│   ├── influx_routes.py
│   └── __init__.py           
├── core
│   ├── config.py
│   ├── logging.py
│   ├── rate_limit.py
│   └── __init__.py     
├── models
│   ├── fall_lstm_final_v2_meta.json
│   ├── fall_lstm_model.h5
│   ├── fall_lstm_model_final_v2.keras
│   ├── fall_lstm_model_final_v2.tflite
│   └── scaler_final_v2.pkl
├── security
│   ├── api_key.py
│   ├── cc_jwt.py
│   ├── ha_auth.py
│   └── __init__.py
├── services
│   ├── fall_runtime.py
│   ├── ha_notify.py
│   ├── influx_v1.py
│   └── __init__.py    
├── certs
│   ├── ca.crt
│   ├── ca.key
│   ├── ca.srl
│   ├── private.key
│   ├── server.cnf
│   ├── server.crt
│   ├── server.csr
│   └── server.key
├── keys
│   ├── jwt_private.pem
│   ├── jwt_private.pem.pub
│   └── jwt_public.pem
├── scripts
│   └── log_to_csv.py
├── .env
├── gunicorn.conf.py
├── README.MD
└── requirements.txt
```

- app/
  - main.py: FastAPI 엔트리포인트. 라우터 등록, CORS/미들웨어, 헬스체크, OpenAPI 문서 노출.
  - server_tls.py: Uvicorn/Gunicorn용 TLS 기동 스크립트(서버 인증서·키 적용, mTLS 옵션 처리).
  - __init__.py: 패키지 초기화.

- api/
  - device.py: 디바이스 등록/상태(heartbeat)·정보 조회 등 장치 관련 REST 엔드포인트.
  - fall.py: 낙상 이벤트 수집 API(/events/fall). JWT 스코프 검증 → 유효성 검사 → InfluxDB 기록 → (옵션) 알림 트리거. 필요 시 services.fall_runtime로 모델 추론 사용.
  - ha.py: Home Assistant 연계(프록시/웹훅/노티 테스트 등). security.ha_auth로 접근 제어.
  - influx_routes.py: InfluxDB v1 관련 유틸/진단 라우트(헬스, 간단 쿼리·쓰기 테스트 등).
  - __init__.py: 패키지 초기화.

- core/
  - config.py: Pydantic Settings(.env 로딩). JWT/Influx/CORS/로그/SSL 등 전역 설정 단일화.
  - logging.py: 로거 초기화(JSON 포맷, 레벨/핸들러 구성).
  - rate_limit.py: 중복 알림 억제·레이트리밋 로직(예: should_alert).
  - __init__.py: 패키지 초기화.

- models/ (ML 아티팩트)
  - fall_lstm_final_v2_meta.json: 입력 스키마/윈도우 크기/라벨 등 메타 정보.
  - fall_lstm_model.h5: Keras H5 포맷 모델(구버전 호환).
  - fall_lstm_model_final_v2.keras: 최신 Keras 저장 포맷 모델(권장 사용).
  - fall_lstm_model_final_v2.tflite: 경량화된 TFLite 모델(엣지 배포용).
  - scaler_final_v2.pkl: 전처리 스케일러(표준화/정규화 파라미터).

- security/
  - api_key.py: 내부용 API Key 인증(헤더 파싱, 의존성 주입).
  - cc_jwt.py: Client-Credentials 토큰 발급/검증(RS256, aud/iss/exp/scope 확인, Bearer 의존성).
  - ha_auth.py: Home Assistant/외부 IdP 연동용 인증/인가 헬퍼(어드민 보호 엔드포인트용).
  - __init__.py: 패키지 초기화.

- services/
  - fall_runtime.py: 낙상 모델 로딩·전처리·추론 서비스(메타/스케일러 사용).
  - ha_notify.py: 알림 전송(HA REST/노티, 필요 시 FCM 등) 래퍼.
  - influx_v1.py: InfluxDB v1 클라이언트(라인프로토콜 생성, write/health, 재시도).
  - __init__.py: 패키지 초기화.

- certs/ (TLS/PKI 아티팩트)
  - ca.crt / ca.key: 로컬 CA 인증서/개인키(서버 인증서 서명용).
  - ca.srl: CA 발급 일련번호(state 파일).
  - server.cnf: OpenSSL 설정(SAN, 키용도 등).
  - server.csr: 서버 인증서 서명요청(CSR).
  - server.crt: CA가 서명한 서버 인증서(배포 사용본).
  - server.key: 서버 인증서 개인키.
  - private.key: 추가 생성된 키(용도 중복 가능—실사용 여부 확인·정리 권장).

- keys/ (JWT 서명키)
  - jwt_private.pem: RS256 개인키(서명).
  - jwt_private.pem.pub / jwt_public.pem: 공개키(검증). 둘 중 하나로 일원화 가능(중복 정리 권장).

- scripts/
  - log_to_csv.py: JSON 로그 → CSV 변환 스크립트(운영 분석용).

- 루트 파일
  - .caredian/: 프로젝트 전용 가상환경 디렉토리(개발자 로컬 전용).
  - .env: 환경변수 설정 파일(Settings 소스). 비밀값 포함—버전관리 제외 권장.
  - gunicorn.conf.py: 운영 실행 설정(워커 수, 타임아웃, 로깅 등).
  - README.MD: 프로젝트 개요/실행/배포 가이드 문서.
  - requirements.txt: 파이썬 의존성 목록(잠금/재현성)

---

## 요구 사항

* Python **3.11+**
* InfluxDB **1.x** (HTTP API 활성화)
* (운영 권장) Nginx Proxy Manager 또는 Nginx + Let’s Encrypt
* (선택) mTLS용 장치 클라이언트 인증서

---

## 빠른 시작(개발)

```bash
git clone <this-repo>
cd careDian-gateway

python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt                     # 또는: uv/poetry

cp .env.example .env                                # 값 채우기
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 운영 실행(예시)

```bash
# (권장) 리버스 프록시 뒤에서 Gunicorn+Uvicorn
gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8080 --timeout 60
```

---

## 환경 변수(.env)

```ini
# =========================
# 1) 앱/로깅/CORS
# =========================
APP_NAME="CareDian Gateway"
ENV=dev
LOG_LEVEL=INFO
LOG_JSON=1
ALLOWED_ORIGINS=["http://localhost:3000","https://gw-caredian.gleeze.com"]

# =========================
# 2) API Key / M2M
# =========================
API_KEYS_JSON={"ingestor":"<LONG_RANDOM_SECRET>"}                # 헤더 기반 키 인증
CC_CLIENTS_JSON={"esp32-01":"<LONG_RANDOM_SECRET>"}              # /auth/cc/token 발급 대상

# =========================
# 3) JWT (RS256)
# =========================
JWT_AUD="caredian-gw"
JWT_ISS="urn:caredian:gw"
JWT_PRIVATE_PEM_PATH="./keys/jwt_private.pem"
JWT_PUBLIC_PEM_PATH="./keys/jwt_public.pem"
JWT_TTL_SECONDS=43200  # 12h

# =========================
# 4) 세션
# =========================
SESSION_COOKIE_NAME="session-name"
SESSION_SECRET="<LONG_RANDOM_SECRET>"

# =========================
# 5) TLS / mTLS
# =========================
TLS_CERT=./certs/server.crt
TLS_KEY=./certs/server.key
TLS_HOST=0.0.0.0
TLS_PORT=8443

TLS_CA=./certs/ca.crt
TLS_REQUIRE_CLIENT_CERT=false  # 프록시/내부망 구조에 맞게 true 고려

# =========================
# 6) InfluxDB 1.8
# =========================
INFLUX_URL="http://192.168.1.175:8086"
INFLUX_DB="db"
INFLUX_USERNAME="username"
INFLUX_PASSWORD="<PASSWORD>"
INFLUX_TIMEOUT_SEC=10
INFLUX_VERIFY_TLS=0
INFLUX_MEASUREMENT="fall_events"

# =========================
# 7) Home Assistant
# =========================
HA_BASE_URL="http://homeassistant.local:8123"
HA_TOKEN="<HA_LONG_LIVED_ACCESS_TOKEN>"
REQUEST_TIMEOUT_SEC=10

# =========================
# 8) 알림 타깃
# =========================
HA_NOTIFY_MOBILE="notify.mobile_app"
HA_NOTIFY_PERSIST="notify.persistent_notification"
LOCATION_DEFAULT="home"

# =========================
# 9) 낙상 감지 AI
# =========================
FALL_INFERENCE_ENABLED=true
FALL_BACKEND="tflite"
FALL_MODEL_PATH="app/models/fall_lstm_model_final_v2.tflite"
FALL_SCALER_PATH="app/models/scaler_final_v2.pkl"
FALL_META_PATH="app/models/fall_lstm_final_v2_meta.json"
FALL_THRESHOLD=0.58
FALL_SMOOTH_K=3
FALL_DECISION_MODE="sensor_or_model"
FALL_COOLDOWN_SEC=300
FALL_AI_SUSTAIN_K=3
FALL_SEQ_LEN=3
```

> **권장**: 실제 서비스에서는 HTTPS 종단을 Nginx/NPM에서 수행하고, FastAPI는 내부 통신(예: 127.0.0.1:8080)만 사용하세요.
> **mTLS**: 디바이스→게이트웨이 수집 엔드포인트에 `TLS_REQUIRE_CLIENT_CERT=true`로 강제 가능.

---

## API 문서

### 1) 토큰 발급 – `POST /auth/cc/token`

* **목적**: M2M(ESP32 등) 장치용 Access Token 발급(RS256 JWT)
* **인증**:

  * (권장) `Authorization: Basic base64(client_id:client_secret)`
  * 또는 JSON 바디에 `client_id`, `client_secret`
* **바디 예시(JSON)**

```json
{
  "client_id": "esp32-01",
  "client_secret": "S3cr3t_Long_Random",
  "scope": "events:fall:ingest"
}
```

* **응답 예시**

```json
{
  "access_token": "<JWT>",
  "token_type": "Bearer",
  "expires_in": 43200,
  "scope": "events:fall:ingest"
}
```

* **검증 규칙**: 발급 시 `aud=JWT_AUD`, `iss=JWT_ISS`, `exp=TTL` 포함. 스코프는 최소권한 원칙.

---

### 2) 낙상 이벤트 수집 – `POST /events/fall`

* **목적**: 디바이스/모듈이 전송한 낙상·이상동작 등 이벤트 수집 → InfluxDB 기록(+옵션 알림)
* **인증**: `Authorization: Bearer <access_token>`

  * 요구 스코프: `events:fall:ingest`
* **헤더**: `Content-Type: application/json`
* **바디 예시**

```json
{
  "device_id": "esp32-01",
  "location": "living_room",
  "event": "fall",                // fall|idle|walk|sit|lie|none ...
  "prob": 0.93,                   // 신뢰도/확률
  "ts": 1730000000                // (선택) epoch seconds; 없으면 서버 시간이용
}
```

* **처리**:

  1. JWT 스코프 검증 → 2) 페이로드 검증 → 3) InfluxDB Line Protocol 작성 후 write
  2. (옵션) 동일 이벤트 연속 알림 rate-limit → HA/FCM로 노티 전송

* **응답**

```json
{"ok": true, "written": 1}
```

> Influx 측정명/태그 예시:
> `measurement=fall_events tags={device_id,location,event} fields={prob:float} time=ts`

---

### 3) 상태 점검

* `GET /health` → 애플리케이션 헬스(의존성 최소)
* `GET /ready`  → Influx 등 외부 의존성까지 준비 확인(있을 경우)

---

## InfluxDB 기록 정책(권장)

* **DB**: `sensors`
* **Measurement**:

  * `fall_events` (낙상/이상행동), `environment`, `device_power` 등 도메인별 분리
* **Tags**: `device_id`, `location`, `event`
* **Fields**: 확률/수치(`prob`, `value` 등), 보조지표
* **보존/압축**: RP(retention policy)로 30~90일 세부데이터 + 다운샘플(Continuous Query/Grafana)

---

## 보안 가이드

* **리버스 프록시**: Nginx/NPM에서 TLS 종단 및 HSTS, HTTP→HTTPS 리디렉션
* **CORS**: `ALLOWED_ORIGINS`에 정확한 프론트 도메인만 지정
* **JWT 키 관리**: `keys/`는 배포 시 외부 비공개 경로/시크릿 관리자 사용
* **장치 인증**:

  * 외부망 노출 수집 엔드포인트 → **JWT + mTLS** 조합 권장
  * 내부망만 사용 시라도 토큰 스코프 최소화
* **로그**: 개인정보/시크릿 마스킹, `LOG_JSON=1`로 수집 파이프라인 표준화

---

## 배포 패턴(예시: Nginx Proxy Manager)

1. 도메인 `gw-caredian.gleeze.com` → 프록시 호스트 생성
2. SSL: Let’s Encrypt 활성화
3. 고급 설정(참고):

```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

4. 백엔드: `http://<gateway-host>:8080`

> HA, Grafana 등과 공존 시 **WebSocket 옵션** 활성화 필요(해당 서비스에 한함).

---

## 테스트 예시

### 1) 토큰 발급

```bash
curl -s -X POST https://gw-caredian.gleeze.com/auth/cc/token \
  -H "Content-Type: application/json" \
  -d '{"client_id":"esp32-01","client_secret":"S3cr3t_Long_Random","scope":"events:fall:ingest"}'
```

### 2) 이벤트 전송

```bash
ACCESS_TOKEN="<위에서 받은 토큰>"

curl -s -X POST https://gw-caredian.gleeze.com/events/fall \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"esp32-01","location":"living_room","event":"fall","prob":0.91}'
```

---

## 트러블슈팅

* **401/403**: 토큰 만료/스코프 불일치 → `/auth/cc/token` 재발급, `scope` 확인
* **Influx 4xx**: DB/권한/버전 불일치 → `INFLUX_*` 설정과 DB 존재 여부 확인
* **CORS 에러**: `ALLOWED_ORIGINS`에 호출 도메인/포트를 정확히 추가
* **프록시 뒤 502/504**: 백엔드 포트/방화벽/헬스체크 확인, `--timeout`/리트라이 조정

---

## 개발 메모

* 센서/가전 데이터 목록·구성은 Influx/Grafana 대시보드 설계와 함께 유지보수하세요.
* 대용량 이벤트(초당 수십~수백 RPS) 예상 시 **비동기 write 배치**와 **큐(예: Redis, NATS)** 고려.
* 알림은 rate-limit(중복 억제) 및 장애 시 재시도 백오프 적용 권장.

---

## 라이선스

TBD

---

## 변경 이력(요약)

* v0.1: CC 토큰 발급 + 낙상 이벤트 수집 + InfluxDB 연동 기본 기능
* v0.2: 알림·중복억제, mTLS 옵션, 운영 로그 포맷(JSON) 추가

---

## 연락처

* Maintainer: CareDian Backend Team
* Issue: GitHub Issues 또는 운영 채널

> 이 문서는 레포지토리 구조와 배포 환경에 맞게 적절히 수정하여 사용하십시오.
=======
# 2025ESWContest_smart_kossmetheus
>>>>>>> origin/fastapi
