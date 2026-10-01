# PREDATOR — Master Project Specification

## 1. Overview

PREDATOR is a local, behavior-driven cybersecurity defense platform for a simulated enterprise.

It continuously monitors endpoint, identity, network, and deception telemetry; detects suspicious behavior; understands attack progression; predicts the likely next attack stage; safely observes attackers through an isolated deception environment; and enables controlled containment.

### Core principle

**Protect the real system first. Observe suspicious behavior second. Deceive the attacker in an isolated environment third. Contain when risk becomes high. Preserve the evidence trail.**

PREDATOR is an additional security layer. It does not replace firewalls, authentication, access control, antivirus, or commercial EDR.

---

# 2. Scope

## Included

- Lightweight endpoint telemetry / prototype EDR agent
- Process and file monitoring
- Identity and authentication monitoring
- SSH monitoring
- Network behavior monitoring
- ML-based benign/suspicious detection
- Attack-stage classification
- Next-stage prediction
- Behavioral correlation
- Risk scoring
- Isolated deception
- Fake server, database, credentials, and documents
- Credential-theft behavior simulation
- Malware-behavior simulation
- SSH attack simulation
- Lateral-movement simulation
- Ransomware-like behavior simulation using dummy files
- Controlled containment
- Incident timeline and audit trail
- SOC-style dashboard
- Two-system physical lab
- Independent attack simulator
- Local ML inference
- Local storage

## Excluded

- LLMs
- OpenAI/Gemini or other external AI APIs
- Cloud AI
- Real credential theft
- Real ransomware
- Destructive malware
- Real company data or credentials
- Full commercial-grade EDR
- Full SIEM
- Full firewall replacement
- Full MITRE ATT&CK implementation
- Kubernetes/cloud deployment
- Mobile app

---

# 3. Target Market

PREDATOR operates in enterprise cybersecurity, especially:

- Endpoint Detection and Response (EDR)
- Extended Detection and Response (XDR)
- Behavioral threat detection
- Cyber deception
- Incident response
- Security operations / SOC

### Target users

- SOC analysts
- Security teams
- IT/security administrators
- Enterprises needing additional behavioral visibility and deception

---

# 4. Threat Model

Primary attack chain:

```text
Credential compromise
        ↓
Suspicious authentication / SSH
        ↓
Discovery
        ↓
Credential-access behavior
        ↓
Privilege escalation behavior
        ↓
Lateral movement
        ↓
Deception interaction
        ↓
Data-access / exfiltration-like behavior
        ↓
Ransomware-like impact behavior
        ↓
Containment
```

The attack simulator generates safe activity inside the isolated lab. It never deploys real ransomware or destructive malware.

---

# 5. Two-System Architecture

To ensure a smooth hackathon presentation, the architecture is consolidated into 2 physical systems.

```text
       SYSTEM 2 (Attacker)                          SYSTEM 1 (Defender)
       IP: <ATTACKER_IP>                            IP: <DEFENDER_IP>

┌──────────────────────────────┐          ┌─────────────────────────────────────────┐
│                              │          │                                         │
│                              │          │    [Port 3000] Frontend (Dashboard)     │
│                              │          │           ▲                             │
│    [Attacker Simulator]      │          │           │                             │
│                              │ POST     │    [Port 8000] Backend + ML + DB        │
│    Fires events to System 1  ├─────────►│           │                             │
│                              │          │           ▼                             │
│                              │          │    [Port 8080/9000] Deception Server    │
│                              │          │                                         │
└──────────────────────────────┘          └─────────────────────────────────────────┘
```

A private LAN or mobile hotspot is sufficient. Internet access is not required.

---

# 6. System Architecture

```text
                 ATTACK SIMULATOR
                        │
                 simulated activity
                        ↓
              SIMULATED COMPANY
              Employee / Server / DB
                        │
                 Security telemetry
                        ↓
                 PREDATOR AGENT
                        ↓
                FEATURE ENGINE
                        ↓
                 ML DETECTOR
                        ↓
                BEHAVIOR ENGINE
                        ↓
                STAGE PREDICTOR
                        ↓
                  RISK ENGINE
                        ↓
              ┌─────────┴─────────┐
              ↓                   ↓
         DECEPTION             DASHBOARD
              │                   │
              ↓                   ↓
       Fake environment       SOC analyst
              │                   │
              └────────┬──────────┘
                       ↓
                  CONTAINMENT
```

