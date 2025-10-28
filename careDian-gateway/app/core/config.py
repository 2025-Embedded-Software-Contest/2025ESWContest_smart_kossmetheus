"""
모듈: core/config.py (애플리케이션 설정 관리)

목적:
  - .env 및 환경변수에서 설정값을 읽어 타입-세이프하게 제공한다.
  - pydantic-settings 를 사용하여 검증/전처리/기본값/별칭(alias)을 일관되게 관리한다.
  - 외부 구성요소(InfluxDB, Home Assistant, JWT, 모델 추론 등)와의 접점 값들을 중앙집중화한다.

핵심 포인트:
  - Settings(BaseSettings) 하나로 모든 설정을 관리하고 "settings = Settings()"로 싱글턴처럼 사용한다.
  - env_file 우선순위: CWD 기준 .env → 프로젝트 루트(.env) 폴백.
  - 문자열 기반 환경값을 list/bool/path/json(map) 등으로 파싱하는 validator 제공.

보안/운영 노트:
  - 비밀키(예: INFLUX_PASSWORD, HA_TOKEN, SESSION_SECRET, JWT_PRIVATE_PEM_PATH)는 .env/시크릿 매니저로 관리.
  - 경로 설정값은 절대경로로 정규화하여(validator) 런타임 위치에 의존하지 않도록 한다.
"""

from __future__ import annotations
from pydantic import Field, field_validator  # 필드 정의 및 커스텀 유효성 검증기
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List, Any, Literal, Dict
from pathlib import Path
from dotenv import find_dotenv
import json


