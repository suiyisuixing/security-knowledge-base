---
id: api-bola-001
title: Broken Object Level Authorization (BOLA / IDOR)
domain: api_security
difficulty: medium
related_projects:
  - vulnerability-intelligence-lab
  - security-knowledge-base
related_skills:
  - api_authorization_reasoning
  - safe_verification_planning
  - secure_code_review
tags:
  - OWASP API
  - BOLA
  - IDOR
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

Broken Object Level Authorization (BOLA), historically called IDOR, occurs when an API endpoint accepts an object identifier from the client but does not check whether the calling principal is allowed to access that specific object. The handler authenticates the caller but skips authorization on the object.

## Why it matters

BOLA is the single most common API risk. It usually does not require special tools; a normal authenticated user simply iterates IDs. The impact ranges from data exposure to silent data tampering, depending on the verb.

## Common indicators

- Routes of the form `/resource/{id}` that read or modify by ID with no ownership check
- Shared service-layer functions that do not require a caller identity
- Logs showing successful operations across user boundaries with the same account
- Code reviews where authorization sits in the controller only on some endpoints

## Safe local example

Build a small local API with two users and two notes each. Add a `GET /notes/{id}` endpoint that only checks authentication. Authenticate as user A and request user B's note ID. Confirm the data leaks. Add an explicit `note.owner_id == current_user.id` check and re-run.

## Defensive verification approach

- Maintain an authorization matrix per endpoint, per role
- Write paired tests that assert allowed and denied access for each object
- Use property-based tests over random IDs
- Log authorization decisions with object IDs (without leaking content)

## Remediation guidance

- Push authorization into a single layer that wraps every object lookup
- Prefer opaque, unpredictable IDs as defense in depth
- Reject requests that omit identity context
- Return 404 rather than 403 for unauthorized lookups when appropriate to avoid resource enumeration

## Safety boundary

This document is for defensive review. It does not include payloads against third-party services. Use ideas only in local labs or authorized assessments.

## Related project connection

`vulnerability-intelligence-lab` hosts BOLA-style sample CVEs and reasoning exercises. This knowledge base provides the concept and reasoning template the agent uses.