---

# 7. Endpoint Agent / Prototype EDR

The agent runs on the employee and server machines.

### Endpoint telemetry

- Process creation
- Parent/child process relationships
- File creation
- File modification
- File access rate
- File extension changes
- Entropy/content-change indicators
- Privilege changes
- Suspicious process behavior

### Identity telemetry

- Login attempts
- Failed logins
- Successful logins
- SSH authentication
- New source/device
- Privilege changes

### Network telemetry

- Connection attempts
- Connection frequency
- New destinations
- Internal scanning
- Unique destination count
- Bytes transferred
- Suspicious outbound activity

### Deception telemetry

- Fake server access
- Fake credential attempts
- Fake database queries
- Fake document access
- Suspicious interactions

---

# 8. ML Training

No LLM or external AI is required.

### Public training data

Use suitable public cybersecurity datasets such as:

- CIC-IDS2017
- UNSW-NB15

These provide examples of benign and malicious network behavior.

### Custom PREDATOR data

Generate labeled endpoint, identity, SSH, file, and deception telemetry inside the isolated lab.

The public data provides general network behavior; the custom lab data makes the model relevant to our architecture.

---

# 9. Features

### Network

- Connection count/rate
- Unique destinations
- Unique ports
- Bytes in/out
- Failed connections
- Internal scan count
- New destinations

### Identity

- Failed login count
- Successful login after failures
- New login source
- Login frequency
- Privilege changes

### Endpoint

- Process creation rate
- New/unusual process
- Parent-child relationship
- File access rate
- File modification rate
- Sensitive-directory access
- Browser/credential-directory access
- Privilege change

### Ransomware-like behavior

- Files modified
- Modification rate
- Extension changes
- Entropy/content changes
- Affected directories
- Single-process modification concentration

### Deception

- Decoy accessed
- Fake credential used
- Fake database queried
- Fake file accessed
- Decoy interaction count

---

# 10. ML Components

## Detection model

```text
Telemetry
   ↓
Feature extraction
   ↓
Random Forest / XGBoost
   ↓
BENIGN / SUSPICIOUS
```

## Attack-stage model

Possible stages:

```text
NORMAL
INITIAL ACCESS
DISCOVERY
CREDENTIAL ACCESS
PRIVILEGE ESCALATION
LATERAL MOVEMENT
COLLECTION
EXFILTRATION
IMPACT
```

## Next-stage predictor

Example:

```text
LOGIN
 ↓
DISCOVERY
 ↓
CREDENTIAL ACCESS

Predicted next:
LATERAL MOVEMENT

Confidence:
84%
```

The exact model can use engineered sequence features and a lightweight classifier.

---

# 11. Behavior Engine

The behavior engine correlates events instead of treating each event independently.

Example:

```text
SSH login
+
Discovery
+
Credential access
+
Privilege change
+
Internal scanning
```

produces much higher concern than one isolated SSH login.

A rolling activity window is maintained per endpoint/session.

---

# 12. Risk Engine

Risk combines:

```text
ML confidence
+
behavioral severity
+
attack-stage severity
+
event frequency
+
asset importance
+
deception evidence
```

Risk levels:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Major actions should not be triggered by one weak signal.

---

# 13. Deception Environment

```text
              LAB / PRODUCTION SIDE
                       │
                       X
                 SECURITY BOUNDARY
                       X
                       │
                       ▼
                DECEPTION NETWORK

              ┌───────────────────┐
              │ Fake Server       │
              │ Fake Database     │
              │ Fake Credentials  │
              │ Fake Documents    │
              └───────────────────┘
```

### Security requirements

- No real credentials
- No real secrets
- No real company data
- Restricted outbound access
- No unrestricted route into production
- Only required services exposed
- All interactions logged

The deception environment is treated as potentially compromised.

---

# 14. Attack Simulators

The attack simulator is separate from PREDATOR.

PREDATOR receives telemetry, not an explicit attack label.

