# Transaction System Attack Lab

This lab models a simplified multi-service transaction platform to demonstrate how subtle design and
implementation issues can lead to:

- **Broken access control / IDOR** on account resources
- **Unauthorized transfers** based on weak authorization checks
- **Logging and detection gaps** that make investigations harder

The goal is to show **end-to-end attack paths** across multiple services, not just individual bugs.
It is intentionally vulnerable and designed for **educational** use only.

> Only use this lab on systems you own or have explicit permission to test.

---

## Components

The platform is made up of three small services:

- `auth-service` – handles login and issues tokens containing user identity and roles
- `accounts-service` – exposes account and transfer APIs, and contains deliberate access-control flaws
- `audit-service` – receives structured security/audit events (and intentionally misses some of them)

See `docs/architecture.md` for the high-level architecture and trust boundaries.

---

## Quickstart

Prerequisites:

- Python 3.11+
- Docker & Docker Compose (optional but recommended)

> NOTE: The initial version focuses on structure and documentation. Service implementations will be
> iterated on over time, along with additional attack paths and detection content.

Clone and explore the lab:

```bash
git clone https://github.com/c0ncatenate/transaction-system-attack-lab.git
cd transaction-system-attack-lab
```

(Placeholder) To run all services locally with Docker:

```bash
# TODO: add docker-compose.yml
./scripts/run_lab.sh
```

---

## Learning Objectives

This lab is designed to help practise:

- Reasoning about **trust boundaries** between services
- Finding and exploiting **broken access control / IDOR** on account-like resources
- Chaining **auth design issues** into unauthorized actions (e.g., transfers)
- Identifying **logging and detection gaps** that make attacks hard to spot

The scenarios are inspired by patterns seen in modern transaction and financial-style platforms,
without modelling any specific real-world system.

---

## Visual overview

![Finding IDOR in a transaction system](diagrams/idor-flow.png)

## Documentation

Detailed docs live under `docs/`:

- `docs/overview.md` – high-level overview of the lab and its goals
- `docs/architecture.md` – components, data flows, and trust boundaries
- `docs/threat-model.md` – threat-modelling notes for the system
- `docs/attack-path-01-idor-broken-access-control.md` – first attack path walkthrough
- `docs/detection-and-mitigation.md` – logging, detection, and hardening ideas
- `docs/roadmap.md` – future attack paths and improvements

---

## Status

This repository is under active construction. Initial focus:

- [x] Scaffold repo structure and documentation
- [ ] Implement minimal `auth-service`, `accounts-service`, and `audit-service`
- [ ] Implement attack path 01 (IDOR / broken access control on accounts)
- [ ] Add basic tests and a CI workflow
- [ ] Add further attack paths (webhook verification issues, race conditions on transfers, etc.)

Contributions, feedback, and ideas for additional scenarios are welcome.
