# 공기질 카드 사용 예시

## 대시보드에 카드 추가하기

Home Assistant의 대시보드 YAML 파일에서 아래와 같이 카드를 포함시킬 수 있습니다.

### 기본 사용법

```yaml
# dashboard.yaml 또는 integrated_dashboard.yaml

type: sections
title: 공기질 모니터링
sections:
  - type: grid
    cards:
      # 공기질 측정기(1528) - CO2
      - !include air_quality_cards/1528/co2.yaml
      
      # 에어모니터 플러스 - CO2
      - !include air_quality_cards/airmonitor/co2.yaml
```

### 전체 센서를 포함한 예시

```yaml
# dashboard.yaml

type: sections
title: 공기질 센서 대시보드
sections:
  - type: heading
    heading: 공기질 측정기(1528)
    
  - type: grid
    cards:
      - !include air_quality_cards/1528/co2.yaml
      - !include air_quality_cards/1528/pm2_5.yaml
      - !include air_quality_cards/1528/pm10.yaml
      - !include air_quality_cards/1528/temperature.yaml
      - !include air_quality_cards/1528/humidity.yaml
      - !include air_quality_cards/1528/illuminance.yaml
      - !include air_quality_cards/1528/voc.yaml
  
  - type: heading
    heading: 에어모니터 플러스
    
  - type: grid
    cards:
      - !include air_quality_cards/airmonitor/co2.yaml
      - !include air_quality_cards/airmonitor/pm1.yaml
      - !include air_quality_cards/airmonitor/pm2_5.yaml
      - !include air_quality_cards/airmonitor/pm10.yaml
      - !include air_quality_cards/airmonitor/temperature.yaml
      - !include air_quality_cards/airmonitor/humidity.yaml
      - !include air_quality_cards/airmonitor/odor.yaml
```

### 측정 항목별 그룹화 예시

같은 측정 항목을 하나의 섹션에 모으는 방법:

```yaml
# dashboard.yaml

type: sections
title: 공기질 데이터 비교

sections:
  # CO2 비교
  - type: heading
    heading: CO₂ 수준 비교
    
  - type: grid
    columns: 2
    cards:
      - !include air_quality_cards/1528/co2.yaml
      - !include air_quality_cards/airmonitor/co2.yaml
  
  # 미세먼지 비교
  - type: heading
    heading: 미세먼지 수준 비교
    
  - type: grid
    columns: 3
    cards:
      - !include air_quality_cards/1528/pm2_5.yaml
      - !include air_quality_cards/1528/pm10.yaml
      - !include air_quality_cards/airmonitor/pm2_5.yaml
      - !include air_quality_cards/airmonitor/pm10.yaml
      - !include air_quality_cards/airmonitor/pm1.yaml
  
  # 환경 데이터
  - type: heading
    heading: 환경 데이터
    
  - type: grid
    columns: 2
    cards:
      - !include air_quality_cards/1528/temperature.yaml
      - !include air_quality_cards/airmonitor/temperature.yaml
      - !include air_quality_cards/1528/humidity.yaml
      - !include air_quality_cards/airmonitor/humidity.yaml
```

## 색상 가이드

| 측정 항목 | 카드 색상 | 파일 위치 |
|---------|---------|---------|
| CO₂ | 🟢 초록색 | `1528/co2.yaml`, `airmonitor/co2.yaml` |
| PM2.5 | 🔵 파란색 | `1528/pm2_5.yaml`, `airmonitor/pm2_5.yaml` |
| PM10 | 🔵 파란색 | `1528/pm10.yaml`, `airmonitor/pm10.yaml` |
| PM1 | 🔵 파란색 | `airmonitor/pm1.yaml` |
| 온도 | 🟡 주황색 | `1528/temperature.yaml`, `airmonitor/temperature.yaml` |
| 습도 | 🟣 보라색 | `1528/humidity.yaml`, `airmonitor/humidity.yaml` |
| 조도 | 🟤 갈색 | `1528/illuminance.yaml` |
| VOC | 🔴 빨강색 | `1528/voc.yaml` |
| 냄새 | 🔴 빨강색 | `airmonitor/odor.yaml` |

## 카드 수정하기

각 카드의 임계값(thresholds)을 조정하려면 해당 YAML 파일의 `state_data` 섹션을 수정하세요:

```yaml
# 예: CO2 임계값 조정 (1528/co2.yaml)
const thresholds = [1400, 1000, 0];  # [Poor, Moderate, Good]
```

- **첫 번째 값**: Poor 이상의 기준
- **두 번째 값**: Moderate 이상의 기준  
- **세 번째 값**: Good 이상의 기준 (보통 0)

## 스타일 커스터마이징

각 카드의 `styles` 섹션에서 다음을 조정할 수 있습니다:

- `height`: 카드의 높이
- `font-size`: 텍스트 크기
- `padding`: 여백

```yaml
styles:
  card:
    - height: 160px  # 카드 높이 조정
  label:
    - font-size: 2em  # 라벨 크기 조정
```

## 문제 해결

### 카드가 나타나지 않음
- 센서 엔티티가 Home Assistant에서 사용 가능한지 확인하세요
- `@test.yaml` 파일에서 엔티티 ID를 확인하세요

### 임계값이 작동하지 않음
- YAML 문법 오류를 확인하세요
- 수치 비교 연산자(`>=`)를 확인하세요

### 색상이 변경되지 않음
- 브라우저 캐시를 삭제하세요
- Home Assistant를 다시 로드하세요

