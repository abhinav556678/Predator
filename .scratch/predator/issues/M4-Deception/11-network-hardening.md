# 11 — Network Hardening & Validation

**What to build:** Ensure that the deception environment is properly isolated on System 1 and that the networking works exactly as specified in the threat model.

**Blocked by:** 08 — Deception Logging & Event Forwarding, 01 — Backend Setup & API Contracts

**Status:** completed

- [x] Ensure System 1 (Defender) firewall is configured to only allow the specific ports needed (3000 for UI, 8000 for Backend, 8080/9000 for Deception).
- [x] Verify that Docker container networks do not allow unrestricted routing into System 1's actual host OS files or production database.
- [x] **Connectivity Check:** M2 attempts to ping System 1 ports that are *not* whitelisted and ensures they are blocked. M2 verifies it can still hit the Deception port.
