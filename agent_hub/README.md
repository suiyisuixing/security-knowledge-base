# agent_hub/ — A/B/C/D rule-based agent hub (v5.0)

Model-free; metadata only; never reads or modifies A/B/C source files.
Only the bundled `data/project_status_samples.json`, `project_registry.json`,
and `skill_evidence_map.json` are consulted.

| Module | Purpose |
|---|---|
| `project_adapter.py` | Load registry + status samples and produce per-project summaries. |
| `project_status_model.py` | Pydantic schemas for project status and skill evidence. |
| `cross_project_context.py` | Build a unified context across projects for a query. |
| `skill_evidence.py` | Track evidence (artifacts + confidence) per skill. |
| `portfolio_readiness.py` | Score readiness across 10 categories. |
| `agent_orchestrator.py` | Choose reasoning mode and route + retrieve + classify. |
| `next_action_planner.py` | Recommend project / skill / docs / tests / demo actions. |
| `cross_project_report.py` | Aggregate cross-project reports. |
| `maturity_model.py` | 5-level maturity model. |
| `roadmap_planner.py` | v5.x and v5→v6 roadmaps + release checklists. |

A/B/C source repositories are **not** read, modified, or scanned by this
package. v6.0 may *optionally* add a local LLM connector behind a feature
flag; that work is out of scope here.
