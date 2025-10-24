# 통합 대시보드 가이드

## 📋 개요

`integrated_dashboard.yaml` 파일은 다음 두 대시보드를 통합한 것입니다:
- **test.yaml** (3,450줄): 현재 사용 중인 대시보드
- **dashboard.yaml** (27,878줄): jlnbln의 Bubble Card 템플릿

**파일 정보:**
- 총 라인 수: 31,337줄
- 파일 크기: 1.4MB
- 위치: `/config/integrated_dashboard.yaml`

## 🗂️ 파일 구조

```
integrated_dashboard.yaml
├── kiosk_mode (1-11줄)
├── decluttering_templates (12-70줄)
├── navbar-templates (71-290줄)
├── button_card_templates (291-4428줄)
└── views (4429줄~끝)
    ├── test.yaml의 views (활성화됨)
    │   ├── Home (평면도 기반)
    │   ├── 거실
    │   └── Weather
    └── dashboard.yaml의 views (주석 처리됨)
        ├── Home
        ├── Music
        ├── Security
        ├── Energy
        ├── Server
        └── Shopping List
```

## ✅ 완료된 작업

1. ✅ Git 백업 태그 생성: `backup-20251024-205156`
2. ✅ dashboard.yaml의 템플릿 섹션 통합
3. ✅ Navbar URL 업데이트: `/dashboard-bubble/` → `/integrated-dashboard/`
4. ✅ test.yaml의 views 추가 (활성화 상태)
5. ✅ dashboard.yaml의 views 추가 (주석 처리)
6. ✅ Entity 매핑 주석 추가
7. ✅ configuration.yaml에 대시보드 등록
8. ✅ 필요한 리소스 추가

## 🔧 필요한 Entity 수정 사항

### 📌 사용 가능한 Entity 목록 (자동 감지됨)

**Person Entities:**
- `person.gimseonghyeog`
- `person.mrpc2003`
- `person.gimyeji`
- `person.iilhwan`
- `person.jeonyecan`

**Media Players:**
- `media_player.samsung_tv2`
- `media_player.spotify_gimuhyeon`
- `media_player.uhyeonibang`

**Climate:**
- `climate.seutaendeuhyeong_eeokeon`

### ⚠️ 수정이 필요한 Entity (dashboard.yaml에서 가져온 것들)

파일에서 `# ⚠️ 수정 필요:` 주석을 찾아 다음 entity들을 교체하세요:

#### 1. Person Entities
```yaml
# 원본
person.julian  # ⚠️ 수정 필요
person.anna    # ⚠️ 수정 필요

# 교체 예시
person.gimseonghyeog
person.gimyeji
```

#### 2. 조명 관련
```yaml
# 수정 필요
light.all_lights           # → 전체 조명 그룹 생성 필요
sensor.lights_on_count     # → 켜진 조명 수 센서 생성 필요
```

#### 3. 미디어 플레이어
```yaml
# 원본 → 교체
media_player.music         # → media_player.spotify_gimuhyeon
media_player.tv_and_ps5    # → media_player.samsung_tv2
```

#### 4. 리모트 및 센서
```yaml
# 수정 필요 (없으면 해당 기능 비활성화)
remote.harmony_hub                      # → TV 리모트
binary_sensor.window_sensors            # → 창문 센서 그룹
sensor.window_open_count               # → 열린 창문 수
binary_sensor.monitored_entities       # → 모니터링 대상 센서
binary_sensor.battery_health_attention # → 배터리 경고 센서
```

#### 5. 사용자 정보
```yaml
# 원본
user.name != "Julian"  # ⚠️ 수정 필요
user.name != "Anna"    # ⚠️ 수정 필요

# 사용자 ID (UUID)
82def695e9504f63b1eb09150073737d  # ⚠️ 수정 필요
3eea636aa3de4c7f9c662ad29c6e92e0  # ⚠️ 수정 필요
```

**본인의 사용자 ID 확인 방법:**
1. Home Assistant → 설정 → 사람
2. 사용자 클릭
3. URL의 마지막 부분이 사용자 ID

#### 6. Addon URL
```yaml
/d5369777_music_assistant/ingress  # ⚠️ 수정 필요: Music Assistant URL
```

## 🎨 Navbar에 필요한 Views

dashboard.yaml의 navbar가 다음 view path들을 참조합니다. 현재는 주석 처리되어 있으므로, 필요 시 주석을 해제하고 entity를 수정하세요:

### 메인 Views
- `home` - 홈 뷰 (hash sections: living-room, bedroom, office, kitchen, bathroom, guest-room, corridor, remote, julian, anna)
- `music` - 음악 제어 뷰
- `energy` - 에너지 모니터링 뷰
- `security` - 보안/카메라 뷰
- `server` - 서버 관리 뷰
- `bring` - 쇼핑 리스트 뷰

