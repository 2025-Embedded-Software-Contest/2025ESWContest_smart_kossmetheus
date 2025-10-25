# Energy Dashboard Cards

이 디렉토리에는 Home Assistant Energy 대시보드에 사용할 수 있는 개별 카드 파일들이 포함되어 있습니다.

## 📁 파일 구조

각 카드는 독립적인 YAML 파일로 분리되어 있어 필요한 카드만 선택적으로 사용할 수 있습니다:

1. **01_overview_heading.yaml** - Energy Overview 제목 카드
2. **02_distribution.yaml** - 에너지 분배 카드
3. **03_usage_heading.yaml** - Energy Usage 제목 카드
4. **04_date_selection.yaml** - 날짜 선택 카드
5. **05_usage_graph.yaml** - 에너지 사용량 그래프
6. **06_sources_table.yaml** - 에너지 소스 테이블
7. **07_solar_heading.yaml** - Solar 제목 카드
8. **08_solar_graph.yaml** - 태양광 그래프
9. **09_solar_consumed_gauge.yaml** - 태양광 소비 게이지
10. **10_self_sufficiency_gauge.yaml** - 자급자족률 게이지
11. **11_sensors_heading.yaml** - Sensors 제목 카드
12. **12_sensors_entities.yaml** - 에너지 센서 엔티티 목록

## 🔧 사용 방법

### 방법 1: 개별 카드로 대시보드에 추가

각 YAML 파일의 내용을 복사하여 Lovelace 대시보드에 직접 붙여넣을 수 있습니다:

```yaml
# dashboard.yaml 또는 UI 에디터에서
views:
  - title: Energy
    type: sections
    sections:
      # 01_overview_heading.yaml의 내용
      - type: grid
        cards:
          - type: heading
            icon: mdi:lightning-bolt
            heading: Overview
            heading_style: title
      
      # 02_distribution.yaml의 내용
      - type: grid
        cards:
          - type: energy-distribution
            link_dashboard: true
      
      # ... 나머지 카드들
```

### 방법 2: 전체 Energy 탭 구성 (원본 test.yaml 참고)

모든 카드를 한 번에 사용하려면:

```yaml
views:
  - title: Energy
    type: sections
    max_columns: 3
    path: energy
    icon: mdi:lightning-bolt
    theme: Rounded-Bubble
    sections:
      # 여기에 각 카드 파일의 내용을 순서대로 추가
```

### 방법 3: 선택적 사용

필요한 카드만 선택하여 사용할 수 있습니다. 예를 들어 Solar 관련 카드를 제외하려면:

- `07_solar_heading.yaml`
- `08_solar_graph.yaml`
- `09_solar_consumed_gauge.yaml`
- `10_self_sufficiency_gauge.yaml`

위 파일들을 제외하고 나머지만 사용하면 됩니다.

## 📝 커스터마이징

### 센서 엔티티 변경

`12_sensors_entities.yaml` 파일에서 자신의 Home Assistant 센서에 맞게 엔티티 ID를 수정하세요:

```yaml
entities:
  - entity: sensor.sihas_energy_monitor_power  # 여기를 자신의 센서로 변경
    name: Current Power (W)
  # ... 나머지 센서들
```

### 테마 변경

전체 Energy 탭에 테마를 적용하려면 view 레벨에서 설정:

```yaml
- title: Energy
  type: sections
  theme: Rounded-Bubble  # 원하는 테마로 변경
```

### 컬럼 수 조정

```yaml
- title: Energy
  type: sections
  max_columns: 3  # 1~4 사이의 값으로 조정 가능
```

## ⚠️ 주의사항

1. **Energy 대시보드 설정 필요**: Home Assistant의 Energy 대시보드가 먼저 설정되어 있어야 카드들이 제대로 작동합니다.
   - 설정 > 대시보드 > 에너지 > 에너지 구성

2. **센서 엔티티 확인**: `12_sensors_entities.yaml`의 센서 엔티티 ID가 실제로 존재하는지 확인하세요.

3. **Solar 카드**: 태양광 발전 시스템이 없다면 Solar 관련 카드(07~10)는 제거하는 것이 좋습니다.

## 📦 UI 편집기용 완성 파일

UI 편집기의 "구성 코드 편집하기"에 바로 붙여넣을 수 있는 완성된 파일도 제공됩니다:

### energy_tab_formatted.yaml (전체 버전)
모든 섹션(Overview, Energy Usage, Solar, Sensors)이 포함된 완성 버전입니다.

**특징:**
- `max_columns: 4` 설정
- 각 섹션이 vertical-stack으로 그룹화
- `grid_options: columns: 12, rows: auto` 적용
- `column_span: 4` 로 전체 너비 사용
- Header 카드 포함

**사용법:**
1. Home Assistant UI에서 대시보드 편집 모드 진입
2. 우측 상단 ⋮ 메뉴 → "구성 코드 편집하기" 클릭
3. `views:` 섹션에 `energy_tab_formatted.yaml`의 내용 전체를 붙여넣기
4. 저장

### energy_tab_formatted_no_solar.yaml (Solar 제외 버전)
태양광 발전 시스템이 없는 경우 사용하는 버전입니다.

**포함 섹션:**
- Overview
- Energy Usage
- Sensors (Solar 섹션 제외)

## 🔄 원본 파일

전체 구성이 포함된 원본 파일은 `../test.yaml`에서 확인할 수 있습니다.

