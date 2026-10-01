# 12 — Live Dashboard & WebSockets

**What to build:** Upgrade the React Dashboard to update in real-time when new incidents or risk changes occur on the backend, instead of requiring a manual page refresh.

**Blocked by:** 06 — Dashboard Mock Integration, 10 — ML Dummy Integration & Stage Prediction Logic

**Status:** ready-for-agent

- [ ] Implement WebSocket connection in React to M3's backend (or set up rapid polling if WS is too complex).
- [ ] Connect the "Risk Score" and "Prediction Panel" UI components to the live data stream.
- [ ] Ensure the Incident Timeline auto-scrolls or updates smoothly as new events arrive.
- [ ] **Connectivity Check:** With the dashboard open on M1, M2 manually fires a high-risk event to M3. M1's dashboard immediately flashes Critical without refreshing.
