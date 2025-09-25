from firebase_admin import credentials, initialize_app, messaging
from pathlib import Path

FCM_KEY_PATH = "serviceAccountKey.json"  # FCM 서비스 계정 키 파일
_app = None

if Path(FCM_KEY_PATH).exists():
    cred = credentials.Certificate(FCM_KEY_PATH)
    _app = initialize_app(cred)

def send_fcm(title: str, body: str, data: dict, tokens: list[str]):
    if not _app or not tokens:
        print("[FCM disabled]", title, body, data)
        return

    msg = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body),
        data={k: str(v) for k, v in data.items()},
        tokens=tokens,
    )
    resp = messaging.send_multicast(msg)
    print(f"[FCM] success={resp.success_count}, failure={resp.failure_count}")
