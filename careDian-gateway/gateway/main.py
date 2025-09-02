from __future__ import annotations # 타입 힌트 평가 X, 문자열로 저장


try: # module로 실행
    from .app import create_app
except Exception: # 직접 실행
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

    from gateway.app import create_app

app = create_app()

if __name__ == "__main__":
    # if os.getenv("RUN_SERVER") == "1":
    import uvicorn
    uvicorn.run("gateway.main:app", host="0.0.0.0", port=8080, reload=False)