from __future__  import annotations # 타입 힌트 평가 X, 문자열로 저장
from typing import Any, Dict # 타입 힌트


class HAClient:
    def __init__(self, base_url: str, token: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        self._timeout = timeout
        self._client = None

    async def _ensure(self):
        if self._client is None:
            import httpx # lazy import
            self._httpx = httpx
            self._client = httpx.AsyncClient(timeout=self._timeout)

    async def get_state(self, entity_id: str) -> Dict[str, Any]:
        await self._ensure()
        r = await self._client.get(f"{self.base_url}/api/states/{entity_id}", headers=self._headers)

        if r.status_code == 404:
            raise RuntimeError("Entity not found")
        
        r.raise_for_status()

        return r.json()
    
    async def call_service(self, domain: str, service: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        await self._ensure()
        url = f"{self.base_url}/api/services/{domain}/{service}"
        r = await self._client.post(url, headers=self._headers, json=payload)
        r.raise_for_status()

        try:
            data = r.json()

            if isinstance(data, list) and data:
                return data[0]
            
            return data if isinstance(data, dict) else {"result": data}
        except Exception:
            return {"status": "ok"}
        
    async def close(self):
        if self._client is not None:
            await self._client.aclose()