# 🔧 Home Assistant Unavailable 엔티티 수정 가이드

## ✅ 완료된 수정 사항

### 1. 설정 파일 개선 (`configuration.yaml`)
- **Xbox 통합 로그 레벨**: `critical`로 변경하여 타임아웃 에러 최소화
- **LG ThinQ 로그 레벨**: `debug`로 변경하여 문제 진단 강화  
- **BLE Monitor 로그 레벨**: `info`로 변경하여 연결 상태 모니터링
- **김치냉장고 온도 센서**: 개선된 fallback 로직 및 상세 속성 추가

### 2. 자동화 시스템 추가
- **`fix_unavailable_entities.yaml`**: 30분마다 자동 복구 시도
- **`enhanced_diagnostics.yaml`**: 10분마다 상세 진단 및 분류
- **기존 `diagnostics_unavailable.yaml`**: 15분마다 기본 알림 유지

### 3. 복구 스크립트 추가 (`scripts/bluetooth_recovery.yaml`)
- **`bluetooth_adapter_reset`**: BLE 센서 복구용
- **`thinq_integration_reload`**: LG ThinQ 통합 재로드
- **`apple_devices_battery_check`**: iCloud3/Apple 기기 점검

## 🚀 다음 실행 단계

### A. Home Assistant 재시작 (필수)
```bash
# Home Assistant 재시작하여 새 설정 적용
# 설정 > 서버 제어 > 재시작 또는:
sudo systemctl restart home-assistant@homeassistant
```

### B. 통합별 수정 작업

#### 1. LG ThinQ (김치냉장고) 🧊
**우선순위: 최고**

1. **설정 > 통합 > LG ThinQ SmartThings Sensors**
2. **"재구성" 클릭**
3. **LG 계정 재로그인**
4. **기기 재검색 및 재등록**

또는 스크립트 실행:
```yaml
# 설정 > 스크립트 > thinq_integration_reload 실행
```

#### 2. iCloud3 (Apple 기기) 🍎  
**우선순위: 높음**

1. **설정 > 통합 > iCloud3**
2. **iCloud 계정 2단계 인증 토큰 갱신**
3. **각 Apple 기기에서 Home Assistant Companion 앱 확인**
4. **"나의 찾기" 설정 활성화 확인**

또는 스크립트 실행:
```yaml  
# 설정 > 스크립트 > apple_devices_battery_check 실행
```

#### 3. BLE Monitor (블루투스) 📡
**우선순위: 중간**

1. **BLE 장치들 물리적 재부팅** (심박수계, 칫솔 등)
2. **스크립트 실행**: `bluetooth_adapter_reset`
3. **필요시 BLE Monitor 통합 재설정**

#### 4. Xbox 통합 🎮
**우선순위: 낮음 (선택사항)**

Xbox 통합 완전 비활성화를 위해:
1. **설정 > 통합 > Xbox** 
2. **"통합 삭제"** 선택
3. 또는 로그 레벨을 `critical`로 변경한 상태로 유지

### C. 모니터링 및 검증

#### 1. 실시간 상태 확인
- **개발자 도구 > 상태**: `unavailable` 필터링
- **새 센서**: `sensor.unavailable_entities_count` 모니터링
- **김치냉장고**: `sensor.kimchi_fridge_avg_temperature` 속성 확인

#### 2. 알림 확인  
- **기본 진단**: 15분마다 (기존)
- **향상된 진단**: 10분마다 (새로 추가)
- **자동 복구**: 30분마다 (새로 추가)

#### 3. 로그 확인
```bash
# Home Assistant 로그 실시간 모니터링
tail -f /config/home-assistant.log | grep -i "thinq\|ble\|unavailable"
```

## 📊 예상 결과

### 수정 전 vs 수정 후
| 항목 | 수정 전 | 수정 후 (예상) |
|------|---------|----------------|
| 김치냉장고 온도 센서 | 4개 unavailable | 0-1개 unavailable |
| Apple 배터리 센서 | 2-4개 unavailable | 0-1개 unavailable |
| BLE 센서 | 3-6개 unavailable | 0-2개 unavailable |
| Xbox 엔티티 | 다수 unavailable | 0개 (비활성화) |
| **전체 unavailable** | **15-25개** | **5개 이하** |

### 시스템 개선사항
- ✅ **자동 진단**: 10분마다 상세 분석
- ✅ **자동 복구**: 30분마다 복구 시도  
- ✅ **분류 알림**: 통합별 맞춤 해결책 제공
- ✅ **향상된 fallback**: 김치냉장고 온도 센서 안정성 증대

## ⚠️ 주의사항

1. **엔티티 ID 변경 가능성**: 
   - LG ThinQ 재설정 시 일부 엔티티 ID가 변경될 수 있음
   - 대시보드 및 자동화 업데이트 필요할 수 있음

2. **Apple 2단계 인증**: 
   - 새 앱 전용 암호 생성 필요할 수 있음
   - iCloud 계정 설정 확인 필요

3. **BLE 장치 재페어링**:
   - MAC 주소 변경 가능성
   - 새 엔티티 생성될 수 있음

## 🆘 문제 해결

### 여전히 unavailable 엔티티가 많다면:

1. **Home Assistant 완전 재시작**
```bash
sudo systemctl restart home-assistant@homeassistant
```

2. **통합 재설치**
   - 해당 통합 완전 삭제 후 재설치

3. **설정 백업 복구**
   - 문제 발생 시 이전 설정으로 롤백

4. **전문가 지원 요청**
   - Home Assistant Community 포럼
   - Discord 채널 활용

---

## 📞 지원 정보

- **분석 보고서**: `UNAVAILABLE_ENTITIES_ANALYSIS.md`
- **스크립트 위치**: `scripts/bluetooth_recovery.yaml`  
- **자동화 위치**: `automations/fix_unavailable_entities.yaml`, `automations/enhanced_diagnostics.yaml`
- **로그 확인**: 설정 > 시스템 > 로그

**수정 완료 후 이 가이드는 보관용으로 유지하세요!** 📚
