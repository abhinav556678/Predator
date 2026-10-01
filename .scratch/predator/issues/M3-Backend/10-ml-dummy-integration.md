# 10 — ML Dummy Integration & Stage Prediction Logic

**What to build:** Integrate the initial ML/Risk pipeline logic using a dummy model to prove out the prediction flow and Risk Score escalation before using real models.

**Blocked by:** 05 — Event Ingestion, DB & Behavior Engine

**Status:** ready-for-agent

- [ ] Create an `analyze_incident()` function that runs every time an incident updates.
- [ ] Implement stage logic: Map grouped telemetry to MITRE stages (e.g., Discovery, Credential Access).
- [ ] Implement a Risk Score calculator (e.g., jumps to CRITICAL if `DECEPTION_ACCESS` is present).
- [ ] Output the updated Incident payload with `predicted_stage` and `risk_score`.
- [ ] **Connectivity Check:** Send a `DECEPTION_ACCESS` event manually from M2 to M3; verify the incident risk updates to CRITICAL in the DB.