## Credential-theft simulation

Use synthetic browser-like credential data and generate:

- suspicious process
- credential-directory access
- synthetic credential access
- suspicious outbound behavior

## Malware-behavior simulation

A benign program generates:

- child process creation
- unusual file access
- persistence-like lab artifacts
- repeated network connections
- synthetic credential access

It does not damage the host.

## SSH attack simulation

Inside the lab:

```text
Failed authentication
↓
Repeated attempts
↓
Successful simulated access
↓
Discovery
↓
Privilege-related behavior
```

## Lateral movement simulation

The simulator makes controlled connections between lab machines.

Production systems are never targeted.

## Ransomware simulation

Use only dummy files:

```text
PREDATOR_LAB/
└── ImportantFiles/
    ├── invoice001.txt
    ├── invoice002.txt
    ├── report001.docx
    └── ...
```

Generate:

- rapid file access
- rapid modification
- extension changes
- controlled content transformation
- synthetic entropy changes

PREDATOR detects the resulting behavior.

---

# 15. Main Demonstration

The complete scenario:

```text
Synthetic credential compromise
        ↓
Suspicious employee login
        ↓
SSH/authentication behavior
        ↓
Discovery
        ↓
Credential-access behavior
        ↓
Privilege behavior
        ↓
Lateral movement
        ↓
PREDATOR detects progression
        ↓
PREDATOR predicts next stage
        ↓
Deception activated
        ↓
Fake server interaction
        ↓
Additional evidence
        ↓
Ransomware-like activity on dummy files
        ↓
CRITICAL risk
        ↓
Containment
        ↓
Complete incident preserved
```

---

# 16. Security of PREDATOR

PREDATOR must never intentionally weaken the real environment.

### Existing controls remain active

- Firewall
- Authentication
- Access controls
- Existing EDR/antivirus
- Network segmentation
- Least privilege

### Controlled observation

Safe suspicious activity can be observed. Dangerous activity is blocked, restricted, or redirected to deception.

### Isolated deception

The attacker cannot use the decoy as a bridge into production.

### Synthetic data

No real secrets are placed in the deception environment.

### Controlled containment

High-risk events produce a containment recommendation. The hackathon can use analyst-approved containment.

### Audit trail

Events, predictions, deception actions, risk changes, and response actions are recorded.

---

# 17. Dashboard

A single SOC dashboard is sufficient.

```text
PREDATOR
────────────────────────────────────────
Endpoints: 3
Active Incidents: 1
High Risk: 1
Active Decoys: 1
System: PROTECTED

LIVE ATTACK TIMELINE

08:42  Suspicious Login
08:43  SSH Activity
08:43  Discovery
08:44  Credential Access
08:44  Lateral Movement Predicted
08:45  Decoy Activated
08:45  Decoy Access Detected
08:46  Ransomware-like Activity
08:46  Critical Risk
08:46  Endpoint Contained

CURRENT ASSESSMENT

Current Stage:
Credential Access

Predicted Next:
Lateral Movement

Confidence:
84%

DECEPTION
Finance Decoy: ACTIVE
Interaction: DETECTED
Fake DB: QUERIED

RESPONSE
Endpoint: EMPLOYEE-03
Risk: CRITICAL
[ CONTAIN ]
```

---

# 18. Repository Architecture

