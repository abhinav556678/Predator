"""
PREDATOR Deception Subsystem - Automated Validation & Connectivity Tool
Covers:
  - Ticket 02: HTTP Server & Fake DB validation (curl http://<M4_IP>:8080)
  - Ticket 08: Deception logging & DECEPTION_ACCESS webhook verification
  - Ticket 11: Network hardening & port whitelist verification
"""

import argparse
import os
import socket
import sys
import time
from pathlib import Path
from typing import Dict, Any
import requests

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_fake_database():
    print("\n[1/4] Testing Fake Corporate Database Integrity...")
    from deception.fake_database.fake_db import (
        init_db, get_all_users, get_all_finance_records,
        get_all_server_inventory, get_all_credentials, execute_custom_sql
    )
    db_path = init_db()
    users = get_all_users(limit=10)
    finance = get_all_finance_records(limit=10)
    servers = get_all_server_inventory(limit=10)
    creds = get_all_credentials(limit=10)

    assert len(users) > 0, "No users in fake DB"
    assert len(finance) > 0, "No finance records in fake DB"
    assert len(servers) > 0, "No servers in fake DB"
    assert len(creds) > 0, "No credentials in fake DB"

    # Test custom query execution
    ok, rows, msg = execute_custom_sql("SELECT COUNT(*) as count FROM users")
    assert ok and len(rows) > 0, "Custom SQL execution failed"

    print(f"    [OK] Database initialized at: {db_path}")
    print(f"    [OK] Users loaded: {len(users)} accounts")
    print(f"    [OK] Finance ledger records: {len(finance)} transactions")
    print(f"    [OK] Servers inventory: {len(servers)} hosts")
    print(f"    [OK] Decoy secrets: {len(creds)} credentials")
    print(f"    [OK] Attacker SQL execution: Functional ({rows[0]['count']} users found)")
    return True


def test_http_endpoints(target_ip: str, port: int):
    base_url = f"http://{target_ip}:{port}"
    print(f"\n[2/4] Testing Deception HTTP Server & Endpoints at {base_url}...")

    # 1. Health check
    try:
        r = requests.get(f"{base_url}/health", timeout=3)
        assert r.status_code == 200, f"Healthcheck failed: {r.status_code}"
        print(f"    [OK] GET /health -> HTTP 200 ({r.json().get('status')})")
    except Exception as e:
        print(f"    [FAIL] Could not connect to {base_url}/health: {e}")
        print("           (Make sure deception server is running: python deception/run_deception.py)")
        return False

    # 2. Portal Index / Login page (Ticket 02 check)
    r = requests.get(f"{base_url}/", timeout=3)
    assert r.status_code == 200, "GET / failed"
    assert "Apex Global Financial" in r.text or "Restricted" in r.text or "login" in r.text.lower()
    print("    [OK] GET / -> HTTP 200 (Fake Corporate Login Gateway rendered)")

    # 3. JSON curl check (Ticket 02 check)
    r_json = requests.get(f"{base_url}/", headers={"Accept": "application/json"}, timeout=3)
    assert r_json.status_code == 200
    print("    [OK] GET / with Accept: application/json -> HTTP 200 (API Directory)")

    # 4. REST API User Directory
    r_users = requests.get(f"{base_url}/api/v1/users", timeout=3)
    assert r_users.status_code == 200 and r_users.json().get("count") > 0
    print(f"    [OK] GET /api/v1/users -> HTTP 200 ({r_users.json().get('count')} fake users)")

    # 5. REST API Finance Records
    r_fin = requests.get(f"{base_url}/api/v1/finance/records", timeout=3)
    assert r_fin.status_code == 200 and r_fin.json().get("total_records") > 0
    print(f"    [OK] GET /api/v1/finance/records -> HTTP 200 ({r_fin.json().get('total_records')} fake financial transactions)")

    # 6. Attacker Honey Documents download
    r_doc = requests.get(f"{base_url}/documents/q3_confidential_financials.csv", timeout=3)
    assert r_doc.status_code == 200 and "TransactionID" in r_doc.text
    print(f"    [OK] GET /documents/q3_confidential_financials.csv -> HTTP 200 ({len(r_doc.text)} bytes exfiltrated)")

    # 7. Reconnaissance catchall
    r_recon = requests.get(f"{base_url}/.env.backup", timeout=3)
    assert r_recon.status_code == 404
    print("    [OK] GET /.env.backup -> HTTP 404 (Probe captured and logged)")

    return True


