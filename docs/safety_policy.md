# Safety Policy

## Classes

### Allowed (8)
- `allowed_learning`
- `allowed_defensive`
- `allowed_local_lab`
- `allowed_authorized_testing`
- `allowed_code_review`
- `allowed_report_generation`
- `allowed_authorized_recon_planning`
- `allowed_authorized_low_risk_check_planning`

### Needs confirmation (4)
- `needs_authorization_confirmation`
- `needs_scope_confirmation`
- `needs_rate_limit_confirmation`
- `needs_target_ownership_confirmation`

### Blocked (8)
- `blocked_unauthorized_public_scan`
- `blocked_credential_attack`
- `blocked_exploit_weaponization`
- `blocked_persistence`
- `blocked_evasion`
- `blocked_exfiltration`
- `blocked_destructive_action`
- `blocked_malware`

## Algorithm

`classify_request` checks classes in this order:

1. Blocked intents (most specific first).
2. Needs-confirmation intents.
3. Allow-list intents.
4. Default to `allowed_learning` when nothing matches.

This ordering means a request like "Scan my local lab" will be classified as
local-lab (allowed), but "Scan this public IP" will be blocked first.

## Safe redirects

Every class includes a `safe_redirect` string that the application can show to
the user when blocking or asking for confirmation. The agent must never give
attack guidance even when redirecting.

## Audit

`backend/app/audit.py` writes a JSONL log entry per decision. Sensitive
patterns (`Authorization`, `Bearer`, `password=`, `token=`, `sk-...`) are
redacted before write.
