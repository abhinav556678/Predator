from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, database

router = APIRouter()

@router.get("/incidents")
def get_incidents(db: Session = Depends(database.get_db)):
    incidents = db.query(models.Incident).order_by(models.Incident.timestamp.desc()).all()
    # Format them cleanly for the frontend
    result = []
    for inc in incidents:
        result.append({
            "id": inc.id,
            "timestamp": inc.timestamp.isoformat() if inc.timestamp else None,
            "stage": inc.stage,
            "predicted_stage": inc.predicted_stage,
            "risk_level": inc.risk_level,
            "endpoint": inc.endpoint,
            "description": inc.description
        })
    return result
