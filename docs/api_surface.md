# API Surface (v5.0)

`GET /api/surface` returns the live list. The static index below mirrors
the wiring in `backend/app/main.py`.

## Root

| Method | Path | Summary |
|---|---|---|
| GET | `/` | Project metadata |
| GET | `/health` | Liveness check |

## Knowledge (v3.0)

| Method | Path |
|---|---|
| GET | `/knowledge/domains` |
| GET | `/knowledge/docs` |
| GET | `/knowledge/docs/{doc_id}` |
| POST | `/knowledge/search` |
| POST | `/knowledge/ask` |

## Safety (v3.0)

| Method | Path |
|---|---|
| POST | `/safety/classify` |
| GET | `/safety/policy` |
| GET | `/safety/evaluation` |
| POST | `/safety/evaluate` |

## Memory (v3.0)

| Method | Path |
|---|---|
| GET | `/memory/profile` |
| POST | `/memory/update-skill` |
| GET | `/memory/skill-progress` |
| GET | `/memory/audit` |

## Projects / Skills (v3.0)

| Method | Path |
|---|---|
| GET | `/projects` |
| GET | `/projects/{project_id}` |
| GET | `/skills` |
| GET | `/skills/{skill_id}` |
| POST | `/skills/recommend` |

## Learning / Context (v3.0)

| Method | Path |
|---|---|
| POST | `/learning-path/generate` |
| POST | `/context/build` |

## Quality (v3.0)

| Method | Path |
|---|---|
| GET | `/quality/knowledge` |
| GET | `/quality/knowledge/{doc_id}` |
| POST | `/quality/citations/evaluate` |

## Reasoning templates (v3.0)

| Method | Path |
|---|---|
| GET | `/reasoning/templates` |
| GET | `/reasoning/templates/{template_id}` |
| POST | `/workflow/authorized-plan` |
| POST | `/router/route-task` |

## Benchmark (v3.0)

| Method | Path |
|---|---|
| GET | `/benchmark/tasks` |
| POST | `/benchmark/run` |
| GET | `/benchmark/export-jsonl` |

## Reports (v3.0)

| Method | Path |
|---|---|
| POST | `/report/knowledge-coverage` |
| POST | `/report/safety-policy` |
| POST | `/report/agent-readiness` |

## Evaluation (v3.0)

| Method | Path |
|---|---|
| GET | `/evaluation/scenarios` |
| POST | `/evaluation/run` |

## Demo / Reviewer Experience (v3.1)

| Method | Path |
|---|---|
| GET | `/demo/reviewer-path` |
| GET | `/demo/sample-outputs` |
| GET | `/demo/sample-output/{sample_id}` |
| GET | `/demo/portfolio-summary` |

## Diagnostics (v3.2)

| Method | Path |
|---|---|
| GET | `/diagnostics/health` |
| GET | `/diagnostics/integrity` |
| GET | `/diagnostics/schema-validation` |
| GET | `/diagnostics/project-status` |

## Reasoning (v4.0)

| Method | Path |
|---|---|
| POST | `/reasoning/rule-match` |
| POST | `/reasoning/decision-path` |
| POST | `/reasoning/risk-score` |
| POST | `/reasoning/evidence-chain` |
| POST | `/reasoning/reasoned-answer` |
| POST | `/reasoning/policy-explanation` |

## Hybrid Retrieval (v4.5)

| Method | Path |
|---|---|
| POST | `/retrieval/hybrid-search` |
| POST | `/retrieval/compare` |
| POST | `/retrieval/grounding-report` |
| GET | `/retrieval/evaluation` |
| GET | `/retrieval/conflicts` |
| GET | `/retrieval/source-trust` |

## Agent Hub (v5.0)

| Method | Path |
|---|---|
| GET | `/agent-hub/status` |
| POST | `/agent-hub/context` |
| POST | `/agent-hub/orchestrate` |
| GET | `/agent-hub/skill-evidence` |
| GET | `/agent-hub/missing-evidence` |
| GET | `/agent-hub/portfolio-readiness` |
| GET | `/agent-hub/cross-project-report` |
| GET | `/agent-hub/maturity` |
| GET | `/agent-hub/next-actions` |
| GET | `/agent-hub/v5-release-report` |

## Other

| Method | Path |
|---|---|
| GET | `/api/surface` |
