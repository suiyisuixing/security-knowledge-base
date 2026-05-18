# Project Status

- Version: **v5.0-rc**
- Date: 2026-05-18
- Author: suiyisuixing
- Status: feature-complete release candidate (model-free)

## Completed

- v3.0 — Backend (23 modules), FastAPI surface, 32+ Markdown docs, 60-task
  benchmark, React/Vite frontend.
- v3.1 — Sample outputs (`sample_outputs/`), `demo_assets.py`,
  Reviewer Mode UI, portfolio summary, `/demo/*` endpoints.
- v3.2 — JSON schemas (`schemas/`), `schema_validator.py`,
  `integrity_checker.py`, `error_model.py`, `diagnostics.py`,
  `/diagnostics/*` endpoints.
- v4.0 — `reasoning/` package (rule engine, decision tree, policy
  reasoner, risk scoring, evidence builder, template renderer, workflow
  reasoner, explanation builder), `/reasoning/*` endpoints.
- v4.5 — `retrieval/` package (chunker, lexical, semantic-light, hybrid,
  source trust, citation grounding, faithfulness, knowledge conflict,
  retrieval evaluation), `/retrieval/*` endpoints.
- v5.0 — `agent_hub/` package (project adapter, cross-project context,
  skill evidence, portfolio readiness, agent orchestrator, next-action
  planner, cross-project report, maturity model, roadmap planner),
  `/agent-hub/*` endpoints.

## Numbers

- 68 HTTP endpoints
- 720+ pytest tests, all passing
- 6 knowledge domains, 32+ documents
- 60 benchmark tasks (10 per category, 6 categories)
- 16+ skills mapped across A/B/C/D
- 8 JSON-schema-like schemas
- 15+ bundled sample outputs

## Known limitations

- Local-only; no production deployment intended.
- Hybrid retrieval is rule-based (chunker + lexical + synonym map +
  trust). No embeddings, no vector DB.
- No model integration. v6.0 may add an optional local model behind a
  feature flag.
