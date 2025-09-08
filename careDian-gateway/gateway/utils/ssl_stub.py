import json # JSON 모듈

def ssl_available(simulate_no_ssl: bool) -> bool:
    if simulate_no_ssl: return False

    try:
        import ssl  # noqa
        return True
    except ModuleNotFoundError:
        return False

def build_stub_app(message: str):
    async def app(scope, receive, send):
        assert scope["type"] == "http"
        body = json.dumps({"detail": f"FastAPI unavailable: {message}"}).encode()
        await send({"type":"http.response.start","status":503,"headers":[(b"content-type", b"application/json")]})
        await send({"type":"http.response.body","body":body})
        
    return app
