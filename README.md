# CareDian Backend - Home Assistant Configuration

이 저장소는 CareDian 프로젝트의 Home Assistant 설정 파일들을 관리합니다.

## 주요 통합 요소(Integrations)

### kwh_to_won (전기 요금 계산)

전기 사용량을 기반으로 월간 전기료를 자동 계산하는 통합입니다.

#### 설정 개요

**1. 월간 누적 사용량 센서 (`electricity_energy_monthly`)**
- `utility_meter`를 통해 생성
- 매달 30일 0시 0분에 리셋
- 검침 시작일에 맞춘 설정 (offset: 10일)

```yaml
utility_meter:
  electricity_energy_monthly:
    source: sensor.electricity_energy
    cycle: monthly
    offset:
      days: 10
```

**2. 전월 사용량 센서 (`sensor.electricity_energy_prev_monthly`)**
- Template 센서로 이전 달의 사용량 추적
- `utility_meter`의 `last_period` 속성을 사용

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

**3. 전전월 사용량 저장소 (`input_number.electricity_energy_prev2_monthly`)**
- 전전월 사용량을 수동으로 저장
- 자동화를 통해 자동 업데이트

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

**4. 자동화 - 월간 사용량 자동 업데이트**
- 전월 사용량 변경 시 자동으로 전전월 값 업데이트

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

#### 필수 요구사항

- Home Assistant 2024.1 이상
- `sensor.electricity_energy` 에너지 센서 필수
  - 누적 전력 사용량을 kWh 단위로 제공해야 함
  - SmartThings, Zigbee, 또는 기타 에너지 모니터링 장비에서 제공 가능

#### 사용 방법

1. **초기 설정**
   - `sensor.electricity_energy` 에너지 센서 확인
   - 검침일에 맞춰 `offset` 값 조정
   - configuration.yaml 리로드

2. **kwh_to_won 통합 적용**
   - HACS를 통해 kwh_to_won 설치
   - 대시보드에서 전기 요금 자동 계산

3. **모니터링**
   - 월간 누적 사용량: `sensor.electricity_energy_monthly`
   - 전월 사용량: `sensor.electricity_energy_prev_monthly`
   - 전전월 사용량: `input_number.electricity_energy_prev2_monthly`

## 파일 구조

- `configuration.yaml` - 메인 설정 파일
- `automations.yaml` - 자동화 규칙
- `templates.yaml` - 템플릿 센서 정의
- `scripts.yaml` - 스크립트 정의
- `sensors.yaml` - 센서 정의
- `groups.yaml` - 엔티티 그룹
- `lights.yaml` - 조명 설정
- `themes/` - UI 테마
- `custom_components/` - 커스텀 통합 요소
- `esphome/` - ESPHome 기기 설정
- `pyscript/` - PyScript 자동화 스크립트
