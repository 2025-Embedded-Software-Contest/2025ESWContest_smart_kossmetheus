try:
    from .app import create_app
except Exception:
    # 스크립트 실행 지원
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from gateway.app import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn # ASGI 서버
    uvicorn.run("gateway.main:app", host="0.0.0.0", port=8080, reload=False)
    # reload = True 코드 변경 시 자동 재시작
    # reload = False 자동 재시작 X
