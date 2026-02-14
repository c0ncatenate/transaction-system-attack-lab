# Attack Path 01 – IDOR / Broken Access Control on Accounts

This scenario demonstrates how a malicious user can abuse weak access control on account
endpoints to access other users' data and potentially pivot into unauthorized actions.

## Starting Point

- Attacker has a **legitimate user account** on the platform.
- Attacker can log in via `auth-service` and obtain a token (e.g. JWT) containing their `user_id`.

## Discovery

1. The attacker uses the `accounts-service` API to view their own account balance, e.g.:

   ```http
   GET /accounts/1001/balance
   Authorization: Bearer <attacker-token>
   ```

2. The response and error messages hint that account identifiers are **numeric and sequential**.

3. The attacker suspects that the endpoint is using the `id` path parameter directly, without
   confirming that the account belongs to the authenticated user.

## Enumeration

4. The attacker runs an enumeration script such as `scripts/exploit/idor_enumeration.py` to
   request balances for a range of account IDs:

   ```bash
   python scripts/exploit/idor_enumeration.py --start 1000 --end 1100
   ```

5. The script records which IDs return valid account data, effectively enumerating other users'
   account information.

## Impact

- **Information disclosure**: the attacker gains visibility into other users' balances and
  potentially other metadata.
- Depending on how `accounts-service` is implemented, this may also enable:
  - targeting specific high-value accounts,
  - feeding data into further attacks (e.g. social engineering), or
  - validating stolen credentials.

## Root Causes (Design & Implementation)

- `accounts-service` trusts the `id` parameter from the URL without verifying ownership.
- Authorization logic checks that the request is authenticated, but not that the resource belongs
  to the authenticated principal.

## Detection & Logging Considerations

- Are failed and successful access attempts to `/accounts/{id}/balance` logged with:
  - `user_id`
  - `account_id`
  - source IP / user agent
- Can we detect patterns such as:
  - one user accessing many different `account_id` values in a short period?
- Are logs stored in a way that supports investigations (correlation IDs, timestamps, etc.)?

See `docs/detection-and-mitigation.md` for ideas on how to harden this design and improve
logging and detection.
