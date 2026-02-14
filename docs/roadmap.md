# Roadmap

This lab is intended to evolve over time with additional scenarios and hardening guidance.

## Completed

- [x] Create repository structure and initial documentation
- [x] Define high-level architecture and threat model
- [x] Document Attack Path 01 (IDOR / broken access control on accounts)

## In Progress

- [ ] Implement minimal `auth-service`, `accounts-service`, and `audit-service`
- [ ] Implement exploit scripts for Attack Path 01
- [ ] Add basic tests and CI workflow

## Planned Attack Paths

- [ ] **Attack Path 02 – Webhook / audit event integrity issues**
  - Model a scenario where security-relevant events can be forged, dropped, or lack context.

- [ ] **Attack Path 03 – Race conditions on transfers**
  - Demonstrate how concurrent requests can lead to inconsistent balances or double-spend-like behaviour.

- [ ] **Attack Path 04 – Misuse of internal tooling / support APIs**
  - Explore how internal support features or admin-style APIs can be abused if not designed with
    strong authorization and auditing.

## Other Ideas

- Provide example detection rules or pseudo-Sigma queries for key scenarios
- Add variations of the lab for different stacks (e.g. async Python, different data stores)
- Explore techniques for modelling and testing attack paths as part of CI/CD
