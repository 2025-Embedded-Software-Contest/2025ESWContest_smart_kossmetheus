# CareDian - Home Assistant Configuration

## 프로젝트 개요

CareDian은 Home Assistant를 기반으로 한 스마트 홈 케어 시스템입니다. 이 백엔드 구성은 다양한 IoT 디바이스와 센서를 통합하여 실시간 모니터링, 자동화, 그리고 사용자 안전을 위한 시나리오 기반 시스템을 제공합니다.

## 주요 기능

### 🏠 스마트 홈 자동화
- **시나리오 기반 자동화**: 아침, 조리, 화재, 외출, 낙상, 귀가, 취침 등 10가지 생활 시나리오
- **적응형 조명**: 시간대별 자동 조명 조절 및 색온도 최적화
- **환경 모니터링**: 실시간 공기질, 온도, 습도, 가스 농도 모니터링

### 🔧 기술적 특징
- **ESP32-CAM 통합**: 가스 미터 OCR을 통한 자동 사용량 측정
- **다중 센서 지원**: BLE 모니터, 스마트싱스, LG 스마트싱크 등
- **데이터 수집**: InfluxDB를 통한 시계열 데이터 저장 및 분석
- **음성 제어**: Google Home, Spotify 연동

### 📊 모니터링 및 분석
- **실시간 대시보드**: Lovelace UI를 통한 직관적인 모니터링
- **데이터 시각화**: ApexCharts를 활용한 그래프 및 차트

## 프로젝트 구조

```
homeassistant/
├── configuration.yaml          # 메인 설정 파일
├── automations.yaml            # 자동화 규칙
├── scripts.yaml               # 스크립트 정의
├── templates.yaml             # 템플릿 및 센서
├── packages/
│   └── caredian_scenarios.yaml # CareDian 시나리오 패키지
├── custom_components/          # 커스텀 컴포넌트
│   ├── adaptive_lighting/     # 적응형 조명
│   ├── pyscript/              # Python 스크립트
│   └── ...                    # 기타 커스텀 컴포넌트
├── esphome/                   # ESPHome 설정
│   └── esp32-cam.yaml         # ESP32-CAM 설정
├── pyscript/                  # Python 스크립트
│   ├── gas_ocr_prepare.py     # 가스 미터 OCR 처리
│   ├── image_crop.py          # 이미지 크롭
│   └── fan_control.py         # 팬 제어
├── lovelace/                  # UI 설정
└── themes/                    # 테마 파일
```

## 설치 및 설정

### 1. Home Assistant 설치
```bash
# Home Assistant Core 설치 (Python 환경)
pip install homeassistant

# 또는 Home Assistant OS 사용 권장
```

### 2. 프로젝트 클론
```bash
git clone -b homeassistant https://github.com/2025-Embedded-Software-Contest/2025ESWContest_smart_kossmetheus.git
cd 2025ESWContest_smart_kossmetheus
```

### 3. 설정 파일 복사
```bash
# Home Assistant 설정 디렉토리에 파일 복사
cp -r homeassistant/* /config/
```

### 4. 의존성 설치
```bash
# Python 패키지 설치
pip install -r pyscript/requirements.txt

# HACS를 통한 커스텀 컴포넌트 설치
# - adaptive_lighting
# - pyscript
# - browser_mod
# - spotcast
```

### 5. 환경 설정
```yaml
# secrets.yaml 생성 (민감한 정보)
# 예시:
# google_client_id: "your_client_id"
# telegram_bot_token: "your_bot_token"
# influxdb_password: "your_password"
```

## 주요 컴포넌트

### ESP32-CAM 가스 미터 OCR
- **파일**: `esphome/esp32-cam.yaml`
- **기능**: 30분마다 가스 미터 사진 촬영 및 OCR 처리
- **의존성**: PyScript, OpenCV, Tesseract

### 적응형 조명 시스템
- **컴포넌트**: `custom_components/adaptive_lighting/`
- **기능**: 시간대별 자동 조명 조절, 색온도 최적화
- **지원**: Philips Hue, LIFX, 기타 스마트 조명

### 공기질 모니터링
- **센서**: BLE 모니터, 스마트싱스 센서
- **데이터베이스**: InfluxDB 저장
- **알림**: 임계값 초과 시 자동 알림

## 자동화 시나리오

### 1. 아침 시나리오 (scn_morning)
- 시간: 06:00-09:00
- 기능: 조명 점등, 커튼 개방, 뉴스 알림

### 2. 조리 시나리오 (scn_cooking)
- 트리거: 주방 센서 활성화
- 기능: 환기팬 자동 가동, 가스 누출 모니터링

### 3. 화재 시나리오 (scn_fire)
- 트리거: 연기 감지기, 온도 센서
- 기능: 긴급 알림, 소화기 위치 안내

### 4. 낙상 시나리오 (scn_fall)
- 트리거: 모션 센서 비활성화 + 소리 감지
- 기능: 응급 연락, 가족 알림

## API 및 통합

### 외부 서비스
- **Google Home**: 음성 제어
- **Spotify**: 음악 재생
- **Telegram**: 알림 및 제어
- **Slack**: 팀 알림

### 데이터베이스
- **InfluxDB**: 시계열 데이터 저장
- **SQLite**: 설정 및 상태 저장

## 개발 및 디버깅

### 로그 확인
```bash
# Home Assistant 로그
tail -f /config/home-assistant.log

# 특정 컴포넌트 로그
grep "component_name" /config/home-assistant.log
```

### 설정 검증
```bash
# 설정 파일 문법 검사
hass --script check_config
```

### 자동화 테스트
```yaml
# automations.yaml에서 자동화 활성화/비활성화
automation:
  - alias: "테스트 자동화"
    initial_state: true  # 또는 false
```

## 보안 고려사항

### 민감한 정보 보호
- `secrets.yaml`에 API 키, 비밀번호 저장
- `.gitignore`로 민감한 파일 제외
- 정기적인 백업 및 암호화

### 네트워크 보안
- VPN 사용 권장
- 방화벽 설정
- 정기적인 보안 업데이트

## 문제 해결

### 일반적인 문제
1. **컴포넌트 로드 실패**: HACS 재설치, 의존성 확인
2. **자동화 작동 안함**: 트리거 조건, 엔티티 상태 확인
3. **센서 데이터 없음**: 통합 설정, 네트워크 연결 확인

## 팀 정보

- **프로젝트명**: CareDian
- **대회**: 2025 임베디드 소프트웨어 경진대회
- **팀**: 코스메테우스
- **개발기간**: 2025년

---
