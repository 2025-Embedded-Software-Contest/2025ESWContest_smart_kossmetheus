from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class FallAlert(BaseModel):
    user_id: str
    severity: str = Field(..., pattern="^(low|medium|high)$")
    location: str = Field(..., example="home")
    meta: Optional[Dict[str, Any]] = None
