from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import json
from .. import models, database
from ..behavior.behavior_engine import process_event
from ..websocket_manager import manager

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
        
    # Optional: broad cast generic telemetry update?
    # Actually, we can just leave it as process_event, and broadcast should happen inside behavior_engine, 
    # but for now let's just make it compilable.
    
    return {"status": "ok", "message": "Event received"}
