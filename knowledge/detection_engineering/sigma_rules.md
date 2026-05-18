---
id: det-sigma-rules-001
title: Sigma Rules
domain: detection_engineering
difficulty: medium
related_projects:
  - security-log-ai-assistant
  - security-knowledge-base
related_skills:
  - detection_engineering
  - mitre_mapping
  - log_analysis
tags:
  - Sigma
  - SIEM
  - Detection as Code
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

Sigma is a generic, vendor-neutral signature format for log-based detection rules. A Sigma rule defines a log source, a detection pattern, and metadata such as severity and ATT&CK mapping. Tooling converts the rule into queries for specific SIEMs.

## Why it matters

Sigma makes detection content portable, reviewable, and testable. Teams can version detections in Git, run them through CI, and share rules across organizations.

## Common indicators

- Detections expressed only in vendor-specific query languages
- No version control for detection content
- Rules without ATT&CK or data-source metadata
- No tests against representative log samples

## Safe local example

Write a Sigma rule for a suspicious PowerShell pattern in a local lab. Convert it with a Sigma backend for your SIEM. Apply it to a synthetic log sample and confirm the detection triggers as expected.

## Defensive verification approach

- Treat detections as code with reviews and tests
- Generate representative event samples for every rule
- Run conversion and validation in CI
- Track false-positive rates per rule

## Remediation guidance

- Keep rules small and well-scoped
- Add severity and confidence metadata
- Map every rule to ATT&CK
- Maintain a deprecation process for outdated rules

## Safety boundary

Defensive content only. Rules and samples should be synthetic or sourced from systems you own. Do not include real production data.

## Related project connection

Sigma-style triage and rule maintenance live in `security-log-ai-assistant`. This knowledge base provides the concept and template.
