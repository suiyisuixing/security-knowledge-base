---
id: det-fp-review-001
title: False Positive Review
domain: detection_engineering
difficulty: medium
related_projects:
  - security-log-ai-assistant
  - security-knowledge-base
related_skills:
  - alert_triage
  - detection_engineering
  - log_analysis
tags:
  - SOC
  - False Positive
  - Detection Tuning
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

False positive review is the disciplined process of looking at alerts marked benign and deciding whether the detection content, the data source, or the triage policy needs to change. It turns noise into a feedback signal.

## Why it matters

Persistent noise erodes analyst attention. Without structured review, teams quietly silence alerts, lose coverage, and miss incidents that look similar to chronic false positives.

## Common indicators

- Rules with high alert volume and low conversion to incidents
- Same root cause appearing in multiple closed alerts
- Analyst notes that say "as usual" or "expected"
- No periodic FP review cadence

## Safe local example

In a local lab, generate a synthetic stream of alerts, including known benign sources. Walk through a structured review: sample, categorize root cause, propose tuning, document outcomes.

## Defensive verification approach

- Sample a fixed percentage of closed alerts per week
- Tag root causes with a controlled vocabulary
- Translate root causes into tuning tasks
- Track tuning impact on alert volume and incident catch rate

## Remediation guidance

- Tune at the right layer (log source, rule, triage)
- Document every silenced source with an owner and review date
- Re-enable silenced sources when the underlying condition changes
- Share tuning outcomes with detection engineering

## Safety boundary

Use only synthetic or owned alert data. Do not include third-party operational details.

## Related project connection

False-positive review is exercised in `security-log-ai-assistant`. Concepts and templates live here.
