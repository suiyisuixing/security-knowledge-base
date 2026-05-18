# v3.2 — Stability / Schema / Engineering Maturity

## Goal

Make the project feel like a *stable engineered tool*, not a one-shot
generation. Reviewers should be able to:

- See JSON schemas for every data artifact.
- Run an integrity check against the source tree.
- Receive uniform error shapes from every endpoint.
- See a backend diagnostics report with the same surface as a real service.

## What was added

### `schemas/`

JSON-schema-like definitions for:

- `knowledge_metadata`
- `safety_policy`
- `skill_taxonomy`
- `project_registry`
- `benchmark_task`
- `memory_profile`
- `skill_progress`
- `agent_readiness`

### `backend/app/schema_validator.py`

Lightweight validator (Python stdlib only, no third-party `jsonschema`).
Supports `required`, `type`, `enum`, list item types, and nested object
schemas.

### `backend/app/integrity_checker.py`

Verifies tree structure, required files, knowledge domain coverage, sample
outputs, forbidden imports, no external API usage, no real scanning tool
strings, no model integration patterns.

### `backend/app/error_model.py`

Uniform API error envelope:

```json
{"error": true, "code": "not_found", "message": "...", "safe_redirect": "...", "details": {}}
```

### `backend/app/diagnostics.py`

`/diagnostics/health`, `/diagnostics/integrity`, `/diagnostics/schema-validation`,
`/diagnostics/project-status`.

## Boundary

Validation is fully local. No external HTTP. No real scanning. No model.
