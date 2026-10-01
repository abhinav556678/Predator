from fastapi import APIRouter
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
    return sorted(MOCK_INCIDENTS, key=lambda x: x["timestamp"], reverse=True)

def add_incident(incident_data: dict):
    # Auto-generate ID if not present
    if "id" not in incident_data:
        incident_data["id"] = f"INC-{len(MOCK_INCIDENTS) + 1:03d}"
    if "timestamp" not in incident_data:
        incident_data["timestamp"] = datetime.now(timezone.utc).isoformat()
    MOCK_INCIDENTS.append(incident_data)
    return incident_data
