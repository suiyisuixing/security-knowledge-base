# v5.0 Release Notes

Built across two commits (initial build `v3.0-rc`, completion pass `v5.0`).
The items below are the components delivered in the completion pass — they are
not separate dated releases.

## Components delivered

- **Reviewer Experience** — bundled `sample_outputs/`, `demo_assets.py`,
  Reviewer Mode panel, portfolio summary, reviewer quick path.
- **Stability** — JSON schemas, `schema_validator.py`, `integrity_checker.py`,
  `error_model.py`, `diagnostics.py`, `/diagnostics/*` endpoints, frontend
  diagnostics panel.
- **Rule-based Reasoning** — `reasoning/` package (decision tree, policy
  reasoner, risk scoring, evidence builder, template renderer, workflow
  reasoner, explanation builder), `/reasoning/*` endpoints.
- **Hybrid Retrieval** — `retrieval/` package (chunker, lexical,
  semantic-light, hybrid, source trust, citation grounding, faithfulness,
  knowledge conflict, evaluation), `/retrieval/*` endpoints.
- **Agent Hub** — `agent_hub/` package (project adapter, cross-project
  context, skill evidence tracker, portfolio readiness, orchestrator,
  next-action planner, maturity model, roadmap planner), `/agent-hub/*`
  endpoints.

## Verified totals (2026-07-15)

- 721 pytest tests across 69 files, all passing.
- 68 HTTP endpoints.

## Boundaries

- Backend cannot import `requests` / `urllib.request` / `subprocess`.
- `reasoning/`, `retrieval/`, `agent_hub/` are bound by the same rules.
- No LLM connector, no `llm/` directory, no `model_config.json`.

## Future

- Docs polish, caching, screenshots.
- Optional local model behind a feature flag (out of scope now).