```text
PREDATOR/
│
├── README.md
├── master.md
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── api/
│   │   ├── events.py
│   │   ├── incidents.py
│   │   ├── predictions.py
│   │   ├── deception.py
│   │   └── response.py
│   ├── detection/
│   │   ├── detector.py
│   │   ├── feature_engineering.py
│   │   └── preprocessing.py
│   ├── behavior/
│   │   ├── behavior_engine.py
│   │   ├── attack_stage.py
│   │   └── sequence.py
│   ├── prediction/
│   │   ├── stage_predictor.py
│   │   └── model_loader.py
│   ├── risk/
│   │   └── risk_engine.py
│   ├── deception/
│   │   ├── deception_manager.py
│   │   └── interaction_logger.py
│   └── response/
│       ├── response_engine.py
│       └── containment.py
│
├── agent/
│   ├── agent.py
│   ├── collectors/
│   │   ├── process.py
│   │   ├── files.py
│   │   ├── network.py
│   │   ├── authentication.py
│   │   └── ssh.py
│   ├── feature_buffer.py
│   └── sender.py
│
├── ml/
│   ├── datasets/
│   │   ├── public/
│   │   └── custom/
│   ├── preprocessing/
│   │   └── prepare_dataset.py
│   ├── training/
│   │   ├── train_detector.py
│   │   └── train_predictor.py
│   ├── evaluation/
│   │   └── evaluate.py
│   └── models/
│       ├── detector.pkl
│       └── predictor.pkl
│
├── simulator/
│   ├── attacker.py
│   ├── scenarios/
│   │   ├── credential_theft.py
│   │   ├── malware_behavior.py
│   │   ├── ssh_attack.py
│   │   ├── lateral_movement.py
│   │   └── ransomware_simulation.py
│   └── dummy_data/
│       ├── credentials/
│       └── important_files/
│
├── deception/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── network_config/
│   ├── fake_server/
│   ├── fake_database/
│   ├── fake_credentials/
│   └── fake_documents/
│
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── components/
│   │   │   ├── SystemStatus.jsx
│   │   │   ├── IncidentCard.jsx
│   │   │   ├── AttackTimeline.jsx
│   │   │   ├── PredictionPanel.jsx
│   │   │   ├── DeceptionPanel.jsx
│   │   │   └── ResponsePanel.jsx
│   │   └── pages/
│   │       └── Dashboard.jsx
│   └── public/
│
├── database/
│   └── schema.sql
│
├── docs/
│   ├── architecture.md
│   ├── threat_model.md
│   ├── attack_scenarios.md
│   ├── ml_pipeline.md
│   └── security.md
│
└── tests/
    ├── test_detection.py
    ├── test_prediction.py
    ├── test_deception.py
    └── test_response.py
```

---

# 19. Runtime Distribution

### System 1 — The Defender (Core)

```text
React Dashboard (Port 3000)
Backend API (Port 8000)
ML Models
SQLite Database
Deception Fake Server (Port 8080/9000)
```

### System 2 — The Attacker (Endpoint)

```text
PREDATOR Agent (forwarding simulated events)
Attack Simulator (triggering logins, network scans)
```

---

# 20. Data Flow

```text
Endpoint / Server
       ↓
Telemetry Agent
       ↓
Event Collection
       ↓
Feature Extraction
       ↓
ML Detection
       ↓
Behavior Correlation
       ↓
Attack Stage
       ↓
Next Stage Prediction
       ↓
Risk Score
       ↓
┌──────┴──────────┐
│                 │
Normal         Suspicious
│                 │
Continue       Deception
                  │
                  ↓
            Attacker Interaction
                  │
                  ↓
             More Evidence
                  │
                  ↓
              High Risk
                  │
                  ↓
             Containment
                  │
                  ↓
            Incident Record
```

---

# 21. Team Roles & Responsibilities (4 Members)

To complete this in 4-5 hours, all members must work strictly in parallel. The APIs act as contracts so nobody is blocked waiting for someone else's code.

### Member 1: Frontend & Dashboard Lead (System 1 UI)
- **Role**: Build the React UI (Dashboard, Incident Timeline, Prediction Panel, System Status).
- **Workflow Rule**: Mock all API responses first. Do not wait for Member 3's backend to be ready. Just render JSON files. Connect to live API in the final hour.

### Member 2: Agent & Attacker Simulator (System 2)
- **Role**: Build the Python Telemetry Agent (gathering dummy file access, process logs, network hits) and the Attack Simulator scripts (simulating login failures, port scanning).
- **Workflow Rule**: Hardcode the agent to send POST requests to `http://SYSTEM_1_IP:8000/events`. Just print the output if the backend isn't up.

### Member 3: Core Backend & ML Pipeline (System 1 Backend)
- **Role**: Build the FastAPI backend, SQLite database, Event ingestion API, and the ML logic (Detection, Behavior, Prediction, Risk scoring).
- **Workflow Rule**: Provide a dummy dataset instantly to unblock yourself. Build the API routes (`/events`, `/incidents`) so Member 1 and Member 2 have an endpoint to test against.

