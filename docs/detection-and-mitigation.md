# Detection and Mitigation

This document outlines ideas for detecting the attack paths in this lab and hardening the
underlying design.

## Logging

Good logging is a prerequisite for both detection and investigation. For the endpoints involved
in Attack Path 01 (`/accounts/{id}/balance` and related APIs), logs should ideally include:

- `user_id` (from the authenticated identity)
- `account_id` (from the path or request body)
- Timestamp
- Source IP / user agent (where appropriate)
- Outcome (success / failure and reason)

Examples of events worth logging:

- Access to any `/accounts/{id}` endpoint
- Failed authorization checks
- Unusual error conditions

## Detection Ideas

Potential detection rules or analytics could include:

- A single `user_id` accessing **many distinct `account_id` values** within a short time window
- Repeated access attempts to non-existent or invalid `account_id` values
- Access to `account_id` values that are known not to belong to the authenticated `user_id`

In a production environment, these signals would typically feed into a SIEM or similar system for
alerting and correlation with other events.

## Mitigation Ideas

- Implement strict **ownership checks** in `accounts-service` to ensure that:
  - any access to `/accounts/{id}` verifies that `id` belongs to the authenticated user, or
  - the user has a role that explicitly permits cross-account access.

- Avoid leaking details in error messages that help attackers infer valid identifiers.

- Consider adding **rate limiting** and anomaly detection around access patterns to account
  resources.

- Perform regular **secure design and code reviews** focused on:
  - how identity information is propagated between services,
  - how authorization decisions are made,
  - and whether logging is sufficient to support detection and root-cause analysis.

The intent of this lab is not to provide a complete defense strategy, but to show how
attackers think about these systems and how security engineers can reason about improving them.
