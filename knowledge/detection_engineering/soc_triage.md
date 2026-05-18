---
id: det-soc-triage-001
title: SOC Triage Fundamentals
domain: detection_engineering
difficulty: medium
related_projects:
  - security-log-ai-assistant
  - security-knowledge-base
related_skills:
  - alert_triage
  - log_analysis
  - mitre_mapping
tags:
  - SOC
  - Triage
  - Workflow
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

SOC triage is the process of taking incoming alerts, enriching them with context, and deciding what to do next: close, escalate, hunt, or treat as an incident. Triage is the bridge between detection content and incident response.

## Why it matters

Without consistent triage, even good detections drown teams in noise. Triage standards make outcomes comparable across analysts and shifts and let leadership measure how detections perform in the real world.

## Common indicators

- Alerts closed without a documented reason
- Wide variance in triage outcomes between analysts on the same content
- No standard enrichment per alert type
- No feedback loop to detection engineers

## Safe local example

In a local lab, define a small alert taxonomy (low, medium, high). For each, write a triage playbook with required enrichments and expected outcomes. Walk through synthetic alerts and document the decisions.

## Defensive verification approach

- Track time-to-triage and resolution rates
- Sample closed alerts for quality review
- Compare triage outcomes against post-incident reviews
- Feed insights back into detection content

## Remediation guidance

- Standardize required enrichments per alert type
- Provide playbooks and templates
- Train analysts on judgment calls, not just steps
- Measure and tune false-positive rates by source

## Safety boundary

Use only synthetic or owned alert data. Do not include third-party private telemetry.

## Related project connection

Triage workflows are exercised in `security-log-ai-assistant`. This knowledge base supplies the concept and template.
