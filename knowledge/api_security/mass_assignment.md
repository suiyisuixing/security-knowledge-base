---
id: api-mass-assignment-001
title: Mass Assignment / BOPLA
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
  - Mass Assignment
  - BOPLA
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

Mass assignment (now framed as Broken Object Property Level Authorization, BOPLA) happens when an API accepts a JSON body and binds every field to a database object without filtering. A client can then set fields they should not be allowed to set, such as `is_admin`, `balance`, or `role`.

## Why it matters

Mass assignment looks like a small developer convenience but commonly leads to privilege escalation, financial impact, or data integrity loss. It is invisible to clients but devastating in audit logs.

## Common indicators

- Handlers that pass `request.json` directly into `Model(**body)` or ORM updaters
- No allow-list of writable fields
- Field-level differences across roles are not enforced server-side
- Tests cover happy paths but not field tampering

## Safe local example

Implement a local `PATCH /users/me` endpoint that binds every field. Send a body that includes `is_admin: true`. Verify the field was set. Add a field allow-list and confirm tampering is rejected.

## Defensive verification approach

- Maintain a writable-fields allow-list per endpoint and per role
- Test field tampering for every endpoint
- Add static analyzers that flag direct binding of request bodies
- Audit changes to sensitive fields

## Remediation guidance

- Use explicit input schemas (Pydantic, dataclasses, DTOs)
- Reject unknown fields by default
- Separate user-modifiable fields from admin-modifiable fields
- Log changes to sensitive fields with caller identity

## Safety boundary

Defensive reference only. No third-party exploitation. Practice in local labs or authorized environments.

## Related project connection

CVE pattern catalog in `vulnerability-intelligence-lab`. Concepts and templates here.
