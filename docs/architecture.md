# Architecture

This lab models a small, service-oriented transaction platform made up of three core components:

- **`auth-service`**
  - Responsible for user login and token issuance
  - Issues tokens that contain a `user_id` and (simplified) role information
  - Trust boundary between end-users and the internal services

- **`accounts-service`**
  - Exposes account-related APIs such as:
    - `GET /accounts/{id}/balance`
    - `POST /accounts/transfer`
  - Contains **deliberate access-control weaknesses** that enable:
    - IDOR-style access to other users' account information
    - Unauthorized transfers when token contents are trusted too much

- **`audit-service`**
  - Receives structured audit and security events from other services
  - Intended to illustrate both **good logging** and **missing events / context** that
    make detection and investigations harder

```text
+-------------+        +---------------+        +---------------+
|   Client    | <----> |  auth-service | <----> | accounts-svc  |
+-------------+        +---------------+        +---------------+
                                        \
                                         \
                                          v
                                    +-------------+
                                    | audit-svc   |
                                    +-------------+
```

In a real deployment, each service might live in separate containers or hosts with distinct
network and authentication boundaries. For the purposes of this lab, they are kept simple and
local, but the same **trust-boundary reasoning** applies.

See `docs/threat-model.md` for a threat-modelling view of this architecture.
