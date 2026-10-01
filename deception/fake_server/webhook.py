"""
PREDATOR Deception Subsystem - Event Forwarding & Webhook Dispatcher
Ticket 08: Deception Logging & Event Forwarding
Sends HTTP POST with event_type="DECEPTION_ACCESS" to http://<M3_IP>:8000/events
"""

import datetime
import json
import logging
import threading
from typing import Dict, Any, Optional
import requests
from deception.fake_server.config import (
    M3_BACKEND_URL,
    ENABLE_WEBHOOK,
    LOG_FILE_PATH
)

# Logger setup
logger = logging.getLogger("PREDATOR_DECEPTION")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] [DECEPTION] [%(levelname)s] %(message)s", "%H:%M:%S")
console_handler.setFormatter(console_formatter)
if not logger.handlers:
    logger.addHandler(console_handler)

# File handler
try:
    file_handler = logging.FileHandler(LOG_FILE_PATH, mode="a", encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
except Exception as e:
    print(f"[Warning] Could not attach file logger: {e}")


def format_deception_event(
    source_ip: str,
    action: str,
    path: str,
    method: str = "GET",
    status_code: int = 200,
    user_agent: Optional[str] = "unknown",
    extra_details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Constructs the standard PREDATOR telemetry payload for DECEPTION_ACCESS events.
    Matches Member 3 (Backend) and Member 2 (Agent) schema:
    {
      "timestamp": "<ISO 8601>",
      "event_type": "DECEPTION_ACCESS",
      "source_ip": "<ATTACKER_IP>",
      "details": { ... }
    }
    """
    details = {
        "service": "deception_honeypot",
        "sub_type": "HONEYPOT_INTERACTION",
        "action": action,
        "method": method,
        "path": path,
        "status_code": status_code,
        "user_agent": user_agent or "unknown",
        "severity": "CRITICAL",
        "description": f"Attacker interacted with deception asset: [{method}] {path} ({action})"
    }
    if extra_details:
        details.update(extra_details)

    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "event_type": "DECEPTION_ACCESS",
        "source_ip": source_ip,
        "details": details
    }


def _dispatch_post(payload: Dict[str, Any], target_url: str):
    """Worker function executed in background thread to forward event to M3."""
    try:
        response = requests.post(
            target_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=2.5
        )
        if response.status_code in (200, 201, 202):
            logger.info(
                f"[Webhook SUCCESS] Forwarded DECEPTION_ACCESS event to {target_url} (HTTP {response.status_code})"
            )
        else:
            logger.warning(
                f"[Webhook RESPONSE] M3 Backend returned HTTP {response.status_code}: {response.text[:120]}"
            )
    except requests.exceptions.ConnectionError:
        logger.warning(
            f"[Webhook NOTICE] M3 Backend at {target_url} is unreachable (M3 may still be initializing)."
        )
    except requests.exceptions.Timeout:
        logger.warning(
            f"[Webhook TIMEOUT] Request to M3 Backend at {target_url} timed out."
        )
    except Exception as exc:
        logger.error(f"[Webhook ERROR] Failed to dispatch event to {target_url}: {exc}")


def forward_deception_event(
    source_ip: str,
    action: str,
    path: str,
    method: str = "GET",
    status_code: int = 200,
    user_agent: Optional[str] = "unknown",
    extra_details: Optional[Dict[str, Any]] = None,
    sync: bool = False
) -> Dict[str, Any]:
    """
    Logs the deception access and dispatches a DECEPTION_ACCESS webhook to M3 Backend.
    """
    payload = format_deception_event(
        source_ip=source_ip,
        action=action,
        path=path,
        method=method,
        status_code=status_code,
        user_agent=user_agent,
        extra_details=extra_details
    )

    # 1. Log to local audit log
    log_line = f"ALERT [DECEPTION_ACCESS] From {source_ip} | {method} {path} | Action: {action} | Details: {json.dumps(extra_details or {})}"
    logger.info(log_line)

    # 2. Dispatch to M3 Backend
    if ENABLE_WEBHOOK:
        if sync:
            _dispatch_post(payload, M3_BACKEND_URL)
        else:
            thread = threading.Thread(
                target=_dispatch_post,
                args=(payload, M3_BACKEND_URL),
                daemon=True
            )
            thread.start()

    return payload
