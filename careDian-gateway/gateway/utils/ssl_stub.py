import json # JSON 모듈

# SSL 모듈 사용 가능 여부 확인
def ssl_available(simulate_no_ssl: bool) -> bool:
    if simulate_no_ssl: return False

    try:
        import ssl  # noqa
        return True
    except ModuleNotFoundError:
        return False

# SSL 모듈 부재 시 Stub ASGI 앱 생성
def build_stub_app(message: str):
    async def app(scope, receive, send):
        assert scope["type"] == "http"
        body = json.dumps({"detail": f"FastAPI unavailable: {message}"}).encode() # Response Body
        await send({"type":"http.response.start",
                    "status":503,
                    "headers":[(b"content-type", b"application/json")]})
        await send({"type":"http.response.body",
                    "body":body})
        
    return app