# -----------------------------------------------------------------------------
# .env 파일 경로 탐색
#   - 개발 중 리로더/서브프로세스 환경을 고려해 CWD 우선으로 탐색하고,
#     그래도 없으면 프로젝트 루트(현재 파일 기준 상위 2단계)의 .env를 폴백으로 사용
# -----------------------------------------------------------------------------
ENV_FILE = find_dotenv(usecwd=True) or str((Path(__file__).resolve().parents[2] / ".env"))
# BASE_DIR: app/ 하위 기준(현재 파일은 app/core/config.py)이므로 상위 한 단계가 app/** 의 루트
BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """프로젝트 전역 설정 컨테이너

    - 모든 환경변수는 Field(alias=...) 로 매핑되어 .env 키와 코드 속 속성명을 분리한다.
    - model_config 로 env 파일 경로/인코딩/대소문자/여분 필드 정책을 지정한다.
    """

    # pydantic-settings 동작 구성
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,              # 위에서 탐색한 .env 경로
        env_file_encoding="utf-8",     # .env 인코딩
        case_sensitive=False,           # 키 대소문자 무시 (APP_NAME == app_name)
        extra="ignore",                # 정의되지 않은 키는 무시
    )

    # -----------------------------
    # App (일반)
    # -----------------------------
    app_name: str = Field("CareDian Gateway", alias="APP_NAME")
    env: str = Field("dev", alias="ENV")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    log_json: bool = Field(False, alias="LOG_JSON")  # JSON 로그 출력 여부
    allowed_origins: List[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")  # CORS 허용 오리진

    # -----------------------------
    # Session (쿠키/서버 사이드 세션 시)
    # -----------------------------
    session_secret: Optional[str] = Field(None, alias="SESSION_SECRET")
    session_cookie_name: str = Field("caredian_session", alias="SESSION_COOKIE_NAME")

    # -----------------------------
    # M2M 인증 (API Key & Client Credentials)
    # -----------------------------
    api_keys_json: Dict[str, str] = Field(default_factory=dict, alias="API_KEYS_JSON")     # (kid -> secret)
    cc_clients_json: Dict[str, str] = Field(default_factory=dict, alias="CC_CLIENTS_JSON") # (client_id -> client_secret)

    # -----------------------------
    # JWT (RS256)
    # -----------------------------
    jwt_aud: str = Field("caredian-gw", alias="JWT_AUD")             # 토큰 Audience
    jwt_iss: str = Field("http://localhost:8080", alias="JWT_ISS")   # 토큰 Issuer
    jwt_ttl_seconds: int = Field(300, alias="JWT_TTL_SECONDS")         # 토큰 만료(초)

    # 키 파일 경로 (서명/검증 키)
    jwt_private_pem_path: Optional[str] = Field(None, alias="JWT_PRIVATE_PEM_PATH")
    jwt_public_pem_path: Optional[str] = Field(None, alias="JWT_PUBLIC_PEM_PATH")

    # -----------------------------
    # InfluxDB 1.x
    # -----------------------------
    influx_url: str = Field(..., alias="INFLUX_URL")
    influx_db: str = Field(..., alias="INFLUX_DB")
    influx_rp: str | None = Field(None, alias="INFLUX_RP")             # Retention Policy(옵션)
    influx_username: str = Field(..., alias="INFLUX_USERNAME")
    influx_password: str = Field(..., alias="INFLUX_PASSWORD")
    influx_timeout_sec: int = Field(5, alias="INFLUX_TIMEOUT_SEC")
    influx_verify_tls: bool = Field(False, alias="INFLUX_VERIFY_TLS")   # Influx HTTP API TLS 검증 여부
    influx_ca_cert: Optional[str] = Field(None, alias="INFLUX_CA_CERT") # 자체 CA 사용 시 경로
    influx_measurement: str = Field("fall_events", alias="INFLUX_MEASUREMENT")

    # -----------------------------
    # Home Assistant
    # -----------------------------
    ha_base_url: str = Field(..., alias="HA_BASE_URL")                 # 예: http://homeassistant.local:8123
    ha_token: str = Field(..., alias="HA_TOKEN")                       # Long-Lived Access Token
    request_timeout: int = Field(10, alias="REQUEST_TIMEOUT_SEC")      # 외부 HTTP 타임아웃(초)

    # -----------------------------
    # Notify (알림 프리셋)
    # -----------------------------
    ha_notify_mobile: str = Field("", alias="HA_NOTIFY_MOBILE")        # 특정 notify 서비스 강제 지정 시
    ha_notify_persist: str = Field("persistent_notification.create", alias="HA_NOTIFY_PERSIST")
    location_default: str = Field("home", alias="LOCATION_DEFAULT")

    # -----------------------------
    # Fall LSTM (모델 추론 관련)
    # -----------------------------
    fall_inference_enabled: bool = Field(True, alias="FALL_INFERENCE_ENABLED")
    fall_backend: Literal["keras", "tflite"] = Field("keras", alias="FALL_BACKEND")
    # 기본 모델/스케일러/메타 경로: app/models/* 상대경로를 절대경로로 변환하여 사용
    fall_model_path: str = Field(str(BASE_DIR / "models" / "fall_lstm_model_final_v2.keras"), alias="FALL_MODEL_PATH")
    fall_scaler_path: str = Field(str(BASE_DIR / "models" / "scaler_final_v2.pkl"), alias="FALL_SCALER_PATH")
    fall_meta_path: Optional[str] = Field(str(BASE_DIR / "models" / "fall_lstm_final_v2_meta.json"), alias="FALL_META_PATH")
    fall_threshold: float = Field(0.5, ge=0.0, le=1.0, alias="FALL_THRESHOLD")     # 낙상 의심 확률 임계값
    fall_smooth_k: int = Field(3, ge=1, alias="FALL_SMOOTH_K")                    # 스무딩 윈도 크기
    fall_decision_mode: Literal["sensor_or_model", "sensor_and_model", "model_only", "sensor_only"] = Field(
        "sensor_or_model", alias="FALL_DECISION_MODE"
    )
    fall_cooldown_sec: int = Field(300, ge=0, alias="FALL_COOLDOWN_SEC")          # 알림 쿨다운(초)
    fall_seq_len_override: Optional[int] = Field(None, alias="FALL_SEQ_LEN")       # 입력 시퀀스 길이 강제 덮어쓰기

    # -----------------------------
    # Validators (전처리/정규화)
    # -----------------------------

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def _parse_allowed_origins(cls, v: Any):
        """CORS 오리진을 다양한 표현식에서 list[str]로 정규화
        - None → []
        - list → 그대로
        - 문자열: "[\"https://a\", \"https://b\"]"(JSON) 또는 "https://a, https://b"
        """
        if v is None:
            return []
        if isinstance(v, list):
            return v
        s = str(v).strip()
        if not s:
            return []
        # JSON 배열 문자열 처리
        if s.startswith("["):
            try:
                arr = json.loads(s)
                return arr if isinstance(arr, list) else []
            except Exception:
                pass
        # 콤마 구분 문자열 처리
        return [t.strip() for t in s.split(",") if t.strip()]

    @field_validator("log_json", "influx_verify_tls", "fall_inference_enabled", mode="before")
    @classmethod
    def _parse_bool_loose(cls, v: Any):
        """느슨한 불리언 파서
        - bool → 그대로
        - 문자열: 1/true/yes/on (대소문자 무시) → True, 그 외 → False
        """
        if isinstance(v, bool):
            return v
        s = str(v).strip().lower()
        return s in {"1", "true", "yes", "on"}

    @field_validator("fall_model_path", "fall_scaler_path", "fall_meta_path", mode="before")
    @classmethod
    def _norm_path(cls, v: Any):
        """경로를 사용자 홈/상대경로 포함해 절대경로 문자열로 정규화
        - None → None 유지
        - 공백/빈문자열 → 그대로 반환(필수 아님)
        - 그 외 → expanduser().resolve() 결과 문자열
        """
        if v is None:
            return None
        s = str(v).strip()
        if not s:
            return s
        try:
            return str(Path(s).expanduser().resolve())
        except Exception:
            # 경로 파싱 실패 시 원본 문자열 유지(후속 단계에서 처리)
            return s
    
    @field_validator("api_keys_json", "cc_clients_json", mode="before")
    @classmethod
    def _parse_json_map(cls, v: Any):
        """문자열(JSON) → dict 로 변환
        - None → {}
        - dict → 그대로
        - 그 외 문자열 → json.loads 시도, dict 가 아니면 {}
        예) '{"svc_ingestor":"****"}' → {"svc_ingestor":"****"}
        """
        if v is None:
            return {}
        if isinstance(v, dict):
            return v
        try:
            d = json.loads(str(v))
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}


