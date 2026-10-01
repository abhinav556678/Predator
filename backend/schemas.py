from pydantic import BaseModel
from datetime import datetime

class IncidentBase(BaseModel):
    id: str
    timestamp: datetime
    stage: str
    risk_level: str
    endpoint: str
    description: str

    class Config:
        from_attributes = True
