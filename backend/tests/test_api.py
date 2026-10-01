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
    assert isinstance(data, list)

def test_behavior_engine_triggers_incident():
    # Send 5 events quickly from a single IP
    for _ in range(5):
        client.post("/events", json={"source_ip": "10.0.0.99", "event_type": "TEST"})
    
    # Check incidents
    response = client.get("/incidents")
    data = response.json()
    
    # We should have at least one incident created for 10.0.0.99
    found = any(inc["endpoint"] == "10.0.0.99" for inc in data)
    assert found
