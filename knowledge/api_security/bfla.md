---
id: api-bfla-001
title: Broken Function Level Authorization (BFLA)
domain: api_security
difficulty: medium
related_projects:
  - vulnerability-intelligence-lab
  - security-knowledge-base
related_skills:
  - api_authorization_reasoning
  - secure_code_review
tags:
  - OWASP API
  - BFLA
  - Authorization
safe_use:
  - local_lab
  - authorized_testing
  - defensive_learning
forbidden_use:
  - unauthorized_scanning
  - credential_theft
  - exploit_weaponization
---

## Concept

Broken Function Level Authorization (BFLA) is when a low-privilege user reaches a function that was meant for a higher-privilege role. The function itself works correctly; the gate that decides who may invoke it is missing or weak.

## Why it matters

BFLA promotes a normal user into a partial administrator. Even when the impact is partial, it usually contradicts policy and compliance assumptions, and may chain with other bugs to escalate further.

## Common indicators

- Admin endpoints discoverable by predictable paths (`/admin/...`, `/internal/...`)
- Role checks placed only in the UI layer
- Different HTTP verbs on the same path with mixed enforcement
- Endpoints that return 200 to forbidden callers and rely on UI to hide buttons

## Safe local example

In a local lab, define `user` and `admin` roles. Add `POST /admin/users/{id}/disable`. Skip the role check intentionally. Sign in as a normal user and call the endpoint. Confirm the action succeeded. Add a decorator that enforces role and re-run.

## Defensive verification approach

- Maintain an explicit role matrix
- Add tests that call each admin endpoint as each non-admin role
- Run static checks for missing role decorators
- Log denied calls for monitoring

## Remediation guidance

- Centralize role checks at the routing or middleware layer
- Deny by default and add allow rules explicitly
- Audit endpoint inventory regularly
- Consider attribute-based access control for complex domains

## Safety boundary

Defensive reference only. No third-party exploitation guidance. Use ideas in local labs or authorized engagements.

## Related project connection

CVE and reasoning exercises in `vulnerability-intelligence-lab`. This knowledge base contains the concept and reasoning template.