### Member 4: Deception Environment & Infrastructure (System 1 Deception)
- **Role**: Build the Deception environment (fake SQLite DB, fake credential files via simple Docker/Python server), log any interaction, and handle networking.
- **Workflow Rule**: Send a webhook/event to the backend whenever the fake server is hit. Ensure firewalls are off for the local network.

---

# 22. 4-5 Hour Parallel Execution Plan

### Hour 1: Setup & API Contracts
- **All Members**: Agree on static IPs (e.g., System 1: `192.168.1.10`). Clone repo.
- **Member 1 (Frontend)**: Init React app. Mock API JSON data. Build basic layout.
- **Member 2 (Agent)**: Write skeleton Python agent to monitor local directory files.
- **Member 3 (Backend)**: Init FastAPI and SQLite. Build `/events` POST endpoint. 
- **Member 4 (Deception)**: Setup Docker on System 1. Spin up a basic fake HTTP server.

### Hour 2: Core Logic & Telemetry
- **Member 1 (Frontend)**: Build Timeline component and live Risk Score UI using mocked data.
- **Member 2 (Agent)**: Implement actual OS telemetry (psutil for processes, basic socket monitoring). Send events to Backend.
- **Member 3 (Backend)**: Create a simple ML dummy model (returns BENIGN/SUSPICIOUS randomly) to unblock the pipeline. Write the Behavior Engine (rolling window).
- **Member 4 (Deception)**: Add fake database tables. Write script that logs whenever a port is touched and sends a "DECEPTION_ACCESS" event to the Backend.

### Hour 3: The Intelligence Layer & Simulation
- **Member 1 (Frontend)**: Implement WebSocket or polling for live dashboard updates.
- **Member 2 (Agent)**: Build the Attack Simulator (Python script that intentionally fails logins, accesses lots of dummy files, and connects to System 1).
- **Member 3 (Backend)**: Implement the actual ML model (scikit-learn Random Forest) using a tiny pre-cleaned dataset or synthetic data. Build Stage Prediction logic.
- **Member 4 (Deception)**: Start helping Member 2 with cross-system networking. Ensure Attacker (System 2) can reach Deception (System 1).

### Hour 4: Integration & "The Kill Chain"
- **All Members**: Connect everything.
- **Member 2** runs the Simulator.
- **Member 3** ensures Backend correctly flags it, scores the risk, and saves to DB.
- **Member 1** removes mock data and connects React to the real FastAPI backend. Watches incidents appear live.
- **Member 4** verifies that when the Simulator touches System 1 Deception, the risk jumps to CRITICAL.

### Hour 5: Polish & Demo Rehearsal
- **All Members**: Fix bugs, UI glitches, and model inaccuracies.
- Rehearse the "Demo Flow":
  1. Show Dashboard (Clean).
  2. Run Simulator on System 2.
  3. Show Dashboard (Timeline updates, prediction triggers).
  4. Simulator hits System 1 (Deception).
  5. Dashboard shows CRITICAL -> Containment.

---

# 23. Final Project Statement

> **PREDATOR is a local, behavior-driven cybersecurity defense platform that monitors enterprise endpoints, identities, and network activity, detects attack behavior, predicts attack progression, safely engages suspicious activity through isolated deception, and enables controlled containment while preserving the complete incident trail.**

The key security statement is:

> **PREDATOR does not allow an attacker to freely spread through the real company network. Existing security controls remain active; suspicious behavior is observed at controlled boundaries, and isolated deception provides a safe environment for collecting additional attacker evidence.**

---

# 24. Technology Stack

| Component | Technology |
|---|---|
| Dashboard | React + Tailwind |
| Backend | Python |
| Local backend interface | FastAPI |
| ML | scikit-learn / XGBoost |
| Data processing | Pandas |
| Database | SQLite |
| Agent | Python |
| Deception | Docker |
| Lab networking | Docker + private LAN |
| Authentication | Local JWT |
| Live dashboard | WebSocket |
| Deployment | Docker Compose |

**No LLM. No external AI API. No cloud AI. No external telemetry processing.**
