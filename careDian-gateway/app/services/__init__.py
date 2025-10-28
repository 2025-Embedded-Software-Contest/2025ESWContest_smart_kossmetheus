"""
패키지: app.services.__init__
역할:
  - 서비스 계층의 공용 진입점. 모듈 외부에서 `from app.services import influx` 처럼
    간편하게 InfluxDB v1 어댑터 인스턴스를 가져다 쓸 수 있도록 초기화한다.
  - 설정(app.core.config.settings)을 읽어 `InfluxServiceV1` 싱글턴을 구성한다.

운영 메모:
  - `verify_arg = settings.influx_ca_cert or settings.influx_verify_tls`
    * influx_ca_cert가 설정되면(예: "/path/ca.crt") 이를 우선 사용(일부 클라이언트/requests는 경로 문자열 허용)
    * 아니면 influx_verify_tls(boolean)로 검증 여부 결정
    * 사용 중인 influxdb 파이썬 클라이언트 버전에 따라 verify_ssl이 **bool만 허용**될 수 있으므로,
      경로 전달이 필요한 경우 어댑터(services/influx_v1.py)에서 세션에 직접 주입하도록 확장 필요
  - URL이 http:// 인 경우, 어댑터에서 ssl=False로 동작하여 verify_ssl은 무시된다.
"""

from app.core.config import settings                 # .env/환경변수 기반 설정 객체
from .influx_v1 import InfluxServiceV1                # InfluxDB 1.x 서비스 어댑터


# TLS 검증 설정 결합
# - 우선순위: CA 경로가 있으면 그 값을 사용 → 없으면 단순 불리언 설정 사용
verify_arg = settings.influx_ca_cert or settings.influx_verify_tls

# 공용 Influx 서비스 인스턴스(Singleton 용도)
# - 외부에서는 `from app.services import influx` 로 재사용
influx = InfluxServiceV1(
    url=settings.influx_url,                    # 예) http(s)://host:8086
    database=settings.influx_db,                # 기본 데이터베이스
    username=settings.influx_username,          # 인증 사용자
    password=settings.influx_password,          # 인증 비밀번호
    timeout_sec=settings.influx_timeout_sec,    # HTTP 타임아웃(초)
    verify_ssl=verify_arg,                      # TLS 검증: 경로 또는 불리언(클라이언트 지원 여부 확인)
    rp=settings.influx_rp,                      # 기본 Retention Policy(옵션)
)
