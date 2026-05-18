---
id: det-mitre-attack-basics-001
title: MITRE ATT&CK Basics
domain: detection_engineering
difficulty: easy
related_projects:
  - security-log-ai-assistant
  - security-knowledge-base
related_skills:
  - mitre_mapping
  - detection_engineering
  - log_analysis
tags:
  - MITRE
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

MITRE ATT&CK is a knowledge base of adversary behavior organized by tactics (the goal), techniques (the method), and sub-techniques (specific variants). It gives defenders a stable vocabulary for describing what attackers do across the kill chain.

## Why it matters

Without a shared taxonomy, detection coverage discussions stay anecdotal. ATT&CK lets a team map detections, gaps, and incidents to the same set of identifiers, making coverage measurable and reviews repeatable.

## Common indicators

- Detections without explicit ATT&CK mappings
- Coverage measured by rule count rather than technique coverage
- Incident reports that describe behavior without referencing a tactic
- Tabletop exercises that do not exercise specific techniques

## Safe local example

In a local lab, pick three techniques relevant to your environment (for example, valid accounts, command-line interface, scheduled tasks). For each, draft a one-paragraph description of how the behavior would appear in your logs.

## Defensive verification approach

- Tag every detection rule with one or more ATT&CK technique IDs
- Build a coverage heatmap and review it quarterly
- Run purple-team exercises that exercise specific techniques
- Track coverage trends over releases

## Remediation guidance

- Treat ATT&CK as a coverage map, not a checklist
- Combine technique coverage with data-source coverage
- Update mappings as new sub-techniques appear
- Document why a technique is intentionally not covered

## Safety boundary

Defensive learning only. No execution of adversary techniques outside a controlled lab. Use the framework for understanding and detection design.

## Related project connection

Detection rules and triage workflows live in `security-log-ai-assistant`. This knowledge base provides the taxonomy and reasoning template.
