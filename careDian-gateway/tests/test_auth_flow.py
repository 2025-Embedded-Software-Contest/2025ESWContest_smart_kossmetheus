from fastapi.testclient import TestClient

from app.main import app


def test_exchange_and_refresh(monkeypatch):
    c = TestClient(app)
    monkeypatch.setenv("API_KEYS", "testkey")

    r = c.post("/auth/exchange", json={"api_key": "testkey", "sub": "user1"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data and "refresh_token" in data

    r2 = c.post("/auth/refresh", json={"refresh_token": data["refresh_token"]})
    assert r2.status_code == 200
    assert "access_token" in r2.json()
