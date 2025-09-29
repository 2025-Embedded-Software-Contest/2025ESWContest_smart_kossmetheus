# ESP32-CAM 가스 검침 AI OCR 자동화 배포 가이드

## 📋 개요
ESP32-S3-Korvo2 v3.1에서 ESP32-CAM으로 마이그레이션하여 가스 검침 AI OCR 자동화 시스템을 구현합니다.

## 🛠️ 하드웨어 요구사항

### ESP32-CAM 모듈 (AI-Thinker)
- **모델**: ESP32-CAM (OV2640 카메라 센서)
- **해상도**: 1600x1200 (UXGA) 지원
- **내장 플래시 LED**: GPIO4 핀
- **Wi-Fi**: 2.4GHz 802.11 b/g/n

### 추가 필요 하드웨어
- **FTDI USB-to-Serial 모듈** (펌웨어 업로드용)
- **점퍼 와이어** (연결용)
- **5V 전원 공급장치** (안정적인 전원 공급)

## 🔌 ESP32-CAM 연결 방법

### FTDI 모듈과 ESP32-CAM 연결
```
FTDI Module    <->    ESP32-CAM
-----------           ---------
VCC (5V)      <->     5V
GND           <->     GND
RXD           <->     U0T (GPIO1)
TXD           <->     U0R (GPIO3)
```

### 프로그래밍 모드 진입
1. **GPIO0을 GND에 연결** (프로그래밍 모드)
2. **전원 연결**
3. **펌웨어 업로드**
4. **GPIO0 연결 해제** (정상 동작 모드)

## 📁 파일 구조

```
CareDian-backend/
├── esphome/
│   ├── esp32-cam.yaml          # ESP32-CAM 설정 파일
│   └── korvo2-v31.yaml        # 기존 Korvo-2 설정 (참고용)
├── automations.yaml           # 자동화 규칙 (업데이트됨)
├── scripts.yaml              # 스크립트 (업데이트됨)
└── pyscript/                 # 이미지 처리 스크립트
    ├── image_crop.py
    ├── image_resize.py
    └── image_rotate.py
```

## 🚀 배포 단계

### 1. ESPHome 펌웨어 컴파일 및 업로드

```bash
# ESPHome 설치 (필요한 경우)
pip install esphome

# 설정 검증
esphome config esphome/esp32-cam.yaml

# 펌웨어 컴파일
esphome compile esphome/esp32-cam.yaml

# 펌웨어 업로드 (첫 번째 업로드는 시리얼 포트 사용)
esphome upload esphome/esp32-cam.yaml --device /dev/ttyUSB0
```

### 2. Home Assistant 통합

ESP32-CAM이 부팅되면 Home Assistant에서 자동으로 발견됩니다:

1. **Settings > Devices & Services**로 이동
2. **ESPHome** 통합에서 새 장치 확인
3. **esp32-cam** 장치 추가
4. API 키 입력 (자동 생성됨)

### 3. 엔티티 확인

다음 엔티티들이 생성되어야 합니다:
- `camera.esp32_cam_esp32_cam_gas_cam` (카메라)
- `light.esp32_cam_esp32_cam_gas_light` (플래시 LED)
- `button.esp32_cam_capture_gas_snapshot` (스냅샷 버튼)
- `switch.esp32_cam_restart` (재시작 스위치)

## 🔧 설정 조정

### 카메라 위치 조정
ESP32-CAM을 가스 미터기에 최적의 위치에 설치한 후, 이미지 처리 파라미터를 조정해야 할 수 있습니다:

#### 1. 테스트 스냅샷 촬영
```yaml
# scripts.yaml의 test_gas_camera_snapshot 스크립트 실행
```

#### 2. 이미지 크롭 좌표 조정
`automations.yaml`의 "가스 검침 사진 촬영" 자동화에서 다음 값들을 조정:

```yaml
# 메인 크롭 영역
left: 200      # X 시작 좌표
top: 400       # Y 시작 좌표  
right: 1400    # X 끝 좌표
bottom: 650    # Y 끝 좌표

# 앞자리 숫자 분리
right: 180     # 앞자리 끝 X 좌표
bottom: 60     # 높이

# 뒷자리 숫자 분리  
left: 181      # 뒷자리 시작 X 좌표
right: 300     # 뒷자리 끝 X 좌표
bottom: 60     # 높이
```

