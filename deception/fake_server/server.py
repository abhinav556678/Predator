"""
PREDATOR Deception Subsystem - Fake Decoy Server
Ticket 02: Deception Environment Setup
Ticket 08: Deception Logging & Event Forwarding
Simulates an internal corporate intranet portal & REST API on System 1 (Port 8080 / 9000).
Logs all attacker interactions and immediately forwards `DECEPTION_ACCESS` events to M3 Backend.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from deception.fake_server.config import (
    DECEPTION_HOST,
    DECEPTION_PORT,
    DECEPTION_DOCS_DIR,
    DECEPTION_CREDS_DIR,
    DECEPTION_DB_PATH
)
from deception.fake_server.webhook import forward_deception_event, logger
from deception.fake_server.portal_html import (
    get_login_page_html,
    get_dashboard_html,
    get_admin_sql_html
)
from deception.fake_database.fake_db import (
    init_db,
    get_all_users,
    get_all_finance_records,
    get_all_server_inventory,
    get_all_credentials,
    execute_custom_sql,
    get_recent_audit_logs
)

# Initialize database
init_db(DECEPTION_DB_PATH)

app = FastAPI(
    title="Apex Corporate Intranet (PREDATOR Deception Subsystem)",
    description="Decoy corporate portal and internal API honeypot",
    version="2.0.0"
)

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_client_ip(request: Request) -> str:
    """Extracts client IP, respecting X-Forwarded-For if proxied."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "127.0.0.1"


class GlobalDeceptionMiddleware(BaseHTTPMiddleware):
    """
    Middleware that intercepts EVERY single HTTP request touching the deception server.
    Logs the interaction and dispatches a DECEPTION_ACCESS event to the M3 Backend.
    """
    async def dispatch(self, request: Request, call_next):
        client_ip = get_client_ip(request)
        method = request.method
        path = request.url.path
        user_agent = request.headers.get("user-agent", "unknown")

        # Skip noisy browser favicon queries for cleaner logs if desired, but still process
        action_category = "HONEYPOT_HTTP_ACCESS"
        if "login" in path:
            action_category = "HONEYPOT_LOGIN_PROBE"
        elif "finance" in path:
            action_category = "HONEYPOT_FINANCIAL_ACCESS"
        elif "admin" in path or "query" in path:
            action_category = "HONEYPOT_DATABASE_PROBE"
        elif "document" in path:
            action_category = "HONEYPOT_DOCUMENT_ACCESS"
        elif "credential" in path or ".env" in path or "ssh" in path:
            action_category = "HONEYPOT_CREDENTIAL_ACCESS"

        # Execute downstream request
        response = await call_next(request)

        # Forward DECEPTION_ACCESS event asynchronously to M3 Backend
        forward_deception_event(
            source_ip=client_ip,
            action=action_category,
            path=path,
            method=method,
            status_code=response.status_code,
            user_agent=user_agent,
            extra_details={
                "query_params": str(request.query_params),
                "client_host": client_ip,
                "portal_asset": "Apex Financial Corporate Gateway"
            }
        )

        return response


app.add_middleware(GlobalDeceptionMiddleware)


# -------------------------------------------------------------------------
# Web Portal & Authentication Decoy Routes
# -------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def root_index(request: Request):
    """
    Root entry point.
    If requested via curl or with Accept: application/json, returns JSON response.
    Otherwise serves the realistic Corporate Intranet Login portal.
    """
    accept_header = request.headers.get("accept", "")
    user_agent = request.headers.get("user-agent", "").lower()

    # If client prefers JSON (e.g. API clients)
    if "application/json" in accept_header and "text/html" not in accept_header:
        return JSONResponse({
            "service": "Apex Global Financial Internal Intranet Gateway",
            "version": "v4.12.0-enterprise",
            "status": "RESTRICTED_ACCESS",
            "authentication": "Bearer / Session required",
            "endpoints": {
                "login": "/login",
                "portal": "/portal",
                "users_api": "/api/v1/users",
                "finance_api": "/api/v1/finance/records",
                "servers_api": "/api/v1/servers",
                "documents": "/documents",
                "admin_sql": "/admin"
            }
        })

    # Default: Corporate SSO Login HTML
    return HTMLResponse(get_login_page_html())


@app.get("/login", response_class=HTMLResponse)
async def login_get():
    """Renders the fake corporate login page."""
    return HTMLResponse(get_login_page_html())


