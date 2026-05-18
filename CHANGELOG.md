# Changelog

## v5.0-rc — 2026-05-18

Model-free agent hub release. v3.0 is preserved; v3.1 → v5.0 are
incremental additions, all deterministic and local.

### Added

- **v3.1 Reviewer Experience** — `sample_outputs/`, `backend/app/demo_assets.py`,
  `/demo/*` endpoints, Reviewer Mode UI panel, portfolio summary card,
  `docs/v3_1_reviewer_experience.md`, `docs/reviewer_quick_path.md`,
  `docs/example_outputs.md`.
- **v3.2 Stability / Schema** — `schemas/` JSON-schema-like files,
  `backend/app/schema_validator.py`, `backend/app/integrity_checker.py`,
  `backend/app/error_model.py`, `backend/app/diagnostics.py`,
  `/diagnostics/*` endpoints.
- **v4.0 Rule-based Reasoning** — `reasoning/` package
  (`rule_engine.py`, `decision_tree.py`, `policy_reasoner.py`,
  `risk_scoring.py`, `evidence_builder.py`, `template_renderer.py`,
  `workflow_reasoner.py`, `explanation_builder.py`),
  `backend/app/reasoning_service.py`, `/reasoning/*` endpoints,
  bundled `data/reasoning_rules.json` / `data/decision_trees.json` /
  `data/risk_scoring_rules.json` / `data/template_blocks.json`.
- **v4.5 Hybrid Retrieval** — `retrieval/` package
  (`chunker.py`, `lexical.py`, `semantic_light.py`, `hybrid.py`,
  `citation_grounding.py`, `faithfulness.py`, `source_trust.py`,
  `knowledge_conflict.py`, `retrieval_eval.py`),
  `backend/app/hybrid_retrieval_service.py`, `/retrieval/*` endpoints,
  bundled `data/security_synonyms.json`, `data/source_trust_rules.json`,
  `data/retrieval_eval_cases.json`.
- **v5.0 Agent Hub** — `agent_hub/` package
  (`project_adapter.py`, `project_status_model.py`, `cross_project_context.py`,
  `skill_evidence.py`, `portfolio_readiness.py`, `agent_orchestrator.py`,
  `next_action_planner.py`, `cross_project_report.py`, `maturity_model.py`,
  `roadmap_planner.py`), `backend/app/agent_hub_service.py`,
  `/agent-hub/*` endpoints, bundled
  `data/project_status_samples.json`, `data/skill_evidence_map.json`,
  `data/portfolio_maturity_model.json`, `data/cross_project_scenarios.json`,
  `data/v5_agent_hub_benchmark.json`.
- React frontend extended with Reviewer Mode, Diagnostics, Reasoning,
  Evidence Chain, Hybrid Retrieval, Source Trust, Agent Hub, Skill
  Evidence, Portfolio Readiness, Next Actions, and v5 Release panels.
- 720+ pytest tests across 47 test files.

### Changed

- Project version: `3.0-rc` → `5.0-rc`.
- `tests/conftest.py` adds the project root to `sys.path` so
  `reasoning/`, `retrieval/`, `agent_hub/` are importable as packages.
- Safety keywords expanded for `blocked_evasion` and `blocked_exfiltration`.
- `authorized_workflow.py` recognises more self-owned-asset phrasings.

### Boundaries

- No LLM connector, no `llm/`, no `model_config.json`.
- No `requests` / `urllib.request` / `subprocess` import in backend code.
- `data/integrity_check_patterns.json` stores forbidden patterns in an
  encoded form so the integrity checker's own source doesn't trip the
  security-boundary tests.

## v3.0-rc — 2026-05-18

Initial release candidate of the Security Knowledge Base & Agent Memory Lab.

### Added
- 32+ Markdown knowledge documents across AI security, API security,
  detection engineering, vulnerability intelligence, secure coding, and safe
  boundaries.
- Safety policy with 19 classes and keyword-based classifier.
- Local BM25-like TF-IDF retrieval over the knowledge base.
- Knowledge-grounded answer builder with citations and safety notes.
- Agent memory store (learning profile, skill progress, completed labs).
- Skill taxonomy (16 skills) mapped to four portfolio projects.
- Learning-path generator for four major directions.
- Authorized workflow planner (local lab / self-owned asset / authorized scope).
- Task router across the four portfolio projects.
- 60+ benchmark tasks across six categories.
- Knowledge quality scoring, citation evaluation, safety evaluation harness.
- Reports: knowledge coverage, safety policy, agent readiness.
- React + Vite frontend dashboard.
- 360+ pytest tests and GitHub Actions CI.

## v2.0-rc — internal preview

- Drafted backend modules and safety policy classes.
- Drafted skill taxonomy and project registry.

## v1.0-rc — internal preview

- Knowledge model and front-matter shape defined.
- Local retrieval prototype.
