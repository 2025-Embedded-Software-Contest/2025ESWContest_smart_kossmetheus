# 실행

```
# dev
export PYTHONPATH=.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# prod
export PYTHONPATH=.
gunicorn -k uvicorn.workers.UvicornWorker app.main:app -c gunicorn.conf.py
```

# 안 쓰는 파일
test_jwt_util.py
test_rate_limit.py
test_ssl_stub.py

# 디렉토리
```
careDian-gateway/
├─ app/
│  ├─ main.py
│  ├─ api/
│  │  ├─ __init__.py
│  │  ├─ health.py
│  │  ├─ auth.py
│  │  ├─ ha_proxy.py
│  │  └─ alerts.py
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ config.py
│  │  ├─ logging.py
│  │  ├─ security.py
│  │  └─ rate_limit.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ auth.py
│  │  └─ alerts.py
│  └─ services/
│     ├─ __init__.py
│     ├─ ha_client.py
│     ├─ fcm.py
│     └─ notify.py
├─ tests/
│  ├─ __init__.py
│  ├─ test_health.py
│  └─ test_auth_flow.py
├─ .env
├─ gunicorn.conf.py
├─ requirements.txt
└─ README.md
```