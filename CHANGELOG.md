# Changelog

This project was built across two commits on 2026-05-18. The entries below group
the work by what was added — they are not separate public releases.

## v5.0 — completion pass (`a210b73`)

Model-free agent hub and hybrid retrieval, all deterministic and local.

### Added

- **Reviewer experience** — `sample_outputs/`, `backend/app/demo_assets.py`,
  `/demo/*` endpoints, Reviewer Mode UI panel, portfolio summary card.
- **Stability / schema** — `schemas/` JSON-schema-like files,
  `backend/app/schema_validator.py`, `backend/app/integrity_checker.py`,
  `backend/app/error_model.py`, `backend/app/diagnostics.py`,
  `/diagnostics/*` endpoints.
- **Rule-based reasoning** — `reasoning/` package (`rule_engine.py`,
  `decision_tree.py`, `policy_reasoner.py`, `risk_scoring.py`,
  `evidence_builder.py`, `template_renderer.py`, `workflow_reasoner.py`,
  `explanation_builder.py`), `backend/app/reasoning_service.py`,
  `/reasoning/*` endpoints, bundled reasoning/rule data.
- **Hybrid retrieval** — `retrieval/` package (`chunker.py`, `lexical.py`,
  `semantic_light.py`, `hybrid.py`, `citation_grounding.py`, `faithfulness.py`,
  `source_trust.py`, `knowledge_conflict.py`, `retrieval_eval.py`),
  `backend/app/hybrid_retrieval_service.py`, `/retrieval/*` endpoints.
- **Agent hub** — `agent_hub/` package (`project_adapter.py`,
  `project_status_model.py`, `cross_project_context.py`, `skill_evidence.py`,
  `portfolio_readiness.py`, `agent_orchestrator.py`, `next_action_planner.py`,
  `cross_project_report.py`, `maturity_model.py`, `roadmap_planner.py`),
  `backend/app/agent_hub_service.py`, `/agent-hub/*` endpoints.
- React frontend extended with panels for all of the above.

### Boundaries

- No LLM connector, no `llm/`, no `model_config.json`.
- No `requests` / `urllib.request` / `subprocess` imports in backend code.
- `data/integrity_check_patterns.json` stores forbidden patterns in an encoded
  form so the integrity checker's own source doesn't trip the security-boundary
  tests.

## v3.0-rc — initial build (`ad70742`)

Security Knowledge Base & Agent Memory Lab.

### Added

- 32 Markdown knowledge documents across six domains (AI security, API
  security, detection engineering, vulnerability intelligence, secure coding,
  safe boundaries).
- Safety policy with 19 classes and a keyword-based classifier.
- Local BM25-like TF-IDF retrieval; knowledge-grounded answer builder with
  citations and safety notes.
- Agent memory store (learning profile, skill progress, completed labs).
- Skill taxonomy (16 skills) mapped to four portfolio projects.
- Learning-path generator, authorized workflow planner, and task router.
- 60 benchmark tasks across six task types.
- Knowledge quality scoring, citation evaluation, safety evaluation harness.
- Reports: knowledge coverage, safety policy, agent readiness.
- React + Vite frontend dashboard.

## Totals (re-verified 2026-07-15)

- 721 pytest tests across 69 test files, GitHub Actions CI.
- 68 HTTP endpoints, 8 schemas, 16 bundled sample outputs.