@app.post("/login")
async def login_post(request: Request):
    """
    Captures attacker authentication attempts.
    Logs harvested credentials and returns a simulated session or portal redirect.
    """
    client_ip = get_client_ip(request)
    username = None
    password = None

    # Try extracting from form-data or urlencoded
    try:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
    except Exception:
        pass

    # Try extracting from JSON if not in form
    if not username:
        try:
            body = await request.json()
            username = body.get("username")
            password = body.get("password")
        except Exception:
            pass

    # Log credential theft / brute-force attempt
    forward_deception_event(
        source_ip=client_ip,
        action="CREDENTIAL_SUBMISSION",
        path="/login",
        method="POST",
        status_code=200,
        user_agent=request.headers.get("user-agent"),
        extra_details={
            "submitted_username": username or "<blank>",
            "password_length": len(password) if password else 0,
            "credential_harvested": True
        }
    )

    accept_header = request.headers.get("accept", "")
    if "application/json" in accept_header:
        return JSONResponse({
            "status": "authenticated",
            "message": f"Welcome, {username or 'admin'}. Session granted.",
            "session_token": "apk_sess_77a9b0c1d2e3f4a5b6c7",
            "role": "FinanceAuditor",
            "redirect_url": "/portal"
        })

    # Serve the authenticated portal dashboard
    return HTMLResponse(get_dashboard_html(username or "Finance Admin"))


