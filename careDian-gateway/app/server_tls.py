import os, ssl, sys
import uvicorn

try:
    from dotenv import load_dotenv
    load_dotenv()  # .env 자동 로드
except Exception:
    pass

from app.main import app


def _flag(name: str, default=False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return str(v).strip().lower() in ("1","true","yes","y","on")

def _resolve_paths():
    cert = os.getenv("TLS_CERT")
    key  = os.getenv("TLS_KEY")
    ca   = os.getenv("TLS_CA")

    return cert, key, ca

def build_ssl_kwargs() -> dict:
    """uvicorn.run 에 넘길 SSL 관련 kwargs 구성"""
    cert, key, ca = _resolve_paths()
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
        if not ca:
            print("[m2m] TLS_REQUIRE_CLIENT_CERT=true 이면 TLS_CA가 필요합니다.", file=sys.stderr)
            raise SystemExit(2)
        kwargs["ssl_cert_reqs"] = ssl.CERT_REQUIRED
        kwargs["ssl_ca_certs"]  = ca
    else:
        # 서버 입장에선 별도 설정 불필요 (클라이언트 hostname 검증은 클라이언트 책임)
        kwargs["ssl_cert_reqs"] = ssl.CERT_NONE

    return kwargs


if __name__ == "__main__":
    host = os.getenv("TLS_HOST", "0.0.0.0")
    port = int(os.getenv("TLS_PORT", "8443"))
    workers = int(os.getenv("UVICORN_WORKERS", "1"))

    uvicorn.run(
        app,
        host=host,
        port=port,
        forwarded_allow_ips="*",
        workers=workers,
        **build_ssl_kwargs(),
    )