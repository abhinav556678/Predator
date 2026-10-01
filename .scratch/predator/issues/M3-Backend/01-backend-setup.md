# 01 — Backend Setup & API Contracts

**What to build:** The core hub. A FastAPI server running on System 1 with an initialized SQLite database. It must expose `/events` (POST) and `/incidents` (GET) endpoints that return static mock JSON so the rest of the team can start integrating immediately.

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

- [ ] Initialize FastAPI project with `uvicorn`.
- [ ] Setup basic SQLite database with tables for `Events` and `Incidents`.
- [ ] Create `POST /events` endpoint that accepts JSON telemetry (prints to console, returns 200 OK).
- [ ] Create `GET /incidents` endpoint that returns a hardcoded mock JSON array of incidents.
- [ ] **Connectivity Check:** M1, M2, and M4 can `curl http://<M3_IP>:8000/events` from their respective laptops on the LAN and receive a 200 OK.
