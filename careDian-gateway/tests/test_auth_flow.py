from starlette.testclient import TestClient
from gateway.app import create_app


def _mk_env(monkeypatch):
    monkeypatch.setenv("HA_BASE_URL", "https://caredian.gleeze.com")
    monkeypatch.setenv("HA_TOKEN", "t")
    monkeypatch.setenv("JWT_SECRET", "s")
    monkeypatch.setenv("API_KEYS", "k1")


def test_exchange_and_refresh(monkeypatch):
    _mk_env(monkeypatch)
    app = create_app()

    # FastAPI 모드일 때만 동작(ssl이 있을 때). 없으면 이 테스트는 스킵되어야 함.
    if not hasattr(app, "routes"):
        return
    
    c = TestClient(app)
    r = c.post("/auth/exchange", json={"api_key":"k1", "sub":"user1"})
    assert r.status_code == 200
    
    pair = r.json()
    r2 = c.post("/auth/refresh", json={"refresh_token": pair["refresh_token"]})
    assert r2.status_code == 200
# access로 보호된 엔드포인트 호출은 별도 통합 테스트에서 검증