# v5.0 Release Notes

## What's new since v3.0

- **v3.1 Reviewer Experience** — bundled `sample_outputs/`, `demo_assets.py`,
  Reviewer Mode panel, portfolio summary, reviewer quick path.
- **v3.2 Stability** — JSON schemas, `schema_validator.py`,
  `integrity_checker.py`, `error_model.py`, `diagnostics.py`,
  `/diagnostics/*` endpoints, frontend diagnostics panel.
- **v4.0 Rule-based Reasoning** — `reasoning/` package, decision tree,
  policy reasoner, risk scoring, evidence builder, template renderer,
  workflow reasoner, explanation builder, `/reasoning/*` endpoints.
- **v4.5 Hybrid Retrieval** — `retrieval/` package: chunker, lexical,
  semantic-light, hybrid, source trust, citation grounding, faithfulness,
  knowledge conflict, evaluation. `/retrieval/*` endpoints.
- **v5.0 Agent Hub** — `agent_hub/` package: project adapter,
  cross-project context, skill evidence tracker, portfolio readiness,
  orchestrator, next-action planner, maturity model, roadmap planner.
  `/agent-hub/*` endpoints.

## Test counts

- v3.0: 386
- v5.0: 720+ (added ~340 new tests across new modules)

## API surface

- v3.0: 38 endpoints
- v5.0: 68 endpoints

## Boundaries

Same as v3.0 plus stronger:

- Backend still cannot import `requests`/`urllib.request`/`subprocess`.
- `reasoning/`, `retrieval/`, `agent_hub/` are bound by the same rules.
- No LLM connector, no `llm/` directory, no `model_config.json`.

## Future

v5.x — docs polish, caching, screenshots.
v6.0 — optional local model behind a feature flag.
