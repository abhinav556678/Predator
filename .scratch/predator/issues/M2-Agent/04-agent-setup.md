# 04 — Agent Skeleton & Core Telemetry Loop

**What to build:** The Python agent running on the Attacker laptop (System 2). It needs a basic loop that gathers telemetry and pushes formatted JSON events to the M3 Backend.

**Blocked by:** 01 — Backend Setup & API Contracts

**Status:** ready-for-agent

- [ ] Create a Python script (`agent.py`) with a main loop.
- [ ] Define the JSON payload schema for events (timestamp, event_type, source_ip, details).
- [ ] Implement an HTTP POST request to send static/dummy telemetry to M3's `/events` endpoint every few seconds.
- [ ] **Connectivity Check:** Agent runs on M2's laptop, and M3's Backend terminal prints "Event Received: <telemetry data>".
