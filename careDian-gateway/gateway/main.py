from __future__ import annotations
import os
from .app import create_app


app = create_app()

if __name__ == "__main__":
    if os.getenv("RUN_SERVER") == "1":
        import uvicorn
        uvicorn.run("gateway.main:app", host="0.0.0.0", port=8080, reload=False)