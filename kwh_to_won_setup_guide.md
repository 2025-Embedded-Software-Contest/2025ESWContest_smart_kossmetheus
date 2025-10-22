# kwh_to_won 통합 설정 가이드

CareDian 프로젝트의 Home Assistant에서 전기 요금을 자동으로 계산하기 위한 `kwh_to_won` 통합 설정 가이드입니다.

## 📋 설정 구조

### 1️⃣ 월간 누적 사용량 센서 - `utility_meter`

**역할**: 매달 30일(검침일)에 리셋되는 누적 전력 사용량 센서

```yaml
utility_meter:
  electricity_energy_monthly:
    source: sensor.electricity_energy          # 원본 에너지 센서
    cycle: monthly                              # 월간 주기
    offset:
      days: 10                                  # 매달 30일 리셋 (20일 - 10일)
```

**설명**:
- `source`: 전력 에너지를 제공하는 센서 (kWh 단위)
- `cycle: monthly`: 1개월 주기로 리셋
- `offset: days: 10`: 검침일이 매달 20~30일인 경우, 오프셋 10일을 적용하면 매달 30일 0시 0분에 리셋됨

**생성되는 엔티티**:
- `sensor.electricity_energy_monthly`: 현재 월간 사용량
- 속성 `last_period`: 이전 달 사용량

### 2️⃣ 전월 사용량 센서 - `template` 센서

**역할**: 이전 달의 전력 사용량을 추적

```yaml
template:
  - sensor:
      - name: "electricity_energy_prev_monthly"
        unique_id: "electricity_energy_prev_monthly"
        state: "{{ state_attr('sensor.electricity_energy_monthly','last_period') | round(1) }}"
        unit_of_measurement: kWh
        device_class: energy
        attributes:
          state_class: total
```

**설명**:
- `utility_meter`의 `last_period` 속성을 이용하여 이전 달 사용량을 현재 값으로 표시
- 매달 1일 경과 시 이전 달의 누적값으로 업데이트됨
- `state_class: total`: 누적 에너지 값임을 명시

**생성되는 엔티티**:
- `sensor.electricity_energy_prev_monthly`: 이전 달 사용량

### 3️⃣ 전전월 사용량 저장소 - `input_number`

**역할**: 2개월 전 전력 사용량을 저장

```yaml
input_number:
  electricity_energy_prev2_monthly:
    name: "전기 전전월 사용량"
    unit_of_measurement: "kWh"
    icon: mdi:lightning-bolt
    min: 0
    max: 9999
    step: 0.01
    mode: box
```

**설명**:
- 월간 사용량 변경 시 자동으로 업데이트 (자동화 참조)
- 사용자가 수동으로 편집할 수도 있음
- 년-대-년(YoY) 비교 또는 3개월 추이 분석에 사용

**생성되는 엔티티**:
- `input_number.electricity_energy_prev2_monthly`: 2개월 전 사용량

### 4️⃣ 월간 사용량 자동 업데이트 - `automation`

**역할**: 전월 사용량 변경 시 자동으로 전전월 값 업데이트

```yaml
automation:
  - id: 'electricity_energy_prev2_monthly_update'
    alias: 전기 전전월 사용량 업데이트
    description: '전월 전기 사용량 변경 시 전전월 값을 업데이트'
    trigger:
      - platform: state
        entity_id:
          - sensor.electricity_energy_prev_monthly
    condition:
      - condition: template
        value_template: '{{ trigger.to_state.state|float(0) > 0 and trigger.from_state.state|float(0) > 0 }}'
    action:
      - service: input_number.set_value
        data:
          value: '{{ trigger.from_state.state }}'
        target:
          entity_id: input_number.electricity_energy_prev2_monthly
    mode: single
```

**설명**:
- `trigger`: `sensor.electricity_energy_prev_monthly` 변경 감지
- `condition`: 전월 사용량이 0을 초과할 때만 실행 (유효한 데이터 확인)
- `action`: 이전 상태(from_state)를 `input_number.electricity_energy_prev2_monthly`에 저장
- 자동으로 달마다 변경 기록을 유지

