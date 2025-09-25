from pydantic import BaseSettings

class Settings(BaseSettings):
    FCM_CREDENTIALS: str = "serviceAccountKey.json"
    DATABASE_URL: str = "sqlite:///./caredian.db"

    class Config:
        env_file = ".env"

settings = Settings()
