import os

os.makedirs('backend/api', exist_ok=True)

with open('backend/requirements.txt', 'w') as f:
    f.write('fastapi\nuvicorn\nsqlalchemy\npydantic\n')

with open('backend/__init__.py', 'w') as f:
    pass

with open('backend/api/__init__.py', 'w') as f:
    pass

with open('backend/database.py', 'w') as f:
    f.write('''from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./predator.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')

with open('backend/models.py', 'w') as f:
    f.write('''from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    payload = Column(Text) # Raw JSON string

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    stage = Column(String)
    risk_level = Column(String)
    endpoint = Column(String)
    description = Column(String)
''')

with open('backend/schemas.py', 'w') as f:
    f.write('''from pydantic import BaseModel
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
''')

with open('backend/api/events.py', 'w') as f:
    f.write('''from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import json
from .. import models, database

router = APIRouter()

@router.post("/events")
async def create_event(request: Request, db: Session = Depends(database.get_db)):
    payload = await request.json()
    print(f"Received event: {json.dumps(payload, indent=2)}")
    
    db_event = models.Event(payload=json.dumps(payload))
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return {"status": "ok", "message": "Event received"}
''')

with open('backend/api/incidents.py', 'w') as f:
    f.write('''from fastapi import APIRouter
from .. import schemas
from datetime import datetime, timezone

router = APIRouter()

MOCK_INCIDENTS = [
    {
        "id": "INC-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stage": "CREDENTIAL ACCESS",
        "risk_level": "HIGH",
        "endpoint": "EMPLOYEE-03",
        "description": "Suspicious login followed by credential directory access."
    },
    {
        "id": "INC-002",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stage": "DISCOVERY",
        "risk_level": "MEDIUM",
        "endpoint": "SERVER-01",
        "description": "Unusual internal scanning behavior detected."
    }
]

@router.get("/incidents")
def get_incidents():
    return MOCK_INCIDENTS
''')

with open('backend/main.py', 'w') as f:
    f.write('''from fastapi import FastAPI
from . import models
from .database import engine
from .api import events, incidents

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PREDATOR Backend")

app.include_router(events.router)
app.include_router(incidents.router)

@app.get("/")
def read_root():
    return {"message": "PREDATOR API is running"}
''')
