---
id: bound-responsible-disclosure-001
title: Responsible Disclosure
domain: safe_boundaries
difficulty: medium
related_projects:
  - security-knowledge-base
  - vulnerability-intelligence-lab
related_skills:
  - safe_verification_planning
  - safety_boundary_classification
  - vulnerability_prioritization
tags:
  - Disclosure
  - Reporting
  - Coordination
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

Responsible disclosure is the process of reporting a vulnerability to the affected vendor or owner and giving them a reasonable window to remediate before any public discussion. It balances the right to know with the time required to fix.

## Why it matters

Disclosure done well protects users, builds trust with vendors, and earns credibility for the reporter. Disclosure done badly creates risk for users and reputation costs for everyone involved.

## Common indicators

- Reports sent to documented contact channels
- Agreed timeline and updates
- Sensitive details kept off public channels until coordinated
- Records of communication

## Safe local example

Practice writing a disclosure report for a finding in a local lab. Include scope, impact, reproduction notes that avoid weaponization, and proposed remediation. Keep the language factual.

## Defensive verification approach

- Use the vendor's published security contact
- Maintain a coordinated timeline
- Update the report as new information appears

## Remediation guidance

- Be specific, factual, and short
- Avoid attack chains in public discussion
- Coordinate with the vendor on timing
- Credit fixes and people fairly

## Safety boundary

This document covers disclosure planning for findings discovered under authorized conditions or in local labs. It does not encourage or describe unauthorized discovery.

## Related project connection

Disclosure work intersects with `vulnerability-intelligence-lab`. Concept and template live here.
