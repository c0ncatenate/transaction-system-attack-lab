# Threat Model

This document captures a lightweight threat model for the Transaction System Attack Lab. It is
not intended to be exhaustive, but to demonstrate the kind of thinking applied when assessing
multi-service platforms.

## Assets

- **Account data**
  - Balances and basic profile information
- **Transaction operations**
  - Ability to initiate and complete transfers
- **Authentication tokens**
  - Tokens issued by `auth-service` representing user identity and role
- **Audit logs**
  - Security and operational events used for detection and investigations

## Actors

- **External user**
  - Legitimate customer of the platform
- **Malicious user**
  - Registered user attempting to abuse the system for unauthorized access or financial gain
- **Operator / admin**
  - Internal staff with elevated access (out of scope for the initial lab, reserved for future scenarios)

## Trust Boundaries

1. **Client ↔ auth-service**
   - Boundary between untrusted external clients and the first internal component.
   - Concerns: credential handling, brute force, session/token security.

2. **auth-service ↔ accounts-service**
   - Boundary where identity is passed as tokens/headers between services.
   - Concerns: token validation, misuse of claims, confused deputy problems.

3. **accounts-service ↔ audit-service**
   - Boundary where security-relevant events are emitted.
   - Concerns: integrity of logs, missing events, lack of context.

## Example Threats (STRIDE-like)

- **Spoofing**
  - Use of stolen or replayed tokens to impersonate another user.

- **Tampering**
  - Manipulating requests to access other users' accounts via ID patterns.

- **Repudiation**
  - Actions that are not logged with sufficient detail to attribute them to a user.

- **Information Disclosure**
  - Reading balances or account details for other users (broken access control / IDOR).

- **Denial of Service**
  - Out of scope for the initial scenario (could be added later).

- **Elevation of Privilege**
  - Using weak authorization checks on `accounts-service` to perform actions beyond a user's intended role.

See `docs/attack-path-01-idor-broken-access-control.md` for a concrete attack path built around
information disclosure and broken access control.
