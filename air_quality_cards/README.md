# 공기질 카드 (Air Quality Cards)

이 폴더는 공기질 측정기(1528)와 에어모니터 플러스의 각종 측정치별로 생성된 카드 파일들을 포함합니다.

## 📁 폴더 구조

```
air_quality_cards/
├── README.md (이 파일)
├── _card_template.yaml (카드 템플릿)
├── 1528/
│   ├── co2.yaml
│   ├── pm2_5.yaml
│   ├── pm10.yaml
│   ├── temperature.yaml
│   ├── humidity.yaml
│   ├── illuminance.yaml
│   └── voc.yaml
└── airmonitor/
    ├── co2.yaml
    ├── pm2_5.yaml
    ├── pm10.yaml
    ├── pm1.yaml
    ├── temperature.yaml
    ├── humidity.yaml
    └── odor.yaml
```

## 🎨 색상 코드

각 측정 항목별로 일관된 색상을 사용합니다:

| 측정 항목 | 색상 | 16진수 |
|---------|------|--------|
| CO₂ | 🟢 초록색 | #4CAF50 |
| PM2.5/PM10/PM1 | 🔵 파란색 | #2196F3 |
| 온도 | 🟡 주황색 | #FF9800 |
| 습도 | 🟣 보라색 | #9C27B0 |
| 조도 | 🟤 갈색 | #795548 |
| VOCs/냄새 | 🔴 빨강색 | #F44336 |

## 📊 사용 방법

대시보드에서 이 카드들을 사용하려면:

```yaml
# dashboard.yaml 또는 다른 대시보드 파일에서
cards:
  - !include air_quality_cards/1528/co2.yaml
  - !include air_quality_cards/1528/pm2_5.yaml
  - !include air_quality_cards/airmonitor/co2.yaml
  # ... 등등
```

## 🔧 카드 특징

- **반응형 디자인**: 다양한 화면 크기에 대응
- **동적 색상**: 측정치에 따라 색상이 변함
- **상태 표시**: 현재 상태(Good/Moderate/Poor 등)를 표시
- **프로그레스 바**: 시각적으로 측정값을 표현

## 📝 수정 팁

각 카드를 수정할 때는 같은 측정 항목의 다른 장치 카드도 동시에 수정하여 일관성을 유지하세요.
