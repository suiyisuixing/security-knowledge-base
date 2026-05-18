---
id: det-coverage-001
title: Detection Coverage
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
  - Coverage
  - ATT&CK
  - Detection
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

Detection coverage describes which adversary behaviors a team is positioned to see, given current data sources and detection content. Coverage is measured against a stable taxonomy such as MITRE ATT&CK and against the data sources actually flowing into the SIEM.

## Why it matters

Counting rules is not coverage. A team can have hundreds of rules concentrated on a handful of techniques and large blind spots elsewhere. Coverage analysis turns the question from "how many rules" into "what can we actually detect."

## Common indicators

- Lack of ATT&CK mapping on rules
- No inventory of effective data sources
- Coverage discussions that rely on counts
- New rule requests without prioritization context

## Safe local example

In a local lab, map your existing rules to ATT&CK techniques. Build a simple heatmap (technique by tactic). Identify the top three gaps and write a plan for each.

## Defensive verification approach

- Maintain a live mapping of detections to techniques
- Track data-source health
- Run purple-team exercises focused on gaps
- Re-baseline coverage on a regular cadence

## Remediation guidance

- Prioritize gaps by adversary relevance and data-source availability
- Pair coverage work with detection-as-code reviews
- Track coverage trends over releases
- Communicate coverage in plain language to leadership

## Safety boundary

Defensive learning only. No execution of adversary techniques outside a controlled lab.

## Related project connection

Coverage exercises live in `security-log-ai-assistant`. This knowledge base supplies the taxonomy and template.
