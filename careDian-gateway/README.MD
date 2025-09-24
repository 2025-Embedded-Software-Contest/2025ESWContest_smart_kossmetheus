# CareDian Backend Gateway – README

## 📌 개요

CareDian 프로젝트는 **스마트 홈 IoT 플랫폼**으로,
라즈베리파이4 기반 Home Assistant + FastAPI Gateway + InfluxDB + MySQL + SSO(Auth/OIDC) 아키텍처를 통합합니다.

본 레포지토리는 **FastAPI 기반 API Gateway** 및 **백엔드 서비스**의 명세를 제공합니다.

---

## 📂 디렉토리 구조

```bash
CareDian-backend/
├── careDian-gateway/        # FastAPI Gateway 코드
│   ├── app/
│   │   ├── api/             # API 라우터 (auth, ha_proxy 등)
│   │   ├── core/            # 설정(config.py), 보안, DB 연결
│   │   ├── models/          # Pydantic 모델 및 ORM
│   │   ├── main.py          # FastAPI 엔트리포인트
│   │   └── ...
│   ├── gunicorn.conf.py     # Gunicorn 서버 설정
│   └── requirements.txt     # Python 의존성
├── InfluxDB.md              # IoT 센서 목록 및 InfluxDB 연동 정의
├── Home Assistant Sensor Data Capture.pdf
├── TechStack.md             # 기술 스택 정의
├── 작업.md                   # 진행 중인 작업 계획
└── README.md                # 현재 문서
```

---

## 🚀 실행 방법

### 1) 로컬 실행 (개발용)

```bash
$ cd careDian-gateway
$ uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 2) 프로덕션 실행 (Gunicorn + Uvicorn workers)

```bash
$ gunicorn -c gunicorn.conf.py app.main:app
```

**gunicorn.conf.py**

```python
bind = "0.0.0.0:8080"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
```

---

## 🔑 주요 기능

### 1. **API Gateway (FastAPI)**

* Home Assistant 프록시 API (`/ha/api`)
* Auth / OIDC 기반 로그인 (`/auth/login`, `/auth/callback`)
* Health Check (`/healthz`, `/readyz`)
* IoT 장치 이벤트 연동 (MQTT ↔ FastAPI ↔ InfluxDB/MySQL)

### 2. **데이터베이스**

* **MySQL**

  * 사용자 계정 / 인증 정보 / 자동화 YAML 저장
  * Authentik Webhook → FastAPI → MySQL UPSERT
* **InfluxDB**

  * 모든 IoT 센서 시계열 데이터 저장
  * Grafana 대시보드 연동

  → [InfluxDB.md](InfluxDB.md)에 센서/측정 항목 정의

### 3. **통신 (MQTT)**

* Mosquitto MQTT Broker
* TLS 1.3 / mTLS 적용
* 모든 메시지는 InfluxDB 로깅
* LG ThinQ API 연동 (Rate Limit 대응 포함)

### 4. **SSO (OIDC 기반)**

* Authentik을 IdP로 사용
* Google / Naver / Kakao 소셜 로그인 지원
* Home Assistant ↔ Authentik ↔ FastAPI 연동
* Redirect URI 예시:

  ```
  https://auth-caredian.gleeze.com/auth/callback
  https://caredian.gleeze.com/auth/openid/callback
  ```

### 5. **보안**

* OAuth2 / OIDC 기반 인증
* HS256 JWT 서명
* Redis 기반 세션 검증 (초당 10,000 req 이상 처리)
* API Key 기반 보호 기능 추가

---

## ⚙️ 기술 스택

* **Backend**: FastAPI, Uvicorn, Gunicorn
* **Database**: MySQL, InfluxDB
* **Auth**: Authentik (OIDC/SAML), JWT, Redis
* **IoT**: Home Assistant, Mosquitto MQTT, LG ThinQ API
* **Visualization**: Grafana
* **Infra**: Raspberry Pi 4, AWS EC2
