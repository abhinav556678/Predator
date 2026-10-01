"""
PREDATOR Deception Subsystem - Configuration
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DECEPTION_DIR = BASE_DIR
PROJECT_ROOT = BASE_DIR.parent

# Server Network Configuration
DECEPTION_HOST = os.getenv("DECEPTION_HOST", "0.0.0.0")
DECEPTION_PORT = int(os.getenv("DECEPTION_PORT", "8080"))
DECEPTION_SECONDARY_PORT = int(os.getenv("DECEPTION_SECONDARY_PORT", "9000"))

# Central M3 Backend Configuration
# In System 1, backend is on port 8000; when deployed cross-system, point to M3 IP
M3_BACKEND_IP = os.getenv("M3_IP", os.getenv("DEFENDER_IP", "127.0.0.1"))
M3_BACKEND_PORT = int(os.getenv("M3_PORT", "8000"))
M3_BACKEND_URL = os.getenv("M3_BACKEND_URL", f"http://{M3_BACKEND_IP}:{M3_BACKEND_PORT}/events")
ENABLE_WEBHOOK = os.getenv("ENABLE_WEBHOOK", "true").lower() in ("true", "1", "yes")

# Database & Decoy Asset Paths
DECEPTION_DB_PATH = os.getenv(
    "DECEPTION_DB_PATH",
    str(DECEPTION_DIR / "fake_database" / "fake_corporate.db")
)
DECEPTION_DOCS_DIR = os.getenv(
    "DECEPTION_DOCS_DIR",
    str(DECEPTION_DIR / "fake_documents")
)
DECEPTION_CREDS_DIR = os.getenv(
    "DECEPTION_CREDS_DIR",
    str(DECEPTION_DIR / "fake_credentials")
)
LOGS_DIR = os.getenv("DECEPTION_LOGS_DIR", str(DECEPTION_DIR / "logs"))
LOG_FILE_PATH = os.path.join(LOGS_DIR, "deception_access.log")

# Ensure required directories exist
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DECEPTION_DB_PATH), exist_ok=True)
os.makedirs(DECEPTION_DOCS_DIR, exist_ok=True)
os.makedirs(DECEPTION_CREDS_DIR, exist_ok=True)
