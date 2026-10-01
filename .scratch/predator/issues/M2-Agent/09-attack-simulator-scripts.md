# 09 — Attack Simulator Script

**What to build:** A separate Python script on System 2 that simulates an attacker executing a kill chain (failed logins, scanning, ransomware dummy file changes).

**Blocked by:** 04 — Agent Skeleton & Core Telemetry Loop

**Status:** ready-for-agent

- [ ] Create `simulator.py`.
- [ ] Write a function to simulate multiple failed SSH/login attempts.
- [ ] Write a function to rapidly modify files in the watched dummy folder (simulating ransomware).
- [ ] Write a function to run a port scan targeting M4's deception server.
- [ ] **Connectivity Check:** Run the simulator on M2. The M2 Agent should pick up the file changes/logins and send them to M3, while the port scan directly hits M4's Deception server.
