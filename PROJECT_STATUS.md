# Project Status

- Status: feature-complete, model-free (local educational project)
- Date: 2026-05-18
- Author: suiyisuixing

This project was built as an AI-assisted learning project, with author-directed
design, validation, and review. The component groups below describe *what was
built* — they are scope milestones, not separate public releases.

## What is built

- **Core** — FastAPI backend (32 modules), local Markdown knowledge base,
  React/Vite frontend, and a 60-task benchmark.
- **Reviewer experience** — bundled `sample_outputs/`, `demo_assets.py`,
  Reviewer Mode UI, and `/demo/*` endpoints.
- **Stability / schema** — JSON schemas (`schemas/`), `schema_validator.py`,
  `integrity_checker.py`, `error_model.py`, and `/diagnostics/*` endpoints.
- **Rule-based reasoning** — `reasoning/` package (rule engine, decision tree,
  policy reasoner, risk scoring, evidence and explanation builders) and
  `/reasoning/*` endpoints.
- **Hybrid retrieval** — `retrieval/` package (chunker, lexical scoring,
  light-semantic expansion, hybrid scoring, source trust, citation grounding,
  faithfulness, retrieval evaluation) and `/retrieval/*` endpoints.
- **Agent hub** — `agent_hub/` package (project adapter, cross-project context,
  skill evidence, portfolio readiness, orchestrator, next-action planner,
  5-level maturity model, roadmap planner) and `/agent-hub/*` endpoints.

## Numbers (re-verified 2026-07-15)

- 68 HTTP endpoints
- 721 pytest tests, all passing, across 69 test files
- 32 local Markdown knowledge documents
- 60 benchmark tasks across 6 task types
- 8 JSON-schema-like schemas
- 16 bundled sample outputs

## Known limitations

- Local-only; no production deployment intended.
- Hybrid retrieval is rule-based (chunker + lexical + synonym map + source
  trust). No embeddings, no vector database.
- No model integration; an optional local model behind a feature flag is a
  possible future direction.
