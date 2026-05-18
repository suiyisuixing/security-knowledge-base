# v5.0 — Architecture

```
+--------------------------+
|        Frontend          |  React + Vite (cards/tables/badges only)
+-----------+--------------+
            |
            | HTTP (CORS to localhost)
            |
+-----------v--------------+
|   FastAPI (main.py)      |
|  68+ endpoints           |
+---+--------+-------+-----+
    |        |       |
    |        |       +---> reasoning/   (rule engine, decision tree, risk,
    |        |              evidence, templates, workflow, explanation)
    |        |
    |        +---> retrieval/   (chunker, lexical, semantic-light,
    |                           hybrid, citation grounding, faithfulness,
    |                           source trust, conflict, eval)
    |
    +---> agent_hub/  (project adapter, cross-project context,
                       skill evidence, portfolio readiness,
                       orchestrator, next-action, maturity, roadmap)

+---v---------------+    +---v----------------+    +---v----------------+
| knowledge/ *.md   |    | data/ *.json       |    | memory/ *.json     |
| 32 docs, 6        |    | safety, skills,    |    | learning profile,  |
| domains, YAML     |    | benchmark, schema  |    | skill progress,    |
| front matter      |    | maturity, etc.     |    | completed labs     |
+-------------------+    +--------------------+    +--------------------+

All arrows are LOCAL. No network. No LLM. No subprocess in backend.
```

## Layering

1. **Data** — JSON + Markdown bundled in the repo.
2. **Domain modules** — knowledge_loader, retrieval, safety_policy, …
3. **Reasoning** — `reasoning/` rule engine + decision tree.
4. **Hybrid retrieval** — `retrieval/` chunker + scoring + grounding.
5. **Agent hub** — `agent_hub/` cross-project orchestration.
6. **Service wrappers** — `backend/app/reasoning_service.py`,
   `hybrid_retrieval_service.py`, `agent_hub_service.py`.
7. **API** — `backend/app/main.py` exposes uniform endpoints.
8. **Frontend** — React panels consume the API.

## Determinism

Every module is rule-based and deterministic for a fixed input. CI re-runs
the same `pytest` suite (520+ tests) and gets the same result every time.