## 📝 dashboard.yaml Views 활성화 방법

dashboard.yaml의 뷰들은 참고용으로 주석 처리되어 있습니다. 활성화하려면:

1. `integrated_dashboard.yaml` 파일 열기
2. 원하는 뷰 섹션 찾기 (약 7878줄 이후)
3. 주석(`  # `) 제거
4. Entity 참조를 본인 환경에 맞게 수정
5. Home Assistant 재시작

**예시:**
```yaml
# 주석 처리된 상태
  # - title: Music
  #   header:
  #     card:
  #       type: markdown

# 활성화 후
  - title: Music
    header:
      card:
        type: markdown
        content: |
          # 🎵 Music
```

## 🔍 Entity 수정 방법

### 방법 1: 파일 내 검색 및 교체
```bash
# person.julian을 person.gimseonghyeog로 교체
sed -i '' 's/person\.julian/person.gimseonghyeog/g' integrated_dashboard.yaml

# media_player.music를 media_player.spotify_gimuhyeon로 교체
sed -i '' 's/media_player\.music\b/media_player.spotify_gimuhyeon/g' integrated_dashboard.yaml
```

### 방법 2: 텍스트 에디터에서 직접 수정
1. VS Code나 다른 에디터로 `integrated_dashboard.yaml` 열기
2. `⚠️ 수정 필요` 검색
3. 각 항목을 본인 환경에 맞게 수정

## 🚀 활성화 및 테스트

### 1. Home Assistant 재시작
```bash
# 설정 검증
ha core check

# Home Assistant 재시작
ha core restart
```

### 2. 대시보드 확인
1. Home Assistant UI 접속
2. 사이드바에서 "통합 대시보드" 클릭
3. test.yaml의 뷰들이 정상 작동하는지 확인
4. dashboard.yaml 뷰를 사용하려면 주석 해제 및 entity 수정

## 📊 리소스 목록

다음 커스텀 카드들이 configuration.yaml에 등록되었습니다:

**기존 리소스:**
- button-card
- card-mod
- Bubble-Card
- mushroom
- state-switch
- stack-in-card
- vertical-stack-in-card
- apexcharts-card
- mini-graph-card
- multiple-entity-row
- mini-media-player
- battery-state-card
- timer-bar-card

**추가된 리소스:**
- navbar-card
- decluttering-card
- auto-entities
- expander-card
- css-swipe-card
- notify-card
- my-slider-v2
- layout-card

## 🐛 문제 해결

### 대시보드가 로드되지 않음
1. Home Assistant 로그 확인: `설정 > 시스템 > 로그`
2. YAML 구문 오류 확인: `개발자 도구 > YAML > 구성 확인`
3. 누락된 entity 확인: 로그에서 `entity not found` 검색

### Entity를 찾을 수 없음
1. `⚠️ 수정 필요` 주석이 있는 entity들을 확인
2. 본인 환경의 entity로 교체하거나
3. 해당 카드/뷰를 비활성화

### Navbar가 작동하지 않음
1. navbar-card 리소스가 로드되었는지 확인
2. `/hacsfiles/lovelace-navbar-card/navbar-card.js` 파일 존재 확인
3. 필요한 view path들이 생성되었는지 확인

## 📚 추가 정보

### test.yaml (현재 대시보드) Views
- ✅ 완전히 작동 가능
- ✅ Entity들이 모두 매핑됨
- ✅ 즉시 사용 가능

### dashboard.yaml (Bubble Card 템플릿) Views
- ⚠️ 주석 처리됨 (비활성화)
- ⚠️ Entity 수정 필요
- ⚠️ 선택적으로 활성화 가능

### 다음 단계 (선택사항)
1. dashboard.yaml의 원하는 뷰 활성화
2. Entity 매핑 완료
3. 테마 및 스타일 커스터마이징
4. test.yaml의 특정 뷰를 Bubble Card 스타일로 변환

## 💡 팁

1. **단계적 접근**: 한 번에 하나의 뷰만 활성화하고 테스트하세요
2. **백업**: `backup-20251024-205156` 태그로 언제든 되돌릴 수 있습니다
3. **로그 확인**: 수정 후 항상 Home Assistant 로그를 확인하세요
4. **Entity 생성**: 없는 entity는 Helper로 생성하거나 Template sensor로 만들 수 있습니다

## 📞 도움이 필요하면

- Home Assistant 로그에서 오류 메시지 확인
- 특정 카드나 기능이 작동하지 않으면 해당 부분을 주석 처리
- 원본 파일(`test.yaml`, `dashboard.yaml`)은 백업으로 보관되어 있음

---

**생성일**: 2024-10-24
**버전**: 1.0
**Git 백업 태그**: `backup-20251024-205156`

