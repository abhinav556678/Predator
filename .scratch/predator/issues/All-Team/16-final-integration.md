# 16 — Final Integration & Rehearsal

**What to build:** The final end-to-end dry run across all 4 laptops ensuring the entire architecture works as specified in the master document.

**Blocked by:** 11 — Network Hardening & Validation, 13 — ML Live Model Integration, 14 — UI Polish & Containment Actions, 15 — Kill Chain Execution Automation

**Status:** ready-for-agent

- [ ] Connect all 4 laptops to the presentation LAN/hotspot.
- [ ] Verify static IPs are correctly updated in M1 (Frontend), M2 (Agent), M4 (Deception).
- [ ] Run the full demo:
  - M1 shows clean dashboard.
  - M2 starts `demo_run.py`.
  - UI updates live through the stages.
  - Deception is hit, risk jumps to CRITICAL.
  - M1 clicks CONTAIN.
- [ ] **Connectivity Check:** The demo runs flawlessly end-to-end with zero errors in any terminal.
