---
id: bound-no-unauthorized-scanning-001
title: No Unauthorized Scanning
domain: safe_boundaries
difficulty: easy
related_projects:
  - security-knowledge-base
related_skills:
  - safety_boundary_classification
  - safe_verification_planning
tags:
  - Safe Boundary
  - Policy
  - Refusal
safe_use:
  - local_lab
  - defensive_learning
forbidden_use:
  - unauthorized_scanning
  - credential_theft
  - exploit_weaponization
---

## Concept

Unauthorized scanning means probing systems you do not own and have not been authorized to test. It includes port scans, vulnerability scans, credential checks, and any active interaction whose purpose is to discover weaknesses without permission.

## Why it matters

Unauthorized scanning can violate laws and contracts, generate incidents for the owner, and waste investigation effort. The agent declines to plan or assist with such activity.

## Common indicators

- Requests that name a third-party domain or IP without proof of ownership or authorization
- Requests that describe production targets without scope
- Requests that escalate from learning questions to active probing

## Safe local example

If the desired activity is learning, switch to a local lab. If it is professional assessment, secure a written engagement with documented scope and stay inside it.

## Defensive verification approach

- The safety policy classifies such requests as blocked
- The agent redirects to local labs, authorized testing, or defensive review

## Remediation guidance

- Decline and explain
- Offer a safe alternative

## Safety boundary

The system refuses unauthorized scanning. It does not provide scanner commands, payloads, or evasion guidance for such activity.

## Related project connection

This boundary is enforced across all four portfolio projects.