# Settings 인스턴스 생성: import 시점에 .env/환경변수 로딩 및 유효성 검증 수행
settings = Settings()



# .env 경로 찾기 (CWD 우선 → 리로더/서브프로세스에서도 루트 폴백)
ENV_FILE = find_dotenv(usecwd=True) or str((Path(__file__).resolve().parents[2] / ".env"))
BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = Field("CareDian Gateway", alias="APP_NAME")
    env: str = Field("dev", alias="ENV")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    log_json: bool = Field(False, alias="LOG_JSON")
    allowed_origins: List[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")

    # Session
    session_secret: Optional[str] = Field(None, alias="SESSION_SECRET")
    session_cookie_name: str = Field("caredian_session", alias="SESSION_COOKIE_NAME")

    # M2M 인증
    # API Key (kid->secret)
    api_keys_json: Dict[str, str] = Field(default_factory=dict, alias="API_KEYS_JSON")
    # Client-Credentials (client_id->client_secret)
    cc_clients_json: Dict[str, str] = Field(default_factory=dict, alias="CC_CLIENTS_JSON")

    # JWT RS256
    jwt_aud: str = Field("caredian-gw", alias="JWT_AUD")
    jwt_iss: str = Field("http://localhost:8080", alias="JWT_ISS")
    jwt_ttl_seconds: int = Field(300, alias="JWT_TTL_SECONDS")

    # 키 제공 경로
    jwt_private_pem_path: Optional[str] = Field(None, alias="JWT_PRIVATE_PEM_PATH")
    jwt_public_pem_path: Optional[str] = Field(None, alias="JWT_PUBLIC_PEM_PATH")

    # InfluxDB 1.x
    influx_url: str = Field(..., alias="INFLUX_URL")
    influx_db: str = Field(..., alias="INFLUX_DB")
    influx_rp: str | None = Field(None, alias="INFLUX_RP")
    influx_username: str = Field(..., alias="INFLUX_USERNAME")
    influx_password: str = Field(..., alias="INFLUX_PASSWORD")
    influx_timeout_sec: int = Field(5, alias="INFLUX_TIMEOUT_SEC")
    influx_verify_tls: bool = Field(False, alias="INFLUX_VERIFY_TLS")
    influx_ca_cert: Optional[str] = Field(None, alias="INFLUX_CA_CERT")
    influx_measurement: str = Field("fall_events", alias="INFLUX_MEASUREMENT")

    # HA
    ha_base_url: str = Field(..., alias="HA_BASE_URL")
    ha_token: str = Field(..., alias="HA_TOKEN")
    request_timeout: int = Field(10, alias="REQUEST_TIMEOUT_SEC")

    # Notify
    ha_notify_mobile: str = Field("", alias="HA_NOTIFY_MOBILE")
    ha_notify_persist: str = Field("persistent_notification.create", alias="HA_NOTIFY_PERSIST")
    location_default: str = Field("home", alias="LOCATION_DEFAULT")

    # Fall LSTM
    fall_inference_enabled: bool = Field(True, alias="FALL_INFERENCE_ENABLED")
    fall_backend: Literal["keras", "tflite"] = Field("keras", alias="FALL_BACKEND")
    fall_model_path: str = Field(str(BASE_DIR / "models" / "fall_lstm_model_final_v2.keras"), alias="FALL_MODEL_PATH")
    fall_scaler_path: str = Field(str(BASE_DIR / "models" / "scaler_final_v2.pkl"), alias="FALL_SCALER_PATH")
    fall_meta_path: Optional[str] = Field(str(BASE_DIR / "models" / "fall_lstm_final_v2_meta.json"), alias="FALL_META_PATH")
    fall_threshold: float = Field(0.5, ge=0.0, le=1.0, alias="FALL_THRESHOLD")
    fall_smooth_k: int = Field(3, ge=1, alias="FALL_SMOOTH_K")  
    fall_decision_mode: Literal["sensor_or_model", "sensor_and_model", "model_only", "sensor_only"] = Field(
        "sensor_or_model", alias="FALL_DECISION_MODE"
    )
    fall_cooldown_sec: int = Field(300, ge=0, alias="FALL_COOLDOWN_SEC")
    fall_seq_len_override: Optional[int] = Field(None, alias="FALL_SEQ_LEN")

    # validators
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def _parse_allowed_origins(cls, v: Any):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        s = str(v).strip()
        if not s:
            return []
        if s.startswith("["):
            try:
                arr = json.loads(s)
                return arr if isinstance(arr, list) else []
            except Exception:
                pass
        return [t.strip() for t in s.split(",") if t.strip()]

    @field_validator("log_json", "influx_verify_tls", "fall_inference_enabled", mode="before")
    @classmethod
    def _parse_bool_loose(cls, v: Any):
        if isinstance(v, bool):
            return v
        s = str(v).strip().lower()
        return s in {"1", "true", "yes", "on"}

    @field_validator("fall_model_path", "fall_scaler_path", "fall_meta_path", mode="before")
    @classmethod
    def _norm_path(cls, v: Any):
        if v is None:
            return None
        s = str(v).strip()
        if not s:
            return s
        try:
            return str(Path(s).expanduser().resolve())
        except Exception:
            return s
    
    @field_validator("api_keys_json", "cc_clients_json", mode="before")
    @classmethod
    def _parse_json_map(cls, v: Any):
        if v is None:
            return {}
        if isinstance(v, dict):
            return v
        try:
            d = json.loads(str(v))
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}


settings = Settings()
