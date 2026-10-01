# 15 — Kill Chain Execution Automation

**What to build:** Automate the entire attack simulator sequence so it runs perfectly for the final demo, chaining the stages together with appropriate delays.

**Blocked by:** 07 — Real OS Telemetry Collection, 09 — Attack Simulator Script

**Status:** ready-for-agent

- [ ] Write `demo_run.py` on System 2 that executes the sequence automatically:
  1. Failed logins (wait 5s).
  2. Dummy file ransomware changes (wait 5s).
  3. Deception server port scan.
- [ ] **Connectivity Check:** Running `python demo_run.py` automatically generates the telemetry that pushes M3's model through Normal -> Suspicious -> High -> Critical without any manual intervention.
