# 07 — Real OS Telemetry Collection

**What to build:** Upgrade the Python agent to pull actual OS metrics (processes, network, file changes) rather than sending dummy strings.

**Blocked by:** 04 — Agent Skeleton & Core Telemetry Loop

**Status:** ready-for-agent

- [ ] Integrate `psutil` to monitor process creations and network connections.
- [ ] Implement a basic directory watcher (e.g., using `watchdog`) to monitor a "dummy sensitive files" folder for file modifications.
- [ ] Format these real metrics into the JSON payload and send them to M3.
- [ ] **Connectivity Check:** Run the agent on M2, create a file in the watched folder, and verify M3 receives a file modification event.