## 🔧 적용 단계

### Step 1: 에너지 센서 확인

먼저 `sensor.electricity_energy` 센서가 존재하는지 확인하세요.

**SmartThings 예시**:
```yaml
# SmartThings 통합에서 제공하는 에너지 센서
sensor.tv_energy
sensor.refrigerator_energy
```

**Zigbee 예시**:
```yaml
# Zigbee 스마트 플러그
sensor.smart_plug_energy
```

만약 에너지 센서가 없다면:
1. SmartThings, Zigbee, Z-Wave 등 에너지 모니터링 장비 추가
2. 에너지 센서 엔티티 ID 확인
3. 위 설정의 `source` 값을 실제 센서 ID로 변경

### Step 2: 검침일 확인 및 offset 조정

검침일에 따라 `utility_meter`의 `offset` 값을 조정하세요.

**예시**:
- 검침일 20일 → `offset: days: 10` (20 + 10 = 30)
- 검침일 30일 → `offset: days: 0` (30 + 0 = 30)
- 검침일 1일 → `offset: days: 29` (1 + 29 = 30)

### Step 3: YAML 파일 리로드

Home Assistant에서 설정 변경 후 리로드:

1. **UI에서**:
   - Settings → Developer Tools → YAML
   - "Check Configuration" 클릭
   - 오류 없으면 "Reload YAML" 클릭

2. **또는 명령어로**:
   ```bash
   # Home Assistant CLI 또는 SSH
   ha core check-config
   ha core reload
   ```

### Step 4: kwh_to_won 통합 설치

HACS를 통해 설치:

1. HACS → Integrations
2. "kwh_to_won" 검색 및 설치
3. Home Assistant 재시작
4. Settings → Devices & Services → Create Integration
5. kwh_to_won 선택 및 설정

### Step 5: 센서 동작 확인

설정 후 다음을 확인하세요:

```
Home Assistant UI → Developer Tools → States

Entity ID                                   | State    | Unit
-------------------------------------------|----------|------
sensor.electricity_energy                  | 123.45   | kWh
sensor.electricity_energy_monthly          | 45.67    | kWh
sensor.electricity_energy_prev_monthly     | 52.34    | kWh
input_number.electricity_energy_prev2_m... | 48.12    | kWh
```

## 📊 대시보드 카드 예시

### Energy Usage Card

```yaml
type: vertical-stack
cards:
  - type: statistic
    entity: sensor.electricity_energy
    stat_type: total_increase
    period: month
    title: "이번 달 전기 사용량"
  
  - type: history-stats
    title: "월별 사용량"
    entities:
      - entity: sensor.electricity_energy
    stat_type: total_increasing
    period: month
    format: "/5"

  - type: statistic
    entity: sensor.electricity_energy_prev_monthly
    stat_type: last_changed
    title: "지난 달 전기 사용량"

  - type: gauge
    entity: sensor.electricity_energy_monthly
    min: 0
    max: 500
    title: "월간 누적 사용량"
```

## ⚠️ 주의사항

1. **초기 데이터 없음**: 첫 달에는 `last_period` 데이터가 없을 수 있습니다.
2. **센서 업데이트 지연**: 에너지 센서 업데이트 주기에 따라 약간의 지연 발생 가능
3. **offset 설정**: 잘못된 offset은 리셋 시간 오류 초래
4. **자동화 조건**: 0 이상의 값일 때만 업데이트되도록 설정 (유효성 검증)

## 🔗 참고 자료

- [Home Assistant Utility Meter 공식 문서](https://www.home-assistant.io/integrations/utility_meter/)
- [Home Assistant Template Sensor](https://www.home-assistant.io/docs/configuration/templating/)
- [kwh_to_won GitHub](https://github.com/dugurs/kwh_to_won)

## 💾 설정 파일 백업

변경 전 백업을 생성했습니다:
```bash
git tag
# backup-20251022-154835 확인
```

문제 발생 시 다음 명령으로 이전 버전 복원 가능:
```bash
git checkout backup-20251022-154835 -- configuration.yaml templates.yaml automations.yaml
```
