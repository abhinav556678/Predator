from datetime import datetime, timedelta
import json
import uuid
from sqlalchemy.orm import Session
from .. import models

def process_event(db: Session, new_event: models.Event):
    payload = json.loads(new_event.payload)
    source_ip = payload.get("source_ip")
    
    if not source_ip:
        return

    # Use naive UTC datetimes for SQLite compatibility
    now = datetime.utcnow()
    one_min_ago = now - timedelta(minutes=1)
    
    # SQLite datetime strings are comparable
    recent_events = db.query(models.Event).filter(
        models.Event.received_at >= one_min_ago
    ).all()
    
    count = 0
    for e in recent_events:
        e_payload = json.loads(e.payload)
        if e_payload.get("source_ip") == source_ip:
            count += 1
            
    if count >= 5:
        # Check if an incident already exists for this IP in the last 5 minutes
        five_mins_ago = now - timedelta(minutes=5)
        existing_incident = db.query(models.Incident).filter(
            models.Incident.endpoint == source_ip,
            models.Incident.timestamp >= five_mins_ago
        ).first()
        
        if not existing_incident:
            incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
            new_incident = models.Incident(
                id=incident_id,
                stage="SUSPICIOUS ACTIVITY",
                risk_level="HIGH",
                endpoint=source_ip,
                description=f"Behavior Engine: {count} events detected within 1 minute from {source_ip}"
            )
            db.add(new_incident)
            db.commit()
            print(f"*** NEW INCIDENT CREATED: {incident_id} for {source_ip} ***")
