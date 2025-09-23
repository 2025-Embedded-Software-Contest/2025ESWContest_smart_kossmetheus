# 가스 검침 AI OCR 시스템

ESP32-S3-Korvo 2 v3.1 보드를 사용한 가스 검침 자동 인식 시스템입니다.

## 📋 개요

- **하드웨어**: ESP32-S3-Korvo 2 v3.1 + 카메라 모듈
- **소프트웨어**: ESPHome + Home Assistant + PyScript + OpenAI Vision API
- **기능**: 가스 검침기 숫자 자동 인식 및 사용량 추적

## 🚀 설치 및 설정

### 1. OpenAI API 키 설정

1. [OpenAI Platform](https://platform.openai.com/)에서 계정을 생성합니다.
2. API 키를 발급받습니다.
3. `secrets.yaml` 파일에서 다음을 수정합니다:

```yaml
openai_api_key: "sk-your-actual-openai-api-key-here"
```

### 2. WiFi 설정

`secrets.yaml` 파일에서 WiFi 정보를 수정합니다:

```yaml
wifi_ssid: "YOUR_WIFI_SSID"
wifi_password: "YOUR_WIFI_PASSWORD"
```

### 3. ESP32-S3-Korvo 2 v3.1 보드 설정

1. ESPHome 대시보드에서 새 장치를 추가합니다.
2. `korvo2-v31.yaml` 파일의 내용을 복사하여 붙여넣습니다.
3. "설치" 버튼을 클릭하여 펌웨어를 플래시합니다.

### 4. Home Assistant 재시작

설정이 완료되면 Home Assistant를 재시작합니다:

```bash
# Home Assistant 재시작
ha core restart
```

## ⚙️ 작동 원리

### 자동 검침 스케줄
- **30분마다**: 정기적으로 가스 검침기 사진 촬영
- **매일 오전 9시**: 아침 검침
- **매일 오후 9시**: 저녁 검침

### 이미지 처리 과정
1. **촬영**: ESP32 카메라가 가스 검침기 사진 촬영
2. **전처리**: PyScript를 통한 이미지 회전, 크롭, 대비 조정
3. **OCR**: OpenAI Vision API를 사용한 숫자 인식
4. **검증**: 이상치 감지 및 유효성 검사
5. **저장**: 검침값을 Home Assistant 센서에 저장

### 알림 기능
- **가스 사용량 과다 알림**: 월 50m³ 초과시 알림
- **가스 사용량 적음 알림**: 24시간 1m³ 미만 사용시 알림
- **OCR 오류 알림**: 인식 실패시 알림

## 📊 사용 가능한 엔티티

### 센서
- `sensor.gas_meter_2`: 현재 가스 검침값 (m³)
- `sensor.gas_meter_monthly`: 월별 가스 사용량

### 입력 수단
- `input_number.gas_meter_2`: 가스 검침값 설정
- `input_text.gas_message_2`: OCR 상태 메시지

### 자동화
- `automation.gas_meter_ocr_schedule`: 정기 검침 자동화
- `automation.gas_meter_ocr_manual`: 수동 검침 자동화
- `automation.gas_meter_low_usage_alert`: 사용량 적음 알림
- `automation.gas_meter_high_usage_alert`: 사용량 과다 알림

## 🔧 커스터마이징

### 이미지 전처리 조정

`pyscript.yaml`에서 이미지 처리 파라미터를 조정할 수 있습니다:

```yaml
global_ctx:
  gas_meter_crop_box: [100, 100, 700, 500]  # 크롭 영역 [left, top, right, bottom]
  gas_meter_rotation: -90  # 이미지 회전 각도
  ocr_confidence_threshold: 0.8  # OCR 신뢰도 임계값
```

### 검침 스케줄 변경

`automations.yaml`에서 스케줄을 수정할 수 있습니다:

```yaml
triggers:
  - trigger: time_pattern
    minutes: /30  # 30분마다 → 원하는 간격으로 변경
```

### 카메라 설정 조정

`esphome/korvo2-v31.yaml`에서 카메라 설정을 조정할 수 있습니다:

```yaml
esp32_camera:
  resolution: 800x600  # 해상도 변경
  jpeg_quality: 14     # JPEG 품질 (1-63, 낮을수록 품질 좋음)
  brightness: 0        # 밝기 조정
  contrast: 0          # 대비 조정
```

## 🐛 문제 해결

### OCR 인식률이 낮은 경우

1. **조명 확인**: 가스 검침기 주변 조명이 충분한지 확인
2. **카메라 각도 조정**: 카메라가 검침기를 정면으로 촬영하도록 조정
3. **크롭 영역 조정**: `pyscript.yaml`의 `gas_meter_crop_box` 값 조정
4. **해상도 향상**: ESPHome에서 해상도를 더 높게 설정

### API 오류 발생시

1. **API 키 확인**: `secrets.yaml`의 OpenAI API 키가 올바른지 확인
2. **인터넷 연결 확인**: ESP32와 Home Assistant의 인터넷 연결 확인
3. **API 사용량 확인**: OpenAI 계정의 API 사용량 한도 확인

### ESP32 연결 문제

1. **WiFi 신호 확인**: ESP32가 WiFi에 안정적으로 연결되는지 확인
2. **전원 공급 확인**: 안정적인 5V 전원 공급 확인
3. **펌웨어 재플래시**: 문제가 지속되면 ESPHome에서 펌웨어 재플래시

## 📝 로그 확인

### PyScript 로그
```bash
# Home Assistant 로그에서 PyScript 관련 로그 확인
설정 → 로그 → PyScript
```

### ESPHome 로그
```bash
# ESPHome 대시보드에서 로그 확인
ESPHome → korvo2-v31 → 로그
```

## 🔄 업데이트

새로운 버전의 기능이 업데이트되면:

1. `pyscript/gas_meter_ocr.py` 파일 업데이트
2. `automations.yaml`의 자동화 업데이트
3. Home Assistant 재시작

## 📞 지원

문제가 발생하거나 개선 제안이 있으시면:

1. 로그 파일 확인 후 문제 상황 설명
2. 카메라 설치 각도와 조명 상태 설명
3. 현재 검침기 사진 첨부 (가능하다면)

## ⚠️ 주의사항

- **API 비용**: OpenAI API 사용으로 인한 비용이 발생할 수 있습니다
- **개인정보**: 가스 검침 정보가 클라우드에 전송되므로 보안에 유의하세요
- **전력 사용**: 24시간 작동으로 인한 전력 소모를 고려하세요
- **정확성**: OCR 결과는 100% 정확하지 않을 수 있으니 정기적으로 확인하세요