### 3. 회전 각도 조정
필요한 경우 `rotation_angle` 값을 조정:
- `0`: 회전 없음
- `90`: 시계방향 90도
- `180`: 180도 회전
- `270`: 반시계방향 90도

## 🔄 자동화 동작

### 가스 검침 사진 촬영 (30분마다)
1. **플래시 LED 켜기** (78% 밝기, 흰색)
2. **2초 대기** (안정화)
3. **스냅샷 촬영** (`/config/www/tmp/gas/gas_latest.jpg`)
4. **이미지 회전** (필요시)
5. **이미지 크롭** (가스 미터 영역만 추출)
6. **이미지 리사이즈** (300px 폭으로 조정)
7. **숫자 영역 분리** (앞자리/뒷자리)
8. **플래시 LED 끄기**

### AI OCR 숫자 판독 (30분 30초마다)
1. **Google AI Vision API** 호출
2. **앞자리 숫자 읽기** (`gas_latest-crop-resize1.jpg`)
3. **뒷자리 숫자 읽기** (`gas_latest-crop-resize2.jpg`)
4. **숫자 조합 및 검증** (기존 값과 비교)
5. **가스 사용량 업데이트** (`input_number.gas_meter_2`)

## 🐛 문제 해결

### 연결 문제
- **Wi-Fi 연결 실패**: `secrets.yaml`에서 Wi-Fi 자격증명 확인
- **Home Assistant 연결 실패**: API 키 및 네트워크 설정 확인

### 이미지 품질 문제
- **흐린 이미지**: 카메라 위치 및 초점 조정
- **어두운 이미지**: 플래시 LED 밝기 조정 (`brightness_pct`)
- **잘못된 크롭**: 크롭 좌표 재조정

### OCR 인식 문제
- **숫자 인식 실패**: 이미지 전처리 파라미터 조정
- **잘못된 숫자**: AI 프롬프트 개선 또는 이미지 품질 향상

## 📊 모니터링

### 로그 확인
```bash
# ESPHome 로그
esphome logs esphome/esp32-cam.yaml

# Home Assistant 로그
tail -f /config/home-assistant.log | grep esp32_cam
```

### 이미지 확인
웹 브라우저에서 다음 경로로 이미지 확인:
- `http://your-ha-ip:8123/local/tmp/gas/gas_latest.jpg`
- `http://your-ha-ip:8123/local/tmp/gas/gas_latest-crop-resize1.jpg`
- `http://your-ha-ip:8123/local/tmp/gas/gas_latest-crop-resize2.jpg`

## 🔒 보안 고려사항

1. **API 키 보안**: `secrets.yaml` 파일 보호
2. **네트워크 보안**: 방화벽 설정으로 불필요한 포트 차단
3. **OTA 업데이트**: 안전한 네트워크에서만 수행

## 📈 성능 최적화

### 전력 관리
- **슬립 모드**: 필요시 deep sleep 모드 구현
- **프레임레이트 조정**: `max_framerate`와 `idle_framerate` 최적화

### 메모리 관리
- **JPEG 품질**: `jpeg_quality` 값으로 파일 크기 조절
- **해상도 조정**: 필요에 따라 해상도 낮춤

## 🆕 업그레이드 경로

### OTA (Over-The-Air) 업데이트
첫 번째 설치 후에는 Wi-Fi를 통해 무선 업데이트 가능:

```bash
esphome upload esphome/esp32-cam.yaml --device esp32-cam.local
```

### 설정 변경
ESPHome 설정 파일 수정 후 OTA로 업데이트하여 실시간 설정 변경 가능.

---

## 📞 지원

문제 발생 시 다음을 확인:
1. ESPHome 로그
2. Home Assistant 로그  
3. 네트워크 연결 상태
4. 하드웨어 연결 상태

이 가이드를 따라 ESP32-CAM 기반 가스 검침 AI OCR 자동화 시스템을 성공적으로 구축할 수 있습니다.
