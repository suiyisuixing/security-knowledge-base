# Knowledge Model

Each knowledge document is a Markdown file with YAML front matter and a fixed
body template.

## Front matter

```yaml
---
id: api-bola-001
title: Broken Object Level Authorization
domain: api_security
difficulty: medium
related_projects: [vulnerability-intelligence-lab]
related_skills: [api_authorization_reasoning, safe_verification_planning]
tags: [OWASP API, BOLA, IDOR]
safe_use: [local_lab, authorized_testing, defensive_learning]
forbidden_use: [unauthorized_scanning, credential_theft, exploit_weaponization]
---
```

## Body sections

1. Concept
2. Why it matters
3. Common indicators
4. Safe local example
5. Defensive verification approach
6. Remediation guidance
7. Safety boundary
8. Related project connection

## Domains

- `ai_security`
- `api_security`
- `detection_engineering`
- `vulnerability_intelligence`
- `secure_coding`
- `safe_boundaries`

## IDs

Document IDs are stable and follow `<domain-prefix>-<topic>-NNN`. The loader
falls back to the file stem when an explicit `id` is missing.

## Loader

`backend/app/knowledge_loader.py` reads all `.md` files under `knowledge/`,
parses front matter via a small in-house YAML reader (no external dependency),
and caches the index in memory.
