# v5.0 — A/B/C/D Rule-based Agent Hub & Portfolio Control Plane

## Goal

Project D becomes the *control plane* for the A/B/C/D portfolio. It routes
queries, retrieves grounded knowledge, classifies safety, plans authorized
workflows, tracks skill evidence, and scores portfolio readiness — all
without an LLM.

## Modules (`agent_hub/`)

| Module | Purpose |
|---|---|
| `project_adapter.py` | Bundled metadata only; never opens A/B/C source files. |
| `project_status_model.py` | Pydantic shapes for project status, capability, evidence. |
| `cross_project_context.py` | Merge knowledge + routing + safety + skills for a query. |
| `skill_evidence.py` | Records (project, skill, artifacts, confidence) + reporting. |
| `portfolio_readiness.py` | Score 10 readiness categories → overall 0..1. |
| `agent_orchestrator.py` | Pick reasoning mode → orchestrate → return result. |
| `next_action_planner.py` | Recommend project / skill / docs / tests / demo actions. |
| `cross_project_report.py` | Aggregate cross-project reports. |
| `maturity_model.py` | 5-level maturity model. |
| `roadmap_planner.py` | v5.x and v5→v6 roadmaps. |

## Orchestration modes

Selected purely from keyword/structure rules — no model:

- `knowledge_only`
- `safety_classification`
- `authorized_workflow`
- `project_routing`
- `portfolio_gap_analysis`
- `skill_gap_analysis`
- `rule_based_grounded_answer`
- `benchmark_analysis`

## A/B/C/D mapping

| Project | Focus | Key skills |
|---|---|---|
| A — llm-security-lab | AI/RAG Security Evaluation | prompt_injection_reasoning, rag_access_control, secure_retrieval_design, llm_security_evaluation |
| B — security-log-ai-assistant | Detection Engineering / SOC | log_analysis, mitre_mapping, alert_triage, detection_engineering |
| C — vulnerability-intelligence-lab | Vulnerability Intelligence | vulnerability_prioritization, api_authorization_reasoning, dependency_risk_reasoning, safe_verification_planning |
| D — security-knowledge-base | Knowledge / Safety / Memory / Hub | safety_boundary_classification, task_routing, agent_memory, hybrid_retrieval, rule_based_reasoning, portfolio_readiness |

## Boundary

- A/B/C source files are never read or modified. Only bundled
  `data/project_status_samples.json`, `project_registry.json`,
  `skill_evidence_map.json` are consulted.
- No external API.
- No LLM. v6.0 may introduce an *optional* local model connector behind a
  feature flag.
