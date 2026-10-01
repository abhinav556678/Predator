# 14 — UI Polish & Containment Actions

**What to build:** Final visual polish for the dashboard, adding critical alert states and the interactive "Contain" action button for the demo.

**Blocked by:** 12 — Live Dashboard & WebSockets

**Status:** ready-for-agent

- [ ] Add visual flair: Red flashing borders or banners when Risk Score hits CRITICAL.
- [ ] Add a "CONTAIN" button on the Incident card that sends a POST request back to M3's `/response` endpoint.
- [ ] Implement a "System Contained" success state in the UI.
- [ ] **Connectivity Check:** When Risk is Critical, clicking "CONTAIN" on M1's laptop sends a successful request to M3's Backend and updates the UI to show the threat is neutralized.
