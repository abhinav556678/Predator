# 13 — ML Live Model Integration

**What to build:** Swap out the dummy heuristic model in the backend with the actual scikit-learn Random Forest model trained on the dataset.

**Blocked by:** 10 — ML Dummy Integration & Stage Prediction Logic

**Status:** ready-for-agent

- [ ] Load the trained `detector.pkl` into the FastAPI backend on startup.
- [ ] Map the incoming JSON telemetry into the feature vector required by the model.
- [ ] Update the `analyze_incident()` loop to pass data through the real model for classification (BENIGN / SUSPICIOUS).
- [ ] **Connectivity Check:** M2 sends a known "Suspicious" payload from the simulator. The M3 Backend logs the scikit-learn model's confidence score and marks it appropriately.
