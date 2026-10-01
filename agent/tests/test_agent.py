import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import responses
from agent import create_dummy_payload, send_event

def test_create_dummy_payload():
    payload = create_dummy_payload("192.168.1.5")
    assert "timestamp" in payload
    assert payload["event_type"] == "DUMMY_TELEMETRY"
    assert payload["source_ip"] == "192.168.1.5"
    assert "details" in payload
    assert payload["details"]["cpu_usage"] == 5.2

@responses.activate
def test_send_event_success():
    backend_url = "http://testserver:8000"
    payload = create_dummy_payload("10.0.0.1")
    
    responses.add(
        responses.POST,
        "http://testserver:8000/events",
        json={"status": "ok"},
        status=200
    )
    
    success = send_event(backend_url, payload)
    assert success is True
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://testserver:8000/events"

@responses.activate
def test_send_event_failure():
    backend_url = "http://testserver:8000"
    payload = create_dummy_payload("10.0.0.1")
    
    responses.add(
        responses.POST,
        "http://testserver:8000/events",
        status=500
    )
    
    success = send_event(backend_url, payload)
    assert success is False
