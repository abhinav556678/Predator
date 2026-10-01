# 02 — Deception Environment Setup

**What to build:** The fake environment on System 1. A Dockerized fake HTTP server (acting as an internal company portal) and a fake DB. Firewalls must be configured to allow LAN access from System 2.

**Blocked by:** None — can start immediately

**Status:** completed

- [x] Create a simple Python HTTP server or use Nginx in a Docker container.
- [x] Create a fake SQLite DB with dummy tables (`users`, `finance_records`).
- [x] Ensure the Docker container exposes ports (e.g., 8080 or 9000) to the host.
- [x] **Connectivity Check:** M2 can `curl http://<M4_IP>:8080` from the Attacker laptop and receive the fake deception response (e.g., a dummy login page).
