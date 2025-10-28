"""
모듈: /events/fall (낙상 이벤트 처리)
목적:
  - 센서/디바이스로부터 낙상 관련 이벤트(FallEvent)를 수신
  - LSTM 추론으로 보정 확률 산출 및 기록
  - InfluxDB(v1)에 이벤트 저장
  - Home Assistant(HA)로 모바일앱 푸시 알림 전송 및 후속 상태 업데이트
보안:
  - M2M JWT 스코프 필수: "events:fall:ingest"
외부 연동:
  - InfluxDB v1: write_point, (선택) 최근 movement 조회
  - Home Assistant: /api/services(서비스 목록), notify.mobile_app_* 알림, input_boolean.turn_on
주의:
  - _ai_over_cnt는 프로세스 로컬 상태이므로 멀티 워커/멀티 인스턴스 환경에서는 공유되지 않음
  - 네트워크 장애 대비 타임아웃/재시도/예외 처리 필요
"""

import httpx
import asyncio
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from collections import defaultdict

from app.core.rate_limit import should_alert
from app.core.config import settings  
from app.services import influx_v1 as influx
from app.services.ha_notify import send_fall_alert
from app.services.influx_v1 import InfluxServiceV1
from app.services.fall_runtime import FallRuntime
from app.security.cc_jwt import m2m_required


# 라우터: /events 프리픽스, 문서 태그 "fall"
router = APIRouter(prefix="/events", tags=["fall"])

# -----------------------------------------------------------------------------
# InfluxDB 클라이언트 초기화 (v1.x)
#   - 환경변수(settings)에서 URL/DB/사용자/비밀번호를 읽어 클라이언트를 구성
#   - write_point(...) 로 측정치 기록에 사용
# -----------------------------------------------------------------------------
influx = InfluxServiceV1(
    url=settings.influx_url,
    database=settings.influx_db,
    username=settings.influx_username,
    password=settings.influx_password
)

# -----------------------------------------------------------------------------
# 낙상 모델 런타임(FallRuntime) 및 보정 관련 파라미터
#   - model_path/scaler_path/meta_path: 모델/스케일러/메타 파일 경로
#   - threshold: 낙상 의심 확률 임계값
#   - smooth_k: 스무딩 윈도 크기(연속 프레임 안정화)
#   - backend: 'keras' | 'tflite' 등
# -----------------------------------------------------------------------------
runtime = FallRuntime(  # ADDED
    model_path   = getattr(settings, "fall_model_path", "/models/fall_lstm_model_final_v2.keras"),
    scaler_path  = getattr(settings, "fall_scaler_path", "/models/scaler_final_v2.pkl"),
    meta_path    = getattr(settings, "fall_meta_path", None),
    threshold    = getattr(settings, "fall_threshold", None),
    smooth_k     = getattr(settings, "fall_smooth_k", 3),
    backend      = getattr(settings, "fall_backend", "keras"),
)

# 디바이스별 AI 임계 초과 누적 카운터(프로세스 로컬)
_ai_over_cnt: Dict[str, int] = defaultdict(int)
# AI 확률이 threshold를 연속 몇 번 초과해야 의심 알림을 보낼지
AI_SUSTAIN_K = getattr(settings, "fall_ai_sustain_k", 1)
# 동일 디바이스 알림 쿨다운(초). 중복 알림 방지
COOLDOWN_SEC = getattr(settings, "fall_cooldown_sec", 300)
# 모델 추론 사용 여부 플래그
INFERENCE_ENABLED = getattr(settings, "fall_inference_enabled", True)


# -----------------------------------------------------------------------------
# 요청 스키마: 낙상 이벤트 페이로드
# -----------------------------------------------------------------------------
class FallEvent(BaseModel):
    device_id: str = Field(..., description="ESP32 또는 센서 디바이스 ID")
    presence: int = Field(..., description="사람 존재 여부 (0: 없음, 1: 있음)")
    movement: int = Field(..., description="움직임 상태 (0: 없음, 1: 정지, 2: 활동)")
    moving_range: int = Field(..., description="움직임 거리/범위")
    fall_state: int = Field(..., description="낙상 상태 (0: 정상, 1: 낙상 감지)")
    dwell_state: int = Field(..., description="정지 상태 (0: 없음, 1: 장시간 정지)")
    ts: int = Field(..., description="타임스탬프 (초 단위)")
    location: str = Field("거실", description="센서 위치 (기본: 거실)")
    predicted_prob: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="LSTM 예측 낙상 확률"
    )
    meta: Optional[Dict[str, Any]] = Field(
        default=None,
        description="추가 메타 정보"
    )


