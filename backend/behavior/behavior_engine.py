from datetime import datetime, timedelta
import json
import uuid
from sqlalchemy.orm import Session
from .. import models

def analyze_incident(incident: models.Incident, event_types: list):
    # Dummy ML Logic
    if "DECEPTION_ACCESS" in event_types:
        incident.stage = "IMPACT"
        incident.predicted_stage = "CONTAINMENT"
        incident.risk_level = "CRITICAL"
        incident.description = "Critical: Deception environment accessed."
    elif "SSH_AUTH_FAILED" in event_types:
        incident.stage = "CREDENTIAL ACCESS"
        incident.predicted_stage = "LATERAL MOVEMENT"
        incident.risk_level = "HIGH"
    elif "OS_TELEMETRY" in event_types:
        incident.stage = "DISCOVERY"
        incident.predicted_stage = "CREDENTIAL ACCESS"
        incident.risk_level = "MEDIUM"
    else:
        incident.stage = "INITIAL ACCESS"
        incident.predicted_stage = "DISCOVERY"
        incident.risk_level = "LOW"

def process_event(db: Session, new_event: models.Event):
    payload = json.loads(new_event.payload)
    source_ip = payload.get("source_ip")
    event_type = payload.get("event_type", "UNKNOWN")
    
    if not source_ip:
        return

    now = datetime.utcnow()
    is_immediate_trigger = event_type == "DECEPTION_ACCESS"
    one_min_ago = now - timedelta(minutes=1)
    
    recent_events = db.query(models.Event).filter(
        models.Event.received_at >= one_min_ago
    ).all()
    
    recent_types = []
    count = 0
    for e in recent_events:
        e_payload = json.loads(e.payload)
        if e_payload.get("source_ip") == source_ip:
            count += 1
            recent_types.append(e_payload.get("event_type", "UNKNOWN"))
            
    if count >= 5 or is_immediate_trigger:
        five_mins_ago = now - timedelta(minutes=5)
        existing_incident = db.query(models.Incident).filter(
            models.Incident.endpoint == source_ip,
            models.Incident.timestamp >= five_mins_ago
        ).first()
        
        if existing_incident:
            analyze_incident(existing_incident, recent_types)
            db.commit()
            print(f"*** INCIDENT UPDATED: {existing_incident.id} for {source_ip} ***")
        else:
            incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
            new_incident = models.Incident(
                id=incident_id,
                endpoint=source_ip,
                description=f"Behavior Engine: Suspicious activity detected."
            )
            analyze_incident(new_incident, recent_types)
            db.add(new_incident)
            db.commit()
            print(f"*** NEW INCIDENT CREATED: {incident_id} for {source_ip} ***")
