"""
PREDATOR Deception Subsystem - Automated Test Suite
Tests fake database, honeypot REST endpoints, query logging, and event formatting.
Run with:
    python -m unittest tests/test_deception.py
"""

import os
import sys
import unittest
from pathlib import Path
from starlette.testclient import TestClient

# Ensure root directory is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from deception.fake_database.fake_db import (
    init_db,
    get_all_users,
    get_all_finance_records,
    get_all_server_inventory,
    get_all_credentials,
    execute_custom_sql,
    get_recent_audit_logs
)
from deception.fake_server.webhook import format_deception_event
from deception.fake_server.server import app

client = TestClient(app)


class TestDeceptionDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = init_db()

    def test_database_tables_seeded(self):
        users = get_all_users()
        finance = get_all_finance_records()
        servers = get_all_server_inventory()
        creds = get_all_credentials()

        self.assertGreaterEqual(len(users), 5, "Users table not properly seeded")
        self.assertGreaterEqual(len(finance), 5, "Finance table not properly seeded")
        self.assertGreaterEqual(len(servers), 4, "Server inventory not seeded")
        self.assertGreaterEqual(len(creds), 4, "Decoy credentials not seeded")

    def test_custom_sql_execution(self):
        success, rows, msg = execute_custom_sql("SELECT username, email FROM users WHERE username='admin'")
        self.assertTrue(success)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["username"], "admin")

    def test_audit_log_captures_query(self):
        execute_custom_sql("SELECT * FROM finance_records WHERE currency='CHF'", source_ip="192.168.1.55")
        logs = get_recent_audit_logs(limit=10)
        self.assertGreater(len(logs), 0)
        recent_query = [l for l in logs if "192.168.1.55" in l["source_ip"]]
        self.assertTrue(len(recent_query) > 0, "Audit log failed to record source IP")


class TestWebhookEventFormatting(unittest.TestCase):
    def test_event_payload_schema(self):
        payload = format_deception_event(
            source_ip="192.168.1.100",
            action="HONEYPOT_HIT",
            path="/api/v1/finance/records",
            method="GET",
            status_code=200,
            user_agent="curl/8.4.0",
            extra_details={"test_flag": True}
        )

        self.assertEqual(payload["event_type"], "DECEPTION_ACCESS")
        self.assertEqual(payload["source_ip"], "192.168.1.100")
        self.assertIn("timestamp", payload)
        self.assertIn("details", payload)
        self.assertEqual(payload["details"]["action"], "HONEYPOT_HIT")
        self.assertEqual(payload["details"]["severity"], "CRITICAL")
        self.assertTrue(payload["details"]["test_flag"])


class TestDeceptionServerRoutes(unittest.TestCase):
    def test_healthcheck(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("status"), "active")

    def test_portal_html_rendered(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("Apex Global Financial", response.text)

    def test_portal_json_for_curl(self):
        response = client.get("/", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/json", response.headers["content-type"])
        self.assertIn("endpoints", response.json())

    def test_login_post_captures_credentials(self):
        response = client.post(
            "/login",
            data={"username": "hacker@evil.corp", "password": "SuperSecretPassword123"}
        )
        self.assertEqual(response.status_code, 200)

    def test_api_users(self):
        response = client.get("/api/v1/users")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["count"], 0)

    def test_api_finance_records(self):
        response = client.get("/api/v1/finance/records")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["total_records"], 0)

    def test_api_custom_sql_query(self):
        response = client.post(
            "/api/v1/query",
            json={"query": "SELECT count(*) as total FROM users"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["rows"][0]["total"], 5)

    def test_honey_document_download(self):
        response = client.get("/documents/q3_confidential_financials.csv")
        self.assertEqual(response.status_code, 200)
        self.assertIn("TransactionID", response.text)

    def test_reconnaissance_catchall(self):
        response = client.get("/wp-admin/sensitive.php")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Endpoint '/wp-admin/sensitive.php' is restricted", response.json()["message"])


if __name__ == "__main__":
    unittest.main()
