# 05 — Event Ingestion, DB & Behavior Engine

**What to build:** The backend logic to save incoming events to SQLite, group them into incidents using a rolling window, and apply a dummy heuristic to flag suspicious events.

**Blocked by:** 01 — Backend Setup & API Contracts, 04 — Agent Skeleton & Core Telemetry Loop

**Status:** ready-for-agent

- [ ] Update `/events` endpoint to write the incoming JSON to the SQLite `Events` table.
- [ ] Implement a rolling window grouping function (e.g., group events by `source_ip` within a 5-minute window).
- [ ] Write a basic heuristic (e.g., if >5 events in 1 minute, flag as SUSPICIOUS and create an Incident).
- [ ] Update `/incidents` endpoint to read from the actual SQLite DB instead of returning mock data.
- [ ] **Connectivity Check:** M2 sends multiple real events via the Agent; M1's GET request to `/incidents` returns them properly grouped.
