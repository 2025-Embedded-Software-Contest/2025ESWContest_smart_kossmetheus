import hmac
from fastapi import Header, HTTPException

from app.core.config import settings


def api_key_required(x_api_key: str = Header(None)):
    # 헤더: X-API-Key: <kid>.<secret>
    if not x_api_key or "." not in x_api_key:
        raise HTTPException(401, "missing api key")
    kid, provided = x_api_key.split(".", 1)
    secret = settings.api_keys_json.get(kid)
    if not secret or not hmac.compare_digest(secret, provided):
        raise HTTPException(401, "invalid api key")
    return kid  # caller id