# -----------------------------------------------------------------------------
# HA에서 모바일앱 알림 서비스 이름 조회
#   - /api/services 응답 중 domain=="notify" 항목에서 'mobile_app_*' 서비스명 선택
#   - 첫 번째 항목만 반환(운영에서는 캐시/선호도 정책 적용 권장)
#   - 실패 시 None 반환
# -----------------------------------------------------------------------------
async def get_notify_device() -> Optional[str]:
    """Home Assistant에서 notify.mobile_app_* 서비스 중 첫 번째를 반환"""
    url = f"{settings.ha_base_url.rstrip('/')}/api/services"
    headers = {"Authorization": f"Bearer {settings.ha_token}"}

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, headers=headers)
            # 200 이외 상태면 장치 조회 실패로 간주하고 None 반환
            if r.status_code != 200:
                print(f"Failed to fetch notify devices: {r.status_code}")
                return None

            data = r.json()
            # domain == 'notify' 인 항목만 필터링
            notify_services = [s for s in data if s["domain"] == "notify"]
            if not notify_services:
                return None

            # 'mobile_app_*' 접두사를 가진 서비스명을 찾아 'notify.<name>' 형태로 리턴
            for name in notify_services[0]["services"].keys():
                if name.startswith("mobile_app_"):
                    return f"notify.{name}"
    except Exception as e:
        # 네트워크/토큰 오류 등은 None 처리(상위에서 대응)
        print(f"Error fetching HA devices: {e}")
        return None


# -----------------------------------------------------------------------------
# 낙상 후 일정 시간 뒤(현재 15초) 추가 움직임 확인
#   - 최근 movement 값을 조회하여 0/1(없음/정지)이면 보조 경보 전송
#   - Influx 조회 구현체(query_last_movement)가 있으면 사용
# -----------------------------------------------------------------------------
async def check_post_fall_motion(ev: FallEvent):
    await asyncio.sleep(15)  # 실제 대기: 15초 (주석과 실행값 일치)
    try:
        # (예시) Flux 스타일 쿼리 문자열: v1 환경에서는 직접 사용하지 않음
        query = f"""
        from(bucket: "{settings.influx_db}")
          |> range(start: -40s)
          |> filter(fn: (r) => r["_measurement"] == "fall_event")
          |> filter(fn: (r) => r["device_id"] == "{ev.device_id}")
          |> last()
        """
        # Influx v1 클라이언트 구현에 query_last_movement가 있으면 활용
        last_data = influx.query_last_movement(ev.device_id) if hasattr(influx, "query_last_movement") else None
        movement_val = None

        if last_data:
            movement_val = last_data.get("movement", None)

        print(f"[CHECK] 15초 후 movement 상태: {movement_val}")

        # 0(없음) 또는 1(정지)이면 후속 알림 전송
        if movement_val in (0, 1):
            print(f"🚨 [ALERT] {ev.device_id} - 일정 시간 움직임 없음, 추가 알림 전송")
            await send_fall_alert(
                device_id=ev.device_id,
                title="⚠️ 장시간 움직임 없음",
                message=f"{ev.location}에서 낙상 후 일정 시간 동안 움직임이 없습니다.",
                location=ev.location,
                moving_range=ev.moving_range,
                dwell_state=ev.dwell_state,
                ts=ev.ts,
            )
        else:
            print(f"[INFO] 대기 시간 내 움직임 감지({movement_val}), 추가 알림 생략")
    except Exception as e:
        # 조회/알림 중 오류는 로깅만 수행
        print(f"[ERROR] post-fall motion check 실패: {e}")


