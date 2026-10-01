# Deception Network Hardening & Isolation Policy
**Ticket 11: Network Hardening & Validation**

## 1. Isolation Architecture

The Deception honeypot operates inside a strictly isolated Docker container or unprivileged process on System 1:

```text
       SYSTEM 2 (Attacker)
               │
               ▼  Allowed Ports Only (8080 / 9000)
    ┌──────────────────────────────────────────────┐
    │  System 1 Host Firewall                      │
    │  (Blocks 21, 22, 445, 3306, 5432, etc.)      │
    └──────────────────┬───────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │ Docker Container (Isolated)  │
        │ - User: UID 10001 (Non-root) │
        │ - No new privileges          │
        │ - Isolated bridge network    │
        │ - Dummy SQLite DB ONLY       │
        └──────────────┬───────────────┘
                       │
       X───────────────┴───────────────X
       BLOCKED: Host OS Filesystem & Prod DB
```

## 2. Security Controls Enforced

1. **Non-Root Execution**: Container runs strictly under `deception_user` (`UID 10001`). No privilege escalation (`no-new-privileges:true`).
2. **Network Isolation**: The container is placed on `predator_deception_net` with inter-container communication (`enable_icc`) set to `false`. Outbound routing to local host production interfaces is restricted.
3. **Storage Isolation**: The container only mounts its own dedicated volumes (`deception_data` and `deception_logs`). The host OS filesystem (`C:\`, `/etc`, `/root`, `/home`) is never mapped.
4. **Data Isolation**: The honeypot operates entirely on synthetic data (`fake_corporate.db`), synthetic honeytokens, and decoy files. No real secrets, passwords, or company credentials ever exist in the deception environment.
5. **Event-Driven Boundary**: The only permitted outbound communication from the deception node is the HTTP webhook to `http://<M3_IP>:8000/events` to report `DECEPTION_ACCESS`.

## 3. Verification Steps

1. **Port Whitelist Check**:
   - Verify only ports `3000`, `8000`, `8080`, and `9000` respond to TCP probes.
   - Any probes to port 22, 445, 3306, or 5432 must be rejected or dropped.

2. **Deception Responsiveness**:
   - `curl http://<M4_IP>:8080` must return the fake Corporate Intranet Portal.

3. **Event Generation**:
   - Querying any endpoint on `:8080` immediately produces a `DECEPTION_ACCESS` record.
