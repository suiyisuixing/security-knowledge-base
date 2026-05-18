# Authorized Workflow

## Purpose

`POST /workflow/authorized-plan` produces a planning artifact for activity
that requires scoped authorization. The artifact is text only. The system
does not execute scans, does not call external services, and does not
produce weaponized output.

## Scope detection

The planner accepts a request if any of the following claims appear:

- Local lab (`my local lab`, `in my lab`, `local vm`, `isolated lab`, `home lab`).
- Self-owned asset (`my own server`, `my staging`, `my own asset`, `my own repo`, `my own site`).
- Authorized engagement (`i have authorization`, `authorized scope`, `bug bounty scope`,
  `explicit authorization`, `engagement scope`).

Otherwise the planner blocks with a redirect.

## Steps when allowed

1. Confirm authorization and scope.
2. Identify assets within scope.
3. Perform low-risk information collection planning.
4. Generate safe verification plan.
5. Prepare remediation report.

## Blocked actions (always)

- No unauthorized public scanning.
- No credential attacks.
- No exploit weaponization.
- No persistence or backdoors.
- No detection evasion.
- No data exfiltration.
- No destructive operations.
