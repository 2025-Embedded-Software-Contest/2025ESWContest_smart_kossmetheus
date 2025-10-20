# CareDian Backend Gateway – README

## 1. 개요

CareDian는 **스마트 홈 IoT 플랫폼**으로,
라즈베리파이4 기반 **Home Assistant + FastAPI Gateway + InfluxDB** 아키텍처를 통합합니다.

본 레포지토리는 **FastAPI 기반 API Gateway** 및 백엔드 서비스 명세를 제공합니다.

---

## 2. 디렉토리 구조

```bash
CareDian-backend/
├── careDian-gateway/ # FastAPI Gateway 코드
│ ├── app/
│ │ ├── api/ # API 라우터 (ha_proxy, metrics 등)
│ │ ├── core/ # 설정(config.py), 보안, 외부연동 클라이언트
│ │ ├── models/ # Pydantic 모델 및 ORM/DTO
│ │ ├── services/ # 비즈니스 로직 계층
│ │ └── main.py # FastAPI 엔트리포인트
│ ├── gunicorn.conf.py # Gunicorn 서버 설정
│ └── requirements.txt # Python 의존성
└── README.md
---
```

## 3. 실행 방법

### 3.1. 로컬 실행 (개발용)

```bash
cd CareDian-backend/careDian-gateway
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 3.2. 프로덕션 실행 (Gunicorn + Uvicorn workers)

```bash
$ gunicorn -c gunicorn.conf.py app.main:app
```

**gunicorn.conf.py**

```python
bind = "0.0.0.0:8080"
workers = 2  # Pi4
worker_class = "uvicorn.workers.UvicornWorker"
```

---

## 4. 주요 기능

1. API Gateway (FastAPI)
  - Home Assistant 프록시
    - GET /ha/states : 엔티티 상태 조회(필터: domain, entity_id)
    - POST /ha/services/{domain}/{service} : 서비스 호출(body: entity_id, data)
  - 이벤트/알림
    - POST /events/fall : 낙상 이벤트 수집 → 후속 처리(예: FCM)
    - POST /notify : 보호자 공지/경보 발송
  - 자동화/메타
    - GET /devices, POST /automations, GET /automations/{id}/runs
  - 시계열/분석
    - GET /metrics/energy : Influx 집계(1h/24h/7d) 조회
    - /healthz, /readyz 등 헬스체크 엔드포인트는 현재 문서에서 제외.

2. 데이터베이스
  - InfluxDB
    - IoT 센서 시계열 저장 및 Grafana 연동
    - 측정/태그/필드 규칙 및 다운샘플 정책은 InfluxDB.md 참고

---

## 5. 보안

- JWT(HS256) 토큰 인증, role/scope 기반 인가
- CORS 허용 도메인 제어(ALLOWED_ORIGINS)
- API Key(옵션) / 속도제한(Token Bucket) / 요청 추적(X-Request-ID)
- 프록시(Nginx Proxy Manager) 뒤 배치 시 X-Forwarded-* 신뢰 설정

---

## 6. 기술 스택

- Backend: FastAPI, Uvicorn, Gunicorn
- Time-Series DB: InfluxDB
- IoT: Home Assistant, Mosquitto MQTT, (LG ThinQ via HA Integration)
- Visualization: Grafana
- Infra: Raspberry Pi 4, Docker/Compose
