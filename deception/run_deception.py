"""
PREDATOR Deception Subsystem - Standalone Runner
CLI to launch the fake server and honeypot services.
Usage:
    python deception/run_deception.py
    python deception/run_deception.py --port 8080 --m3-ip 192.168.1.10
"""

import argparse
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from deception.fake_server.server import run_server
from deception.fake_database.fake_db import init_db

def main():
    parser = argparse.ArgumentParser(description="PREDATOR Deception Honeypot Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on (default: 8080)")
    parser.add_argument("--m3-ip", default=None, help="M3 Backend IP address (default: 127.0.0.1)")
    parser.add_argument("--m3-port", type=int, default=8000, help="M3 Backend Port (default: 8000)")
    parser.add_argument("--reinit-db", action="store_true", help="Recreate fake corporate SQLite database")
    args = parser.parse_args()

    if args.m3_ip:
        os.environ["M3_IP"] = args.m3_ip
        os.environ["M3_BACKEND_URL"] = f"http://{args.m3_ip}:{args.m3_port}/events"

    if args.reinit_db:
        print("[*] Reinitializing fake database...")
        init_db(force_recreate=True)

    run_server(host=args.host, port=args.port)

if __name__ == "__main__":
    main()
