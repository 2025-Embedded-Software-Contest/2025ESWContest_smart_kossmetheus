import httpx
from typing import Any, Dict
from app.core.config import settings

class HAClient:
    def __init__(self):
        self.base = settings.ha_base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {settings.ha_token}", "Content-Type": "application/json"}
        self.timeout = settings.request_timeout

    async def get_state(self, entity_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.get(f"{self.base}/api/states/{entity_id}", headers=self.headers)
            r.raise_for_status()
            return r.json()

    async def call_service(self, domain: str, service: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(f"{self.base}/api/services/{domain}/{service}", headers=self.headers, json=payload)
            r.raise_for_status()
            try:
                data = r.json()
                if isinstance(data, list) and data: return data[0]
                return data if isinstance(data, dict) else {"result": data}
            except Exception:
                return {"status": "ok"}
