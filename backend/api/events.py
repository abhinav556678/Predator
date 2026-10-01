from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import json
from .. import models, database
from ..behavior.behavior_engine import process_event

router = APIRouter()

@router.post("/events")
async def create_event(request: Request, db: Session = Depends(database.get_db)):
    try:
        payload = await request.json()
    except json.JSONDecodeError:
        payload = {}
        
    print(f"Event Received: {json.dumps(payload, indent=2)}")
    
    db_event = models.Event(payload=json.dumps(payload))
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    if payload:
        process_event(db, db_event)
    
    return {"status": "ok", "message": "Event received"}