# -----------------------------------------------------------------------------
# InfluxDB에 낙상 이벤트 1건 기록
#   - 실패해도 예외 전파 대신 False 반환(요청 전체 흐름은 계속)
#   - ts(ns) 변환, prob(예측확률) 호환 처리
# -----------------------------------------------------------------------------
async def record_fall_event(ev: FallEvent) -> bool:
    """
    InfluxDB에 낙상 포인트 1건 기록.
    실패해도 예외는 올리지 않고 False 반환.
    """
    try:
        # ts(초)를 나노초로 변환. timestamp_ns가 따로 있으면 그 값을 우선 사용
        ts_ns = int(ev.ts) * 1_000_000_000 if getattr(ev, "ts", None) else None
        if getattr(ev, "timestamp_ns", None) is not None:
            ts_ns = int(ev.timestamp_ns)

        # predicted_prob / prob 호환성 유지: ev.prob가 있으면 우선, 없으면 predicted_prob 사용
        prob = float(getattr(ev, "prob", getattr(ev, "predicted_prob", 0.0)))

        # Line protocol 필드/태그 구성 후 쓰기
        ok = influx.write_point(
            measurement=settings.influx_measurement,           
            tags={
                "device_id": ev.device_id,                     
                "location": ev.location or settings.location_default,
            },
            fields={
                "prob": prob,
                "fall_state": int(ev.fall_state),
                "moving_range": int(getattr(ev, "moving_range", 0) or 0),
                "dwell_state": int(getattr(ev, "dwell_state", 0) or 0),
                "presence": int(getattr(ev, "presence", 0) or 0),
                "movement": int(getattr(ev, "movement", 0) or 0),
            },
            ts_ns=ts_ns,                                       # 타임스탬프 없으면 서버시간 사용
            rp=getattr(settings, "influx_rp", None),           # 예: autogen
        )
        return bool(ok)
    except Exception:
        # TODO: 운영 환경에서는 log.exception으로 상세 스택 기록 권장
        # log.exception("Influx write failed for fall_event")
        return False


