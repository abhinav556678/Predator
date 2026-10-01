from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncidentBase(BaseModel):
    id: str
    timestamp: datetime
    stage: str
    predicted_stage: Optional[str] = None
    risk_level: str
    endpoint: str
    description: str

    class Config:
        from_attributes = True
