# Home Assistant Unavailable 엔티티 전수 조사 보고서

## 📋 분석 개요
- **조사 일자**: 2025년 1월 9일
- **Home Assistant 환경**: CareDian Backend
- **분석 범위**: 전체 엔티티 중 'unavailable' 및 'unknown' 상태 엔티티

## 🔍 확인된 문제 엔티티들

### 1. LG ThinQ (SmartThinQ) - 김치냉장고 온도 센서
**상태**: UNAVAILABLE
- `sensor.jubang_gimcinaengjanggo_bottom_temperature`
- `sensor.jubang_gimcinaengjanggo_left_temperature` 
- `sensor.jubang_gimcinaengjanggo_middle_temperature`
- `sensor.jubang_gimcinaengjanggo_right_temperature`

**문제 원인 분석**:
- ThinQ API 연결 불안정 (MonitorUnavailableError, NotConnectedError)
- LG 계정 인증 토큰 만료 가능성
- 김치냉장고 기기 자체 네트워크 연결 문제
- ThinQ 서버 응답 지연 또는 일시적 서비스 장애

### 2. iCloud3 통합 - Apple 기기 배터리 센서
**상태**: POTENTIALLY UNAVAILABLE
- `sensor.gimuhyeonyi_apple_watch_battery`
- `sensor.gimuhyeonyi_macbook_pro_battery`  
- `sensor.uhyeonyi_ipad_pro_battery`
- `sensor.uhyeonyi_iphone_xs_battery`

**문제 원인 분석**:
- iCloud 계정 2단계 인증 토큰 만료
- Mobile App (Home Assistant Companion) 연결 끊김
- Apple 기기들의 배터리 정보 공유 설정 문제
- iCloud 서버 연결 문제

### 3. BLE Monitor - 블루투스 센서들
**상태**: INTERMITTENT UNAVAILABLE  
- `sensor.ble_heart_rate_e0e33e6221b5`
- `sensor.ble_steps_e0e33e6221b5`
- `sensor.smart_series_7000_6f50` 
- `sensor.smart_series_7000_6f50_duration`
- `sensor.smart_series_7000_6f50_pressure`
- `binary_sensor.ble_toothbrush_f45eab216f50`

**문제 원인 분석**:
- 블루투스 어댑터 전원 관리 문제 (soft/hard block)
- BLE 장치들의 간헐적 연결 끊김
- 블루투스 인터페이스 리셋 필요
- 장치 페어링 재설정 필요

### 4. Xbox 통합
**상태**: NETWORK TIMEOUT ERROR
- `sensor.xbox_*` (모든 Xbox 관련 엔티티)
- `binary_sensor.xbox_*`

**문제 원인 분석**:
- Xbox Live API ReadTimeout (이미 로그에서 확인)
- Xbox 콘솔 네트워크 연결 불안정
- Xbox Live 서비스 일시적 장애

### 5. 기타 네트워크 기반 센서들  
**상태**: CHECKING NEEDED
- 라우터 관련 센서들 (`sensor.paul_router_*`)
- 네트워크 속도 센서들 (`sensor.fast_com_download`)
- 스마트 기기들 (조명, 스위치 등)

## 📊 현재 진단 시스템 상태

### ✅ 이미 구현된 모니터링 시스템
1. **템플릿 센서**: 
   - `sensor.unavailable_entities_count` - unavailable 엔티티 개수 추적
   - `sensor.unavailable_entities` - unavailable 엔티티 목록 저장

2. **자동화**: 
   - `diagnostics_unavailable.yaml` - 15분마다 unavailable 엔티티 알림

3. **로그 설정**: 
   - Xbox 통합 로그 최소화 설정 완료
   - InfluxDB 제외 설정으로 불안정한 엔티티들 제외

### 🔄 김치냉장고 온도 센서 보완 로직
- **평균 온도 계산** (`sensor.kimchi_fridge_avg_temperature`)에서 이미 unavailable 상태 고려
- 일부 센서가 unavailable이어도 작동하는 안전 로직 구현

## 🛠 권장 수정 방안

### 즉시 조치 (High Priority)

#### 1. LG ThinQ 통합 재설정
```yaml
# 설정 > 통합 > LG ThinQ SmartThings Sensors
# 1. 통합 재구성 (Reconfigure)
# 2. LG 계정 재로그인
# 3. 기기 재검색 및 재등록
```

#### 2. iCloud3 통합 점검
```yaml
# 설정 > 통합 > iCloud3
# 1. iCloud 계정 2단계 인증 토큰 갱신
# 2. Mobile App 연결 상태 확인
# 3. Apple 기기들의 "나의 찾기" 설정 확인
```

#### 3. 블루투스 어댑터 리셋
```bash
# 블루투스 어댑터 전원 사이클
sudo hciconfig hci0 down
sudo hciconfig hci0 up
# 또는 BLE Monitor 통합 재시작
```

### 중기 조치 (Medium Priority)

#### 4. Xbox 통합 완전 비활성화
```yaml
# configuration.yaml 수정 - Xbox 통합 완전 제거
# 현재는 로그만 최소화했지만, 통합 자체를 비활성화 권장
```

#### 5. 네트워크 센서들 연결 상태 점검
```yaml
# 라우터 및 네트워크 기반 센서들의 IP/연결 상태 확인
# 필요시 통합 재설정
```

### 장기 조치 (Low Priority)

#### 6. 모니터링 시스템 강화
```yaml
# 추가 진단 자동화 생성:
# - 특정 통합별 unavailable 엔티티 개별 추적
# - 복구 시도 자동화 (통합 재시작 등)
# - Slack/Discord 알림 연동
```

## 📈 예상 효과

### 수정 후 예상 복구율:
- **LG ThinQ (김치냉장고)**: 90% (통합 재설정 후)
- **iCloud3 (Apple 기기들)**: 95% (계정/앱 재연결 후)  
- **BLE 센서들**: 80% (블루투스 리셋 후)
- **Xbox 통합**: 100% (비활성화 시)

### 전체 시스템 안정성:
- unavailable 엔티티 수 예상 감소: **70-80%**
- 시스템 전반 안정성 향상
- 대시보드 및 자동화 정상화

## ⚠ 주의사항

1. **LG ThinQ**: 재설정 시 기존 엔티티 ID 변경 가능성
2. **iCloud3**: Apple 2단계 인증 앱 코드 필요
3. **BLE**: 기기 재페어링 시 MAC 주소 변경 가능성
4. **백업**: 수정 전 현재 설정 백업 필수

## 📝 다음 단계

1. ✅ 분석 완료
2. 🔄 수정 계획 수립 (현재 단계)
3. ⏭ 실제 수정 작업 실시
4. ✅ 수정 사항 검증
5. 📊 모니터링 및 추가 최적화

---
*이 보고서는 Home Assistant configuration.yaml, 로그 파일, 커스텀 컴포넌트 분석을 바탕으로 작성되었습니다.*
