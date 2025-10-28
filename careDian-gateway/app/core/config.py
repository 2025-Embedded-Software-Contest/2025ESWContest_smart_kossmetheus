from __future__ import annotations
from pydantic import Field, field_validator # 데이터 모델의 Field 정의
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List, Any, Literal, Dict
from pathlib import Path
from dotenv import find_dotenv
import json


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
