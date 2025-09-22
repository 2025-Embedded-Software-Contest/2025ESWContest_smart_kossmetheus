# 선택: firebase-admin을 실제로 붙일 때 사용
# pip install firebase-admin
from typing import Any, Dict, Optional

class FCMClient:
    def __init__(self, creds_path: Optional[str] = None):
        self.ready = False
        try:
            import firebase_admin
            from firebase_admin import credentials, messaging
            if creds_path:
                cred = credentials.Certificate(creds_path)
                firebase_admin.initialize_app(cred)
            else:
                firebase_admin.initialize_app()
            self.messaging = messaging
            self.ready = True
        except Exception:
            self.messaging = None

    def send(self, token: str, title: str, body: str, data: Optional[Dict[str, Any]] = None):
        if not self.ready: return {"sent": False, "reason": "FCM not configured"}
        msg = self.messaging.Message(
            notification=self.messaging.Notification(title=title, body=body),
            token=token,
            data=data or {},
        )
        resp = self.messaging.send(msg)
        return {"sent": True, "message_id": resp}