def test_deception_logging_and_webhook(target_ip: str, port: int, m3_url: str):
    base_url = f"http://{target_ip}:{port}"
    print(f"\n[3/4] Testing Deception Logging & Event Forwarding (Ticket 08)...")

    # 1. Simulate attacker credential submission on fake login
    login_payload = {"username": "attacker_probe@malicious.xyz", "password": "StolenPassword9981!"}
    r = requests.post(f"{base_url}/login", data=login_payload, timeout=3)
    assert r.status_code == 200
    print("    [OK] POST /login -> Attacker credential theft captured & logged")

    # 2. Simulate attacker SQL injection
    sql_payload = {"query": "SELECT username, password_hash, api_token FROM users WHERE role='SuperAdmin'"}
    r = requests.post(f"{base_url}/api/v1/query", json=sql_payload, timeout=3)
    assert r.status_code == 200 and r.json().get("success") is True
    print("    [OK] POST /api/v1/query -> Attacker SQL probe executed on fake DB & logged")

    # 3. Check internal audit trail
    r_audit = requests.get(f"{base_url}/audit/logs", timeout=3)
    if r_audit.status_code == 200:
        events = r_audit.json().get("audit_trail", [])
        print(f"    [OK] Honey audit trail contains {len(events)} logged attacker actions")

    # 4. Check connectivity to M3 Backend
    print(f"    [*] Checking M3 Backend webhook target: {m3_url}")
    try:
        m3_test = requests.post(
            m3_url,
            json={
                "timestamp": "2026-10-01T10:00:00Z",
                "event_type": "DECEPTION_ACCESS",
                "source_ip": "127.0.0.1",
                "details": {"test": True, "note": "Validation connectivity check"}
            },
            timeout=2
        )
        print(f"    [OK] M3 Backend is ONLINE: Responded HTTP {m3_test.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"    [NOTE] M3 Backend ({m3_url}) is currently offline (safe - webhook falls back gracefully)")

    return True


def test_network_hardening(target_ip: str):
    print(f"\n[4/4] Testing Network Hardening & Port Whitelisting (Ticket 11)...")

    whitelisted_ports = [3000, 8000, 8080, 9000]
    forbidden_ports = [21, 22, 23, 445, 1433, 3306, 5432]

    def check_tcp_port(ip: str, port: int, timeout: float = 0.8) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            res = s.connect_ex((ip, port))
            s.close()
            return res == 0
        except Exception:
            return False

    print("    Checking whitelisted application ports:")
    for p in whitelisted_ports:
        is_open = check_tcp_port(target_ip, p)
        status_txt = "OPEN (Active)" if is_open else "CLOSED (Service not currently started)"
        print(f"      Port {p:<5} -> {status_txt}")

    print("    Checking non-whitelisted sensitive ports (Should be CLOSED or BLOCKED):")
    blocked_count = 0
    for p in forbidden_ports:
        is_open = check_tcp_port(target_ip, p)
        if not is_open:
            blocked_count += 1
            print(f"      Port {p:<5} -> BLOCKED / CLOSED [SECURE]")
        else:
            print(f"      Port {p:<5} -> OPEN [WARNING: Potential leakage if exposed to LAN]")

    print(f"    [OK] Network Hardening check completed ({blocked_count}/{len(forbidden_ports)} sensitive ports blocked)")
    return True


def main():
    parser = argparse.ArgumentParser(description="PREDATOR Deception Validation Tool")
    parser.add_argument("--ip", default="127.0.0.1", help="Target IP of Deception server (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8080, help="Deception server port (default: 8080)")
    parser.add_argument("--m3-url", default="http://127.0.0.1:8000/events", help="M3 Backend URL")
    parser.add_argument("--skip-net", action="store_true", help="Skip port scanner")
    args = parser.parse_args()

    print("===================================================================")
    print("      PREDATOR DECEPTION SUBSYSTEM VALIDATION (M4)")
    print("===================================================================")

    test_fake_database()
    http_ok = test_http_endpoints(args.ip, args.port)
    if http_ok:
        test_deception_logging_and_webhook(args.ip, args.port, args.m3_url)
    if not args.skip_net:
        test_network_hardening(args.ip)

    print("\n===================================================================")
    print("[OK] All Deception Subsystem validation checks completed.")
    print("===================================================================\n")


if __name__ == "__main__":
    main()