# -----------------------------------------------------------------------------
# 메인 엔드포인트: POST /events/fall
#   - 스코프 기반 M2M 인증 필수(m2m_required)
#   - (옵션) 모델 추론으로 predicted_prob 갱신
#   - InfluxDB 기록 후, 센서 낙상/AI 백스톱 조건에 따라 HA 모바일앱 알림 전송
#   - 후속 모션 체크 태스크를 백그라운드로 실행
# -----------------------------------------------------------------------------
@router.post("/fall")
async def receive_fall(
    ev: FallEvent,
    sub: str = Depends(m2m_required(["events:fall:ingest"])),
    ) -> Dict[str, Any]:
    """
    낙상 이벤트 수신 및 처리\n
    요구: JWT 스코프 "events:fall:ingest"
    응답: { ok, fall_state, recorded, predicted_prob, notify_result }
    """
    # 인증 토큰 주체(sub)와 요청 페이로드 로깅
    print(f"[AUTH] sub={sub}")
    print("[RECEIVED] Fall event data:", ev.dict())

    # (센서 판단과 무관하게) 모델 추론은 먼저 수행해 확률 기록
    prob = None
    try:
        if INFERENCE_ENABLED:
            prob, pred = await runtime.update_and_predict(
                device_id=ev.device_id,
                presence=ev.presence,
                movement=ev.movement,
                moving_range=ev.moving_range,
                dwell_state=ev.dwell_state,
            )
            if prob is not None:
                ev.predicted_prob = prob
    except Exception as e:
        # 추론 실패는 경고만 출력하고 흐름 계속
        print(f"[WARN] model inference failed: {e}")

    # 낙상 이벤트를 InfluxDB에 기록(실패해도 요청은 계속 처리)
    success = await record_fall_event(ev)

    notify_result = None  # HA 알림 호출 결과 보관(코드 맵 등)

    # ---------------------------------------------------------
    # A) 센서가 낙상 판정했고, 쿨다운을 통과하면 즉시 경보 알림 전송
    # ---------------------------------------------------------
    if int(ev.fall_state) == 1 and should_alert(ev.device_id, cooldown_sec=300):
        # 알림 발송 대상(HA 모바일앱 notify 서비스) 조회
        ha_device = await get_notify_device()
        if not ha_device:
            print("No HA mobile notify device found")
            raise HTTPException(status_code=500, detail="No HA mobile notify device found")

        print(f"🚨 [ALERT] Sending fall alert to {ha_device}")

        # 낙상 알림 발송(모바일앱 푸시)
        notify_result = await send_fall_alert(
            device_id=ev.device_id,
            title="🚨 낙상 감지",
            message=f"{ev.location or 'home'}에서 낙상이 감지되었습니다.",
            location=ev.location,
            moving_range=ev.moving_range,
            dwell_state=ev.dwell_state,
            ts=ev.ts,
        )

        # 낙상 알림 결과 로깅 및 보조 엔티티 업데이트(예: 경보 램프)
        print("HA RESPONSE] =>", notify_result)
        try:
            headers = {"Authorization": f"Bearer {settings.ha_token}"}
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    f"{settings.ha_base_url.rstrip('/')}/api/services/input_boolean/turn_on",
                    headers=headers,
                    json={"entity_id": "input_boolean.fall_triggered"}
                )
                print(f"[ENTITY] input_boolean.fall_triggered -> ON (status={r.status_code})")
        except Exception as e:
            # 엔티티 업데이트 실패는 요청 실패로 보진 않고 로깅만 수행
            print(f"[ENTITY ERROR] failed to update entity: {e}")
            
        # 낙상 후 일정 시간 지나면 후속 움직임 체크 태스크 실행(백그라운드)
        asyncio.create_task(check_post_fall_motion(ev))

    # ---------------------------------------------------------
    # B) 센서 미검지(0)인 경우, AI 확률을 이용한 '백스톱' 의심 알림 로직
    # ---------------------------------------------------------
    else:
        print(f"[INFO] No fall detected (fall_state={ev.fall_state})") 

        # 모델 추론이 활성화되어 있고 확률이 계산된 경우에만 백스톱 평가
        try:
            if INFERENCE_ENABLED and prob is not None:
                # threshold 초과 시 디바이스별 연속 초과 카운트 증가, 아니면 리셋
                if prob > runtime.threshold:
                    _ai_over_cnt[ev.device_id] += 1
                else:
                    _ai_over_cnt[ev.device_id] = 0

                # 연속 초과 횟수가 기준 이상이고 쿨다운을 통과하면 의심 알림 발송
                if _ai_over_cnt[ev.device_id] >= AI_SUSTAIN_K and should_alert(ev.device_id, cooldown_sec=COOLDOWN_SEC):
                    ha_device = await get_notify_device()
                    if not ha_device:
                        print("No HA mobile notify device found (AI backstop)")
                        raise HTTPException(status_code=500, detail="No HA mobile notify device found")

                    print(f"🤖 [AI ALERT] Sending backstop fall alert to {ha_device}")
                    msg_extra = f" (모델확률 {prob:.2f})"
                    notify_result = await send_fall_alert(
                        device_id=ev.device_id,
                        title="⚠️낙상 의심",
                        message=f"{ev.location or 'home'}에서 낙상 의심이 감지되었습니다.{msg_extra}",
                        location=ev.location,
                        moving_range=ev.moving_range,
                        dwell_state=ev.dwell_state,
                        ts=ev.ts,
                    )
                    print("[HA RESPONSE] =>", notify_result)

                    # 의심 알림 이후에도 동일하게 후속 움직임 체크 수행
                    asyncio.create_task(check_post_fall_motion(ev))
        except Exception as e:
            # 백스톱 로직 자체 오류는 요청 실패로 보지 않음
            print(f"[WARN] AI backstop failed: {e}")

    # -----------------------------------------------------------------
    # HA 알림 결과 검사: 값 맵에 4xx/5xx가 포함되어 있으면 502로 변환
    #   - send_fall_alert의 리턴 형식(서비스명 -> status code 등)에 의존
    # -----------------------------------------------------------------
    if notify_result:
        if any(code >= 400 for code in notify_result.values() if isinstance(code, int)):
            print("[HA ERROR] Notify failed:", notify_result)
            raise HTTPException(status_code=502, detail=f"HA notify failed: {notify_result}")
        
    # 최종 응답: 기록 성공 여부/센서 낙상/예측확률/알림 결과 포함
    return {
        "ok": True,
        "fall_state": ev.fall_state,
        "recorded": success,
        "predicted_prob": ev.predicted_prob,
        "notify_result": notify_result,
    }
