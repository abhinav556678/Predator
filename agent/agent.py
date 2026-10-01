import time
import json
import requests
import socket
from datetime import datetime, timezone
import argparse

def get_local_ip():
    try:
        # Create a dummy socket to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def create_dummy_payload(source_ip):
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "DUMMY_TELEMETRY",
        "source_ip": source_ip,
        "details": {
            "message": "This is a dummy event to test connectivity.",
            "cpu_usage": 5.2,
            "memory_usage": 42.1
        }
    }

def send_event(backend_url, payload):
    url = f"{backend_url.rstrip('/')}/events"
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        print(f"[{payload['timestamp']}] Successfully sent event to {url}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[{payload['timestamp']}] Failed to send event to {url}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="PREDATOR Agent (Dummy Telemetry)")
    parser.add_argument("--backend", type=str, default="http://127.0.0.1:8000", help="URL of the PREDATOR backend")
    parser.add_argument("--interval", type=int, default=5, help="Interval in seconds between events")
    args = parser.parse_args()

    print(f"Starting PREDATOR Agent...")
    print(f"Backend URL: {args.backend}")
    print(f"Interval: {args.interval} seconds")
    
    source_ip = get_local_ip()
    print(f"Detected local IP: {source_ip}")
    print("-" * 40)

    try:
        while True:
            payload = create_dummy_payload(source_ip)
            send_event(args.backend, payload)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")

if __name__ == "__main__":
    main()
