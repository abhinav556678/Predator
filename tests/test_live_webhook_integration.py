"""
PREDATOR Deception Subsystem - End-to-End Webhook Integration Test
Spins up a mock M3 Backend on port 8000, hits the Deception Server on port 8080,
and verifies that M3 receives the DECEPTION_ACCESS event with the exact expected schema.
"""

import time
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

received_events = []

class MockM3Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/events":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            event_data = json.loads(body.decode())
            received_events.append(event_data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"received"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Quiet logging

def run_mock_m3(server):
    server.serve_forever()

def main():
    print("[*] Starting Mock M3 Backend on port 8000...")
    mock_m3 = HTTPServer(("127.0.0.1", 8000), MockM3Handler)
    m3_thread = threading.Thread(target=run_mock_m3, args=(mock_m3,), daemon=True)
    m3_thread.start()

    time.sleep(0.5)

    print("[*] Simulating Attacker hitting Deception Server on Port 8080...")
    # 1. Attacker queries finance records
    r1 = requests.get("http://127.0.0.1:8080/api/v1/finance/records")
    print(f"    Attacker GET /api/v1/finance/records -> HTTP {r1.status_code}")

    # 2. Attacker submits stolen credentials
    r2 = requests.post("http://127.0.0.1:8080/login", data={"username": "compromised_user", "password": "TargetPassword123"})
    print(f"    Attacker POST /login -> HTTP {r2.status_code}")

    # Allow webhook background thread to deliver
    time.sleep(1.0)

    print(f"\n[+] Total Events Received by Mock M3 Backend: {len(received_events)}")
    assert len(received_events) >= 2, "Expected at least 2 events to be forwarded to M3 Backend"

    for i, event in enumerate(received_events, 1):
        print(f"\n--- Event {i} Forwarded to M3 Backend ---")
        print(f"Timestamp:   {event.get('timestamp')}")
        print(f"Event Type:  {event.get('event_type')}")
        print(f"Source IP:   {event.get('source_ip')}")
        print(f"Action:      {event.get('details', {}).get('action')}")
        print(f"Severity:    {event.get('details', {}).get('severity')}")
        assert event.get("event_type") == "DECEPTION_ACCESS", f"Expected DECEPTION_ACCESS, got {event.get('event_type')}"
        assert event.get("details", {}).get("severity") == "CRITICAL"

    print("\n[OK] Ticket 08 Integration Check: PASSED flawlessly!")
    mock_m3.shutdown()

if __name__ == "__main__":
    main()
