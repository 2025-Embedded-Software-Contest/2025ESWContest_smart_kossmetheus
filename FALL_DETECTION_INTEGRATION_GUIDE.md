# 낙상 감지 시스템 연동 가이드

## 개요
이 가이드는 FastAPI 백엔드와 Home Assistant를 연동하여 낙상 감지 이벤트를 처리하는 방법을 설명합니다.

## Home Assistant 설정

### 1. 가상 엔티티 생성 완료
`configuration.yaml`에 다음 엔티티들이 추가되었습니다:

#### Input Boolean
- **Entity ID**: `input_boolean.fall_triggered`
- **이름**: 낙상 감지 트리거
- **용도**: FastAPI에서 낙상 이벤트 발생 시 상태를 변경하는 트리거

#### Binary Sensor
- **Entity ID**: `binary_sensor.fall_detected`
- **이름**: 낙상 감지 센서
- **용도**: `input_boolean.fall_triggered`의 상태를 기반으로 낙상 감지 여부를 표시
- **Device Class**: safety (안전 관련 센서)
- **아이콘**: 
  - ON 상태: `mdi:alert-circle` (경고)
  - OFF 상태: `mdi:check-circle` (정상)

## FastAPI 연동 방법

### 1. 필요한 설정
Home Assistant의 **장기 액세스 토큰(Long-Lived Access Token)**이 필요합니다.

#### 토큰 생성 방법:
1. Home Assistant 웹 UI에 로그인
2. 프로필 아이콘 클릭 (좌측 하단)
3. 하단의 "장기 액세스 토큰" 섹션으로 스크롤
4. "토큰 생성" 버튼 클릭
5. 토큰 이름 입력 (예: "FastAPI Fall Detection")
6. 생성된 토큰을 안전하게 복사 및 보관

### 2. FastAPI 코드 예제

#### 낙상 이벤트 트리거 (ON)
```python
import httpx
from typing import Optional

class HomeAssistantClient:
    def __init__(self, base_url: str, access_token: str):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
    
    async def trigger_fall_event(self) -> bool:
        """낙상 감지 이벤트를 트리거합니다."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/services/input_boolean/turn_on",
                    headers=self.headers,
                    json={"entity_id": "input_boolean.fall_triggered"},
                    timeout=10.0
                )
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"낙상 이벤트 트리거 실패: {e}")
            return False
    
    async def reset_fall_event(self) -> bool:
        """낙상 감지 상태를 초기화합니다."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/services/input_boolean/turn_off",
                    headers=self.headers,
                    json={"entity_id": "input_boolean.fall_triggered"},
                    timeout=10.0
                )
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"낙상 상태 초기화 실패: {e}")
            return False
    
    async def get_fall_status(self) -> Optional[dict]:
        """현재 낙상 감지 상태를 조회합니다."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/states/binary_sensor.fall_detected",
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"낙상 상태 조회 실패: {e}")
            return None

# 사용 예제
ha_client = HomeAssistantClient(
    base_url="http://homeassistant.local:8123",
    access_token="YOUR_LONG_LIVED_ACCESS_TOKEN_HERE"
)

# 낙상 감지 시
await ha_client.trigger_fall_event()

# 상태 조회
status = await ha_client.get_fall_status()
if status:
    print(f"낙상 감지 상태: {status['state']}")

# 상태 초기화
await ha_client.reset_fall_event()
```

#### FastAPI 엔드포인트 예제
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class FallDetectionEvent(BaseModel):
    detected: bool
    confidence: float
    timestamp: str

@app.post("/api/fall-detection")
async def handle_fall_detection(event: FallDetectionEvent):
    """낙상 감지 이벤트를 처리합니다."""
    if event.detected and event.confidence > 0.8:
        # Home Assistant에 낙상 이벤트 전송
        success = await ha_client.trigger_fall_event()
        if success:
            return {"message": "낙상 이벤트가 Home Assistant에 전송되었습니다."}
        else:
            raise HTTPException(status_code=500, detail="Home Assistant 연동 실패")
    return {"message": "낙상 감지 신뢰도가 낮아 무시되었습니다."}

