from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "PREDATOR API is running"}

def test_post_event():
    response = client.post("/events", json={"event_type": "test", "data": "hello"})
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Event received"}

def test_get_incidents():
    response = client.get("/incidents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == "INC-001"
