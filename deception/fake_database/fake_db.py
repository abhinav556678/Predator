"""
PREDATOR Deception Subsystem - Fake Corporate Database
Simulates an internal SQLite database for Apex Global Financial / Enterprise Corp.
Contains dummy tables: `users`, `finance_records`, `server_inventory`, `credentials_vault`.
Logs all queries and attacker interactions into `interaction_audit_log`.
"""

import os
import sqlite3
import datetime
from typing import List, Dict, Any, Optional, Tuple

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_corporate.db")


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = db_path or os.getenv("DECEPTION_DB_PATH", DEFAULT_DB_PATH)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[str] = None, force_recreate: bool = False) -> str:
    path = db_path or os.getenv("DECEPTION_DB_PATH", DEFAULT_DB_PATH)
    if force_recreate and os.path.exists(path):
        os.remove(path)

    conn = get_db_connection(path)
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            full_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL,
            api_token TEXT NOT NULL,
            last_login TEXT NOT NULL
        )
    """)

    # 2. Finance Records Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE NOT NULL,
            account_number TEXT NOT NULL,
            vendor TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            approval_manager TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # 3. Server Inventory Table (Decoy infrastructure info)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS server_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT UNIQUE NOT NULL,
            ip_address TEXT NOT NULL,
            mac_address TEXT NOT NULL,
            os_version TEXT NOT NULL,
            environment TEXT NOT NULL,
            ssh_port INTEGER DEFAULT 22,
            admin_user TEXT NOT NULL
        )
    """)

    # 4. Honey Credentials Vault
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            system_name TEXT NOT NULL,
            username TEXT NOT NULL,
            secret_key TEXT NOT NULL,
            key_type TEXT NOT NULL,
            environment TEXT NOT NULL,
            notes TEXT
        )
    """)

    # 5. Interaction Audit Log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interaction_audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source_ip TEXT NOT NULL,
            action_type TEXT NOT NULL,
            query_string TEXT,
            rows_returned INTEGER DEFAULT 0,
            user_agent TEXT,
            notes TEXT
        )
    """)

    # Check if seeded
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        _seed_initial_data(cursor)

    conn.commit()
    conn.close()
    return path


