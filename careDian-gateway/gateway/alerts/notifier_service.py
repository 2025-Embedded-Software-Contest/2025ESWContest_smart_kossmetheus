import httpx # 비동기 HTTP 클라이언트 라이브러리
from typing import Any, Dict, List, Optional # 타입 힌트

from gateway.core.settings import Settings


class NotifierService:
    def __init__(self, s: Settings):
        self.s = s

    async def send_fcm(self, title: str, body: str, data: Dict[str, Any], *, server_key: Optional[str], tokens: List[str]=[], topic: Optional[str]=None) -> Optional[Dict[str, Any]]:
        if not server_key: return None

        headers = {"Authorization": f"key={server_key}", "Content-Type":"application/json"}
        payloads = []

        if tokens:
            for t in tokens:
                payloads.append({"to": t, "notification":{"title":title,"body":body}, "data":data, "android":{"priority":"high"}, "priority":"high"})
        elif topic:
            payloads.append({"to": topic, "notification":{"title":title,"body":body}, "data":data, "android":{"priority":"high"}, "priority":"high"})
        else:
            return None
        
        results = []

        async with httpx.AsyncClient(timeout=self.s.request_timeout) as client:
            for pl in payloads:
                r = await client.post("https://fcm.googleapis.com/fcm/send", headers=headers, json=pl)
                r.raise_for_status()
                results.append(r.json())

        return {"sent": len(results), "results": results}

    async def send_ha_notify(self, title: str, message: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not (self.s.ha_base_url and self.s.ha_token and self.s.ha_notify_services):
            return None
        
        headers = {"Authorization": f"Bearer {self.s.ha_token}", "Content-Type":"application/json"}
        results = []

        async with httpx.AsyncClient(timeout=self.s.request_timeout) as client:
            for svc in self.s.ha_notify_services:
                url = f"{self.s.ha_base_url.rstrip('/')}/api/services/{svc.replace('.','/')}"
                body = {"title": title, "message": message, "data": data}
                r = await client.post(url, headers=headers, json=body)
                r.raise_for_status()

                try:
                    results.append(r.json())
                except Exception:
                    results.append({"status": "ok"})
                    
        return {"services": self.s.ha_notify_services, "results": results}
