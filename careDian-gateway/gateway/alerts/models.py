from pydantic import BaseModel, Field # 데이터 모델과 모델의 Field 정의
from typing import Optional # 타입 힌트


class FallAlert(BaseModel):
    person_id: Optional[str] = None
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    location: str = Field(default="home")
    ts: Optional[int] = None
    note: Optional[str] = None