@app.get("/portal", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
async def portal_dashboard():
    """Renders authenticated intranet dashboard."""
    return HTMLResponse(get_dashboard_html())


@app.get("/admin", response_class=HTMLResponse)
async def admin_portal():
    """Renders fake administrative SQL Query console."""
    return HTMLResponse(get_admin_sql_html())


# -------------------------------------------------------------------------
# Fake REST API Endpoints (Entices Automated Scanners & Attackers)
# -------------------------------------------------------------------------

@app.get("/api/v1/users")
async def api_get_users(request: Request, limit: int = 50):
    """Returns fake corporate users from SQLite DB."""
    client_ip = get_client_ip(request)
    users = get_all_users(limit=limit, source_ip=client_ip, user_agent=request.headers.get("user-agent", "unknown"))
    return JSONResponse({
        "status": "success",
        "count": len(users),
        "data": users
    })


@app.get("/api/v1/finance/records")
async def api_get_finance(request: Request, limit: int = 50):
    """Returns fake high-value financial records from SQLite DB."""
    client_ip = get_client_ip(request)
    records = get_all_finance_records(limit=limit, source_ip=client_ip, user_agent=request.headers.get("user-agent", "unknown"))
    return JSONResponse({
        "status": "success",
        "ledger": "Apex Financial Core Q3/Q4 Settlement Ledger",
        "total_records": len(records),
        "data": records
    })


@app.get("/api/v1/servers")
async def api_get_servers(request: Request, limit: int = 50):
    """Returns fake server infrastructure inventory from SQLite DB."""
    client_ip = get_client_ip(request)
    servers = get_all_server_inventory(limit=limit, source_ip=client_ip, user_agent=request.headers.get("user-agent", "unknown"))
    return JSONResponse({
        "status": "success",
        "network_zone": "VLAN-100-PROD-DMZ",
        "total_hosts": len(servers),
        "data": servers
    })


@app.get("/api/v1/credentials")
async def api_get_credentials(request: Request, limit: int = 50):
    """Returns fake credentials vault entries."""
    client_ip = get_client_ip(request)
    creds = get_all_credentials(limit=limit, source_ip=client_ip, user_agent=request.headers.get("user-agent", "unknown"))
    return JSONResponse({
        "status": "success",
        "vault": "Apex Secrets Management Vault",
        "total_secrets": len(creds),
        "data": creds
    })


@app.post("/api/v1/query")
async def api_execute_query(request: Request):
    """
    Executes attacker SQL queries against the fake corporate database.
    Captures SQL Injection probes and arbitrary SQL queries.
    """
    client_ip = get_client_ip(request)
    try:
        body = await request.json()
        sql_query = body.get("query", "").strip()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload. Expecting {'query': '...'}")

    if not sql_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    success, rows, message = execute_custom_sql(
        sql_query=sql_query,
        source_ip=client_ip,
        user_agent=request.headers.get("user-agent", "unknown")
    )

    forward_deception_event(
        source_ip=client_ip,
        action="DATABASE_QUERY_EXECUTION",
        path="/api/v1/query",
        method="POST",
        status_code=200 if success else 400,
        user_agent=request.headers.get("user-agent"),
        extra_details={
            "sql_query": sql_query,
            "rows_returned": len(rows),
            "query_success": success
        }
    )

    return JSONResponse({
        "success": success,
        "message": message,
        "rows": rows
    })


# -------------------------------------------------------------------------
# Honey Documents & Decoy File Downloads
# -------------------------------------------------------------------------

@app.get("/documents")
@app.get("/api/v1/documents")
async def list_honey_documents():
    """Lists decoy downloadable documents."""
    docs_path = Path(DECEPTION_DOCS_DIR)
    files = []
    if docs_path.exists():
        for f in docs_path.iterdir():
            if f.is_file():
                files.append({
                    "filename": f.name,
                    "size_bytes": f.stat().st_size,
                    "download_url": f"/documents/{f.name}"
                })
    return JSONResponse({
        "status": "success",
        "document_repository": "Confidential Executive Fileshare",
        "documents": files
    })


@app.get("/documents/{filename}")
@app.get("/api/v1/documents/{filename}")
async def download_honey_document(filename: str, request: Request):
    """Serves decoy documents and honey tokens."""
    client_ip = get_client_ip(request)
    safe_name = os.path.basename(filename)
    file_path = os.path.join(DECEPTION_DOCS_DIR, safe_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Requested confidential document not found")

    forward_deception_event(
        source_ip=client_ip,
        action="HONEY_DOCUMENT_EXFILTRATION",
        path=f"/documents/{safe_name}",
        method="GET",
        status_code=200,
        user_agent=request.headers.get("user-agent"),
        extra_details={
            "downloaded_file": safe_name,
            "file_size": os.path.getsize(file_path)
        }
    )

    return FileResponse(file_path, filename=safe_name)


@app.get("/credentials/{filename}")
async def download_honey_credential(filename: str, request: Request):
    """Serves decoy credentials files."""
    client_ip = get_client_ip(request)
    safe_name = os.path.basename(filename)
    file_path = os.path.join(DECEPTION_CREDS_DIR, safe_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Credential asset not found")

    forward_deception_event(
        source_ip=client_ip,
        action="HONEY_CREDENTIAL_THEFT",
        path=f"/credentials/{safe_name}",
        method="GET",
        status_code=200,
        user_agent=request.headers.get("user-agent"),
        extra_details={
            "stolen_credential_file": safe_name
        }
    )

    return FileResponse(file_path, filename=safe_name)


# -------------------------------------------------------------------------
# Deception Health, Audit & Reconnaissance Catch-All
# -------------------------------------------------------------------------

@app.get("/health")
@app.get("/status")
async def health_check():
    """Health check endpoint for deception container monitoring."""
    return JSONResponse({
        "status": "active",
        "service": "predator_deception_node",
        "decoy_db": "online",
        "port": DECEPTION_PORT,
        "mode": "armed"
    })


@app.get("/audit/logs")
async def get_audit(limit: int = 50):
    """Provides internal review of logged attacker events."""
    logs = get_recent_audit_logs(limit=limit)
    return JSONResponse({
        "total_audit_events": len(logs),
        "audit_trail": logs
    })


@app.api_route("/{catchall:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def catch_all_probe(request: Request, catchall: str):
    """
    Catches all scanner / reconnaissance / fuzzing attempts
    (e.g., /.env, /wp-admin, /phpmyadmin, /api/v2, /backup.zip, /actuator/env, etc.)
    Logs the attacker probe and triggers a DECEPTION_ACCESS alert.
    """
    client_ip = get_client_ip(request)
    method = request.method
    full_path = f"/{catchall}"

    forward_deception_event(
        source_ip=client_ip,
        action="RECONNAISSANCE_PROBE",
        path=full_path,
        method=method,
        status_code=404,
        user_agent=request.headers.get("user-agent"),
        extra_details={
            "fuzzed_path": full_path,
            "recon_type": "DIR_TRAVERSAL_OR_PROBE"
        }
    )

    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"Endpoint '{full_path}' is restricted or does not exist on this gateway.",
            "service": "Apex Intranet Gateway"
        }
    )


def run_server(host: Optional[str] = None, port: Optional[int] = None):
    """Launches the Uvicorn ASGI server."""
    import uvicorn
    h = host or DECEPTION_HOST
    p = port or DECEPTION_PORT
    print("\n=======================================================")
    print("[*] PREDATOR DECEPTION SERVER ONLINE")
    print(f"    Listening: http://{h}:{p}")
    print(f"    Forwarding Events To: {os.getenv('M3_BACKEND_URL', 'http://127.0.0.1:8000/events')}")
    print(f"    Fake Database: {DECEPTION_DB_PATH}")
    print("=======================================================\n")
    uvicorn.run(app, host=h, port=p, log_level="warning")


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else DECEPTION_PORT
    run_server(port=port_arg)
