from firebase_admin import credentials, initialize_app, messaging
from pathlib import Path

_app = None

def init_fcm():
    """Firebase Admin SDK 초기화"""
    global _app
    if _app is not None:
        return
    cred_path = Path("serviceAccountKey.json")
    if cred_path.exists():
        cred = credentials.Certificate(str(cred_path))
        _app = initialize_app(cred)
        print("[FCM] Initialized")
    else:
        print("[FCM] serviceAccountKey.json not found → FCM disabled")

def send_push(user_id: str, title: str, body: str):
    """특정 유저(혹은 등록된 토큰)에 푸시 알림 발송"""
    if _app is None:
        print("[FCM disabled]", title, body)
        return

    # 현재는 단일 토큰 테스트용 (나중엔 DB에서 user_id→토큰 매핑 필요)
    # 예시: Firebase Console에서 발급받은 단말기 토큰 넣기
    TEST_TOKEN = "<여기에_테스트용_FCM_토큰_넣기>"

    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=TEST_TOKEN,
    )
    resp = messaging.send(message)
    print(f"[FCM] sent to {user_id}: {resp}")
