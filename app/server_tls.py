"""
모듈: server_tls.py — Uvicorn TLS 실행 스크립트

역할
  - FastAPI 앱(app.main.app)을 **TLS(HTTPS)** 로 구동한다.
  - .env에서 인증서/포트/워커 수 등을 읽어 `uvicorn.run`에 전달한다.
  - (옵션) mTLS(Client Certificate) 요구를 활성화할 수 있다.

사용 환경변수(.env)
  - TLS_CERT  : 서버 인증서 경로 (예: ./certs/server.crt)
  - TLS_KEY   : 서버 개인키 경로 (예: ./certs/server.key)
  - TLS_CA    : (옵션) 클라이언트 인증서 신뢰용 CA 체인 경로 (mTLS 시 필수)
  - TLS_REQUIRE_CLIENT_CERT : '1/true/on' 이면 mTLS 활성화(클라이언트 인증서 필수)
  - TLS_HOST  : 바인딩 호스트 (기본 0.0.0.0)
  - TLS_PORT  : 바인딩 포트 (기본 8443)
  - UVICORN_WORKERS : 워커 수 (기본 1)

주의
  - TLS_CERT/TLS_KEY 가 없으면 프로세스를 종료(SystemExit 2).
  - mTLS 활성화 시 TLS_CA 가 없으면 종료(SystemExit 2).
  - 서버 입장에서는 호스트네임 검증을 하지 않는다(`ssl_cert_reqs`만 설정). 클라이언트는 서버 인증서 검증 책임이 있다.
"""

import os, ssl, sys
import uvicorn

# .env 자동 로드 시도 (.env가 없어도 동작)
try:
    from dotenv import load_dotenv
    load_dotenv()  # .env 자동 로드
except Exception:
    pass

# FastAPI 애플리케이션 (app/main.py 의 app 객체)
from app.main import app


def _flag(name: str, default=False) -> bool:
    """문자열 환경변수를 느슨한 불리언으로 변환.
    - 허용 값: 1, true, yes, y, on (대소문자/공백 무시)
    - 미설정 시 default 반환
    """
    v = os.getenv(name)
    if v is None:
        return default
    return str(v).strip().lower() in ("1","true","yes","y","on")


def _resolve_paths():
    # 인증서 관련 경로 수집(TLS_CERT/TLS_KEY/TLS_CA).
    cert = os.getenv("TLS_CERT")
    key  = os.getenv("TLS_KEY")
    ca   = os.getenv("TLS_CA")
    return cert, key, ca


def build_ssl_kwargs() -> dict:
    """`uvicorn.run` 에 넘길 SSL 관련 인자(dict) 구성.

    반환값 예:
      {
        "ssl_certfile": "./certs/server.crt",
        "ssl_keyfile":  "./certs/server.key",
        "ssl_cert_reqs": ssl.CERT_REQUIRED,   # mTLS 시
        "ssl_ca_certs":  "./certs/ca.crt"     # mTLS 시
      }
    """
    cert, key, ca = _resolve_paths()

    # 필수 키 검증: 없으면 표준 에러로 경고 후 종료
    if not key:
        print("[m2m] TLS_KEY not found. Set TLS_KEY (e.g. .\\certs\\server.key).", file=sys.stderr)
        raise SystemExit(2)
    if not cert:
        print("[m2m] TLS_CERT not found. Set TLS_CERT (e.g. .\\certs\\server.crt).", file=sys.stderr)
        raise SystemExit(2)

    require_client = _flag("TLS_REQUIRE_CLIENT_CERT", False)

    kwargs = {
        "ssl_certfile": cert,
        "ssl_keyfile":  key,
    }

    if require_client:
        # mTLS: 클라이언트 인증서를 필수로 요구
        if not ca:
            print("[m2m] TLS_REQUIRE_CLIENT_CERT=true 이면 TLS_CA가 필요합니다.", file=sys.stderr)
            raise SystemExit(2)
        kwargs["ssl_cert_reqs"] = ssl.CERT_REQUIRED
        kwargs["ssl_ca_certs"]  = ca
    else:
        # mTLS 비활성화: 클라이언트 인증서 요구 안 함
        kwargs["ssl_cert_reqs"] = ssl.CERT_NONE

    return kwargs


if __name__ == "__main__":
    # 네트워킹/프로세스 설정값 로드
    host = os.getenv("TLS_HOST", "0.0.0.0")          # 기본 모든 인터페이스 바인딩
    port = int(os.getenv("TLS_PORT", "8443"))         # 기본 8443 포트
    workers = int(os.getenv("UVICORN_WORKERS", "1"))  # 워커 프로세스 수

    # Uvicorn 실행: X-Forwarded-* 신뢰(프록시 뒤 배치 시), TLS 옵션 주입
    uvicorn.run(
        app,
        host=host,
        port=port,
        forwarded_allow_ips="*",  # 모든 프록시의 X-Forwarded 헤더 허용(프록시 신뢰 관리 필요)
        workers=workers,
        **build_ssl_kwargs(),      # 위에서 구성한 SSL 인자 주입
    )
