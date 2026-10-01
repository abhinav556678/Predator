# 08 — Deception Logging & Event Forwarding

**What to build:** The deception server must log any interaction (HTTP requests, DB queries) and immediately forward a `DECEPTION_ACCESS` event to the central M3 Backend.

**Blocked by:** 02 — Deception Environment Setup

**Status:** completed

- [x] Add logging to every route in the fake HTTP server and every query in the fake DB.
- [x] Write a webhook function in the fake server that sends a POST request with `event_type="DECEPTION_ACCESS"` to `http://<M3_IP>:8000/events` whenever touched.
- [x] **Connectivity Check:** M2 `curl`s the Deception server, which in turn causes the M3 Backend to immediately log a `DECEPTION_ACCESS` event.
