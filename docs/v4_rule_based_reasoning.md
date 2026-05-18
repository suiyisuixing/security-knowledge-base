# v4.0 — Rule-based Reasoning

## Goal

Add a deterministic, model-free reasoning layer that:

- Matches rules to a query (`reasoning/rule_engine.py`).
- Walks decision trees for safety, authorization and routing
  (`reasoning/decision_tree.py`).
- Explains *why* the safety policy decided what it decided
  (`reasoning/policy_reasoner.py`).
- Scores risk on a 5-level scale (`reasoning/risk_scoring.py`).
- Builds an evidence chain from retrieved local documents
  (`reasoning/evidence_builder.py`).
- Renders templates for grounded answers, workflows and routes
  (`reasoning/template_renderer.py`).
- Produces planning artifacts only — never executes
  (`reasoning/workflow_reasoner.py`).
- Composes user-friendly explanations
  (`reasoning/explanation_builder.py`).

The `reasoning_service` module orchestrates these for the API.

## API additions

- `POST /reasoning/rule-match`
- `POST /reasoning/decision-path`
- `POST /reasoning/risk-score`
- `POST /reasoning/evidence-chain`
- `POST /reasoning/reasoned-answer`
- `POST /reasoning/policy-explanation`

## Boundary

No LLM. No HTTP. No subprocess. Every output is the deterministic result of
keyword/structure matching against the bundled JSON.
