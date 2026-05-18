# API Surface

| Method | Path | Summary |
|---|---|---|
| GET  | / | Project metadata |
| GET  | /health | Liveness check |
| GET  | /knowledge/domains | List knowledge domains |
| GET  | /knowledge/docs | List knowledge documents (optional `?domain=`) |
| GET  | /knowledge/docs/{doc_id} | Get a knowledge document |
| POST | /knowledge/search | Search the knowledge base |
| POST | /knowledge/ask | Grounded answer with citations |
| POST | /safety/classify | Classify a request against the policy |
| GET  | /safety/policy | Return loaded policy |
| GET  | /safety/evaluation | Run safety evaluation |
| POST | /safety/evaluate | Run safety evaluation |
| GET  | /memory/profile | Load agent memory profile |
| POST | /memory/update-skill | Update skill progress |
| GET  | /memory/skill-progress | List skill progress |
| GET  | /memory/audit | Read recent audit events |
| GET  | /projects | List portfolio projects |
| GET  | /projects/{project_id} | Get a portfolio project |
| GET  | /skills | List skills |
| GET  | /skills/{skill_id} | Get a skill |
| POST | /skills/recommend | Recommend skills for a goal |
| POST | /learning-path/generate | Generate a learning path |
| POST | /context/build | Build agent context for a query |
| GET  | /quality/knowledge | Score all knowledge documents |
| GET  | /quality/knowledge/{doc_id} | Score a single document |
| POST | /quality/citations/evaluate | Evaluate citation quality |
| GET  | /reasoning/templates | List reasoning templates |
| GET  | /reasoning/templates/{template_id} | Get a reasoning template |
| POST | /workflow/authorized-plan | Plan an authorized workflow |
| POST | /router/route-task | Route a task to a portfolio project |
| GET  | /benchmark/tasks | List benchmark tasks |
| POST | /benchmark/run | Run all benchmark tasks |
| GET  | /benchmark/export-jsonl | Export benchmark tasks as JSONL |
| POST | /report/knowledge-coverage | Knowledge coverage report |
| POST | /report/safety-policy | Safety policy report |
| POST | /report/agent-readiness | Agent readiness report |
| GET  | /evaluation/scenarios | List evaluation scenarios |
| POST | /evaluation/run | Run evaluation scenarios |
| GET  | /api/surface | Inventory of API endpoints |
