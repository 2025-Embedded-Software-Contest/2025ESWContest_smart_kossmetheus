"""
# 환경변수 & 실행
export HA_BASE_URL="https://caredian.gleeze.com"
export HA_TOKEN="<ha-long-lived-token>"

# (선택) API 키 & JWT
export API_KEYS="key1,key2"
export JWT_SECRET="change-me"; export JWT_ISSUER="issuer"; export JWT_AUDIENCE="aud"

# (옵션)
export RATE_LIMIT=60; export RATE_WINDOW_SEC=60; export ALLOWED_ORIGINS="https://app.example.com"
export REQUEST_TIMEOUT_S=10; export LOG_LEVEL=INFO

# 서버 실행(권장):
uvicorn "gateway.app:create_app" --host 0.0.0.0 --port 8080

# 또는 패키지 진입점
python -m gateway.main

# Stub 모드 강제(디버그):
FORCE_STUB=1 uvicorn "gateway.app:create_app" --port 8080
"""