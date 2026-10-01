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
    ids = [d["id"] for d in data]
    assert "INC-001" in ids
    assert "INC-002" in ids

def test_get_incidents_cors():
    response = client.options(
        "/incidents",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") in ["*", "http://localhost:5173"]

def test_websocket_connection():
    with client.websocket_connect("/ws/incidents") as websocket:
        # Just connecting and then closing is enough to test it works
        pass