@app.post("/api/fall-detection/reset")
async def reset_fall_detection():
    """낙상 감지 상태를 초기화합니다."""
    success = await ha_client.reset_fall_event()
    if success:
        return {"message": "낙상 감지 상태가 초기화되었습니다."}
    else:
        raise HTTPException(status_code=500, detail="초기화 실패")
```

### 3. 환경 변수 설정 예제
```bash
# .env 파일
HA_BASE_URL=http://homeassistant.local:8123
HA_ACCESS_TOKEN=your_long_lived_access_token_here
```

```python
# settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ha_base_url: str
    ha_access_token: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Home Assistant 자동화 예제

낙상 감지 시 알림을 보내는 자동화를 추가할 수 있습니다:

```yaml
# automations.yaml 또는 automations/ 폴더에 추가
- id: fall_detection_notification
  alias: "낙상 감지 알림"
  description: "낙상이 감지되면 알림을 전송합니다"
  trigger:
    - platform: state
      entity_id: binary_sensor.fall_detected
      to: "on"
  action:
    - service: notify.mobile_app_your_device
      data:
        title: "⚠️ 낙상 감지"
        message: "낙상이 감지되었습니다. 즉시 확인이 필요합니다."
        data:
          priority: high
          notification_icon: "mdi:alert-circle"
    # TTS 알림 (선택사항)
    - service: tts.google_translate_say
      data:
        entity_id: media_player.uhyeonibang
        message: "낙상이 감지되었습니다. 확인이 필요합니다."
```

## 테스트 방법

### 1. Home Assistant에서 직접 테스트
Home Assistant 개발자 도구에서:
```yaml
# Services 탭에서 실행
service: input_boolean.turn_on
target:
  entity_id: input_boolean.fall_triggered
```

### 2. curl을 사용한 API 테스트
```bash
# 낙상 이벤트 트리거
curl -X POST \
  http://homeassistant.local:8123/api/services/input_boolean/turn_on \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_boolean.fall_triggered"}'

# 상태 조회
curl -X GET \
  http://homeassistant.local:8123/api/states/binary_sensor.fall_detected \
  -H "Authorization: Bearer YOUR_TOKEN"

# 상태 초기화
curl -X POST \
  http://homeassistant.local:8123/api/services/input_boolean/turn_off \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "input_boolean.fall_triggered"}'
```

## 주의사항

1. **보안**: 
   - 액세스 토큰은 절대 코드에 하드코딩하지 마세요
   - 환경 변수나 비밀 관리 시스템을 사용하세요
   - 토큰이 노출되면 즉시 재생성하세요

2. **네트워크**:
   - Home Assistant가 FastAPI 서버에서 접근 가능한지 확인하세요
   - 방화벽 설정을 확인하세요
   - HTTPS 사용을 권장합니다

3. **오류 처리**:
   - API 호출 실패 시 재시도 로직을 구현하세요
   - 타임아웃을 적절히 설정하세요
   - 에러 로깅을 구현하세요

4. **성능**:
   - 과도한 API 호출을 피하세요
   - 필요시 디바운싱/쓰로틀링을 구현하세요

## 재시작 필요

설정 변경 후 Home Assistant를 재시작해야 합니다:
- **설정** → **시스템** → **재시작** 클릭
- 또는 CLI: `ha core restart`

## 문제 해결

### 센서가 보이지 않을 때
1. Home Assistant 재시작 확인
2. 개발자 도구 → 상태에서 `input_boolean.fall_triggered` 검색
3. 로그 확인: `configuration.yaml` 구문 오류 확인

### API 호출이 실패할 때
1. 액세스 토큰이 유효한지 확인
2. Home Assistant URL이 올바른지 확인
3. `trusted_proxies` 설정 확인 (프록시 사용 시)
4. 네트워크 연결 확인

### 자동화가 작동하지 않을 때
1. 자동화가 활성화되어 있는지 확인
2. 트리거 조건 확인
3. Home Assistant 로그 확인

