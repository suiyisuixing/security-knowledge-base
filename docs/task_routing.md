# Task Routing

## Rules

```
rag / prompt injection / llm   → llm-security-lab
logs / alerts / sigma / mitre  → security-log-ai-assistant
cve / api / sbom / openapi     → vulnerability-intelligence-lab
concept / policy / safety      → security-knowledge-base   (default)
```

## Output

```json
{
  "query": "Help me triage these SOC alerts.",
  "project_id": "security-log-ai-assistant",
  "knowledge_domain": "detection_engineering",
  "skill_id": "alert_triage",
  "explanation": "Routed query to project=... domain=... skill=... based on keyword rules."
}
```

## Design notes

- The router never executes the routed task; it only suggests a destination.
- Rules are intentionally explicit so that reviewers can audit them.
- Unmatched queries default to this project (the knowledge layer).
