import os
from gateway.app import create_app


def test_stub_when_no_ssl(monkeypatch):
    monkeypatch.setenv("SIMULATE_NO_SSL", "1")
    app = create_app()
    assert callable(app) # Stub ASGI
    monkeypatch.delenv("SIMULATE_NO_SSL")