# 06 — Dashboard Mock Integration

**What to build:** Connect the React UI to the M3 backend to fetch and display the incidents dynamically instead of using hardcoded frontend states.

**Blocked by:** 01 — Backend Setup & API Contracts, 03 — Frontend Skeleton & Setup

**Status:** ready-for-agent

- [ ] Write a data fetching service (e.g., using `axios` or `fetch`) to call `http://<M3_IP>:8000/incidents`.
- [ ] Build the IncidentCard and Timeline components to iterate over the fetched JSON data.
- [ ] Display the data on the Dashboard.
- [ ] **Connectivity Check:** Dashboard loads on M1's laptop and successfully renders the JSON fetched over the network from M3's backend.
