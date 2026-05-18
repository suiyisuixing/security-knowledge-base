---
id: bound-limited-authorized-recon-001
title: Limited Authorized Reconnaissance Planning
domain: safe_boundaries
difficulty: medium
related_projects:
  - security-knowledge-base
  - vulnerability-intelligence-lab
related_skills:
  - authorized_recon_planning
  - safe_verification_planning
  - safety_boundary_classification
tags:
  - Safe Boundary
  - Reconnaissance
  - Planning
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

Limited authorized reconnaissance planning means producing a written plan for information gathering inside a documented authorization. The plan describes what will be collected, why, by which low-risk methods, and with what guardrails. Execution remains the responsibility of an authorized human.

## Why it matters

Most real assessments need a plan before any activity. Documenting the plan keeps the engagement within scope, makes review possible, and prevents drift toward unauthorized actions.

## Common indicators

- Written plan with scope, methods, and guardrails
- Defined out-of-scope items
- Stop conditions and escalation paths
- A clear owner

## Safe local example

Draft a one-page plan for a low-risk recon activity inside a documented engagement. Include the target list, allowed and disallowed methods, rate limits, expected outputs, stop conditions, and review path. Do not execute from this knowledge base.

## Defensive verification approach

- Review the plan with the system owner before any activity
- Keep the plan in version control with the engagement records
- Confirm guardrails before each session
- Log activity centrally

## Remediation guidance

- Iterate the plan as scope evolves
- Document deviations
- Apply the smallest method that answers the question
- Stop and re-confirm when authorization ambiguity appears

## Safety boundary

The system supports planning for limited authorized recon inside a documented scope. It does not perform scans, does not call external services, and does not produce weaponized output.

## Related project connection

Planning artifacts feed analyses in `vulnerability-intelligence-lab` and decisions in `security-log-ai-assistant`. Concept and template live here.
