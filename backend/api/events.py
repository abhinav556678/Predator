from fastapi import APIRouter, Depends, Request
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
