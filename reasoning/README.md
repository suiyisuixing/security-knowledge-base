# reasoning/ — Rule-based reasoning layer (v4.0)

Model-free, deterministic, testable. Every module here uses only Python
standard library + bundled JSON. No LLM, no HTTP.

| Module | Purpose |
|---|---|
| `rule_engine.py` | Load and match rule sets (`data/reasoning_rules.json`). |
| `decision_tree.py` | Step-by-step decision paths for safety / authorization / routing. |
| `policy_reasoner.py` | Human-readable explanations of safety classifications. |
| `risk_scoring.py` | Keyword-based risk score: informational / low / medium / high / blocked. |
| `evidence_builder.py` | Compose a citation/evidence chain from local knowledge. |
| `template_renderer.py` | Render grounded answers, workflow plans, etc., from evidence. |
| `workflow_reasoner.py` | Generate safe verification / low-risk / local lab plans only. |
| `explanation_builder.py` | Short + user-friendly + reviewer-focused explanations. |