def _seed_initial_data(cursor: sqlite3.Cursor):
    # Dummy Users
    dummy_users = [
        ("admin", "admin@apexfinancial.local", "System Administrator", "pbkdf2:sha256:600000$honey$8f4a9b2c3d4e", "SuperAdmin", "IT Infrastructure", "apk_live_99a8b7c6d5e4f3a2b1", "2026-09-30 18:24:12"),
        ("jdoe", "john.doe@apexfinancial.local", "John Doe", "pbkdf2:sha256:600000$honey$1c2d3e4f5a6b", "VP Finance", "Finance & Accounting", "apk_live_44b3c2d1e0f9a8b7c6", "2026-10-01 08:45:00"),
        ("asmith", "alice.smith@apexfinancial.local", "Alice Smith", "pbkdf2:sha256:600000$honey$9a8b7c6d5e4f", "Lead Auditor", "Internal Audit", "apk_live_12c3d4e5f6a7b8c9d0", "2026-10-01 09:12:33"),
        ("rwilliams", "robert.williams@apexfinancial.local", "Robert Williams", "pbkdf2:sha256:600000$honey$3e4f5a6b7c8d", "DevOps Engineer", "Engineering", "apk_live_55d6e7f8a9b0c1d2e3", "2026-09-29 22:10:04"),
        ("esato", "elena.sato@apexfinancial.local", "Elena Sato", "pbkdf2:sha256:600000$honey$7a8b9c0d1e2f", "Payroll Officer", "Human Resources", "apk_live_77e8f9a0b1c2d3e4f5", "2026-10-01 07:30:19"),
    ]
    cursor.executemany("""
        INSERT INTO users (username, email, full_name, password_hash, role, department, api_token, last_login)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, dummy_users)

    # Dummy Finance Records
    dummy_finance = [
        ("TX-2026-8801", "ACCT-90812-US", "Nordic Cloud Hosting Ltd", 145200.00, "USD", "Cloud Infrastructure", "APPROVED", "john.doe@apexfinancial.local", "2026-09-15"),
        ("TX-2026-8802", "ACCT-90812-US", "Global Swift Clearing AG", 894500.50, "USD", "Interbank Settlement", "APPROVED", "john.doe@apexfinancial.local", "2026-09-18"),
        ("TX-2026-8803", "ACCT-44102-CH", "Helvetia Vault Management", 350000.00, "CHF", "Offshore Asset Storage", "PENDING_EXEC_REVIEW", "john.doe@apexfinancial.local", "2026-09-25"),
        ("TX-2026-8804", "ACCT-90812-US", "Executive Retention Bonus Pool", 620000.00, "USD", "Executive Compensation", "RESTRICTED", "john.doe@apexfinancial.local", "2026-09-28"),
        ("TX-2026-8805", "ACCT-11928-UK", "Paladin Security Defense LLC", 82300.00, "GBP", "Physical & Cyber Security", "PAID", "alice.smith@apexfinancial.local", "2026-09-29"),
        ("TX-2026-8806", "ACCT-90812-US", "Cayman Enterprise Holdings", 1250000.00, "USD", "Capital Reallocation", "FLAGGED_CONFIDENTIAL", "john.doe@apexfinancial.local", "2026-09-30"),
    ]
    cursor.executemany("""
        INSERT INTO finance_records (transaction_id, account_number, vendor, amount, currency, category, status, approval_manager, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, dummy_finance)

    # Dummy Server Inventory
    dummy_servers = [
        ("dc-primary.corp.apex", "10.240.0.10", "00:1A:2B:3C:4D:5E", "Ubuntu Server 22.04 LTS", "Core DC", 22, "root"),
        ("db-finance-master.corp.apex", "10.240.0.15", "00:1A:2B:3C:4D:5F", "Debian 12 Bookworm", "Finance Subnet", 2222, "postgres"),
        ("k8s-ingress-prod.corp.apex", "10.240.1.20", "00:1A:2B:3C:4D:60", "RHEL 9.2 Enterprise", "DMZ", 22, "deploy"),
        ("vault-secrets.corp.apex", "10.240.2.5", "00:1A:2B:3C:4D:61", "Alpine Linux 3.19 (Hardened)", "Secure Enclave", 22, "vaultadmin"),
    ]
    cursor.executemany("""
        INSERT INTO server_inventory (hostname, ip_address, mac_address, os_version, environment, ssh_port, admin_user)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, dummy_servers)

    # Dummy Honey Credentials
    dummy_creds = [
        ("AWS S3 Asset Bucket", "predator-finance-backup-role", "HONEYTOKEN_AKIA_IOSFODNN7EXAMPLE:HONEYTOKEN_wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY", "AWS_ACCESS_KEY", "Production", "Full read/write permissions to s3://apex-financial-restricted-2026"),
        ("Production Database Superuser", "postgres_master", "ApexFinance_Vault_P@ssw0rd_2026!#", "DATABASE_PASSWORD", "Production", "Direct connection to 10.240.0.15:5432"),
        ("Corporate VPN Gateway", "vpnaudit_svc", "VpnToken-9941-SecKey-88210384", "VPN_CREDENTIAL", "DMZ", "Gateway: vpn.apexfinancial.com:1194"),
        ("Internal Docker Registry", "registry_writer", "dckr_pat_K3y99AbC_DecoyToken88123", "BEARER_TOKEN", "CI/CD", "Write access to internal harbor registry"),
    ]
    cursor.executemany("""
        INSERT INTO credentials_vault (system_name, username, secret_key, key_type, environment, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, dummy_creds)


def log_db_interaction(
    source_ip: str,
    action_type: str,
    query_string: Optional[str] = None,
    rows_returned: int = 0,
    user_agent: Optional[str] = None,
    notes: Optional[str] = None,
    db_path: Optional[str] = None
):
    """Logs any attacker query or database access into the audit table."""
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO interaction_audit_log (timestamp, source_ip, action_type, query_string, rows_returned, user_agent, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.datetime.now(datetime.timezone.utc).isoformat(),
            source_ip,
            action_type,
            query_string,
            rows_returned,
            user_agent,
            notes
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Deception DB Error] Failed to log interaction: {e}")


def get_all_users(limit: int = 50, source_ip: str = "127.0.0.1", user_agent: str = "unknown") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, full_name, role, department, api_token, last_login FROM users LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    log_db_interaction(source_ip, "QUERY_USERS", "SELECT * FROM users", len(rows), user_agent, "Attacker viewed user accounts")
    return rows


def get_all_finance_records(limit: int = 50, source_ip: str = "127.0.0.1", user_agent: str = "unknown") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM finance_records LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    log_db_interaction(source_ip, "QUERY_FINANCE", "SELECT * FROM finance_records", len(rows), user_agent, "Attacker accessed financial records")
    return rows


def get_all_server_inventory(limit: int = 50, source_ip: str = "127.0.0.1", user_agent: str = "unknown") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM server_inventory LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    log_db_interaction(source_ip, "QUERY_SERVERS", "SELECT * FROM server_inventory", len(rows), user_agent, "Attacker scouted server infrastructure")
    return rows


def get_all_credentials(limit: int = 50, source_ip: str = "127.0.0.1", user_agent: str = "unknown") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM credentials_vault LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    log_db_interaction(source_ip, "QUERY_CREDENTIALS", "SELECT * FROM credentials_vault", len(rows), user_agent, "Attacker accessed decoy credentials vault")
    return rows


def execute_custom_sql(
    sql_query: str,
    source_ip: str = "127.0.0.1",
    user_agent: str = "unknown"
) -> Tuple[bool, List[Dict[str, Any]], str]:
    """
    Safely executes arbitrary queries from attacker on the fake database.
    Allows attacker to feel successful while capturing every detail of their SQL injection / query.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        if sql_query.strip().upper().startswith(("SELECT", "PRAGMA", "EXPLAIN")):
            rows = [dict(r) for r in cursor.fetchall()]
            conn.close()
            log_db_interaction(source_ip, "CUSTOM_SQL_QUERY", sql_query, len(rows), user_agent, "Attacker executed custom SQL query")
            return True, rows, "Query executed successfully"
        else:
            conn.commit()
            changes = conn.total_changes
            conn.close()
            log_db_interaction(source_ip, "CUSTOM_SQL_MUTATION", sql_query, changes, user_agent, "Attacker modified fake database")
            return True, [{"affected_rows": changes}], f"{changes} row(s) updated"
    except Exception as e:
        error_msg = str(e)
        conn.close()
        log_db_interaction(source_ip, "CUSTOM_SQL_ERROR", sql_query, 0, user_agent, f"SQL error: {error_msg}")
        return False, [], error_msg


def get_recent_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interaction_audit_log ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


if __name__ == "__main__":
    db_file = init_db(force_recreate=True)
    print(f"[+] Initialized Fake Corporate Database at: {db_file}")
    users = get_all_users()
    print(f"[+] Loaded {len(users)} users.")
    finance = get_all_finance_records()
    print(f"[+] Loaded {len(finance)} finance records.")
