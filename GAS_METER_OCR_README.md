# 가스 검침기 OCR 자동화 가이드

## 개요
ESP32-CAM을 활용한 가스 검침기 숫자 영역 자동 크롭 및 OCR 처리 시스템입니다.

## 주요 기능
- ✅ 자동 숫자 영역 감지 및 크롭
- ✅ 이미지 회전 기능
- ✅ Home Assistant 자동화 연동
- ✅ OCR용 최적화된 이미지 출력

## 설치 및 설정

### 1. 의존성 설치
```bash
pip install opencv-python==4.8.1.78
pip install Pillow==11.0.0
```

### 2. Pyscript 설정
`pyscript/` 폴더에 다음 파일들이 준비되어 있어야 합니다:
- `image_crop.py` - 주요 크롭 기능
- `requirements.txt` - 의존성 목록

### 3. Home Assistant 설정
`configuration.yaml`에 다음 서비스를 등록하세요:

```yaml
pyscript:
  scripts:
    - image_crop.py
```

## 사용법

### 기본 사용법 (자동 감지)
```python
# 서비스 호출 예시
service.call("pyscript", "gas_meter_crop",
  input_image="/config/www/gas_latest.jpg",
  output_image="/config/www/gas_cropped.jpg",
  rotation_angle_before=0,
  rotation_angle=0
)
```

### 수동 크롭 사용법
```python
# 서비스 호출 예시
service.call("pyscript", "image_crop",
  input_image="/config/www/gas_latest.jpg",
  output_image="/config/www/gas_manual_crop.jpg",
  left=400,
  top=300,
  right=800,
  bottom=500,
  rotation_angle_before=0,
  rotation_angle=0,
  auto_detect=False
)
```

## 서비스 파라미터

### `gas_meter_crop` 서비스
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|-------|------|
| `input_image` | string | ✅ | - | 입력 이미지 경로 |
| `output_image` | string | ✅ | - | 출력 이미지 경로 |
| `rotation_angle_before` | number | ❌ | 0 | 크롭 전 회전 각도 |
| `rotation_angle` | number | ❌ | 0 | 크롭 후 회전 각도 |

### `image_crop` 서비스 (고급)
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|-------|------|
| `input_image` | string | ✅ | - | 입력 이미지 경로 |
| `output_image` | string | ✅ | - | 출력 이미지 경로 |
| `left` | number | 수동시 ✅ | - | 크롭 시작 X 좌표 |
| `top` | number | 수동시 ✅ | - | 크롭 시작 Y 좌표 |
| `right` | number | 수동시 ✅ | - | 크롭 끝 X 좌표 |
| `bottom` | number | 수동시 ✅ | - | 크롭 끝 Y 좌표 |
| `rotation_angle_before` | number | ❌ | 0 | 크롭 전 회전 각도 |
| `rotation_angle` | number | ❌ | 0 | 크롭 후 회전 각도 |
| `auto_detect` | boolean | ❌ | false | 자동 감지 모드 |

## Home Assistant 자동화 예시

### 기본 자동화 (30분마다 실행)
```yaml
automation:
  - alias: "가스 검침기 OCR"
    trigger:
      - platform: time_pattern
        minutes: "/30"
    action:
      - service: pyscript.gas_meter_crop
        data:
          input_image: "/config/www/gas_latest.jpg"
          output_image: "/config/www/gas_cropped.jpg"
      - service: ocr.perform_ocr
        data:
          image_path: "/config/www/gas_cropped.jpg"
          language: "kor+eng"
```

### ESP32-CAM 촬영 후 처리 자동화
```yaml
automation:
  - alias: "ESP32-CAM 촬영 후 처리"
    trigger:
      - platform: file
        files:
          - "/config/www/gas_latest.jpg"
    action:
      - service: pyscript.gas_meter_crop
        data:
          input_image: "/config/www/gas_latest.jpg"
          output_image: "/config/www/gas_ready_for_ocr.jpg"
      - service: ocr.perform_ocr
        data:
          image_path: "/config/www/gas_ready_for_ocr.jpg"
          language: "kor+eng"
```

## 문제 해결

### 일반적인 문제들

1. **자동 감지가 실패할 때**
   - 이미지의 조명이나 각도가 좋지 않은 경우 수동 크롭 사용을 고려하세요
   - `rotation_angle_before` 파라미터로 이미지 회전 조정

2. **OCR 정확도가 낮을 때**
   - 크롭된 이미지의 해상도가 충분한지 확인하세요
   - `image_resize` 서비스로 적절한 크기로 조정하세요

3. **OpenCV 관련 오류**
   - `requirements.txt`의 의존성을 다시 설치하세요
   - Python 버전 호환성을 확인하세요

### 로그 확인
```bash
# Home Assistant 로그에서 확인
tail -f /config/home-assistant.log | grep -i "pyscript\|gas_meter"
```

## 기술적 세부사항

### 자동 감지 알고리즘
1. **그레이스케일 변환**: 컬러 이미지를 명암으로 변환
2. **가우시안 블러**: 노이즈 제거
3. **엣지 검출**: Canny 알고리즘 사용
4. **윤곽선 찾기**: 숫자 디스플레이 영역 추출
5. **필터링**: 면적과 종횡비로 적합한 영역 선택

### 지원 이미지 형식
- JPEG
- PNG
- 기타 PIL/Pillow 지원 형식

## 성능 최적화

### 추천 설정값들
- **크롭 영역**: 감지된 영역의 110% 정도로 여유 공간 추가
- **이미지 크기**: OCR용으로는 800x400 픽셀 정도가 적당
- **회전 각도**: 카메라 설치 각도에 맞춰 -90, 0, 90도 중 선택

### 메모리 사용량
- 일반적인 가스 검침 이미지(1600x1200) 처리 시 약 50MB 메모리 사용
- 대량 처리 시 적절한 메모리 제한 설정 권장

## 버전 정보
- OpenCV: 4.8.1.78
- Pillow: 11.0.0
- Python: 3.9+

## 라이선스
이 프로젝트는 MIT 라이선스 하에 제공됩니다.
