from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import json
from .. import models, database
from .incidents import add_incident
from ..websocket_manager import manager

router = APIRouter()

@router.post("/events")
async def create_event(request: Request, db: Session = Depends(database.get_db)):
    payload = await request.json()
    print(f"Received event: {json.dumps(payload, indent=2)}")
    
    db_event = models.Event(payload=json.dumps(payload))
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # If the event payload simulates an incident, add it and broadcast
    if payload.get("event_type") == "high-risk" or payload.get("is_incident"):
        new_incident = add_incident({
            "stage": payload.get("stage", "EXECUTION"),
            "risk_level": payload.get("risk_level", "CRITICAL"),
            "endpoint": payload.get("endpoint", "UNKNOWN-ENDPOINT"),
            "description": payload.get("description", "High-risk behavior detected via telemetry.")
        })
        await manager.broadcast({"type": "NEW_INCIDENT", "data": new_incident})
    
    return {"status": "ok", "message": "Event received"}
