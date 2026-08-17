# Architecture

## Layout

```
backend/app/        FastAPI service (32 modules)
knowledge/          Markdown knowledge base (6 domains, 32 docs)
data/               Policy / taxonomy / registry / benchmark / templates JSON
memory/             Agent memory JSON
frontend/           React + Vite dashboard
tests/              pytest suite (69 files)
docs/               Architecture, threat model, safety policy, etc.
reports/            SECURITY_REPORT.md
tools/              Local-development check runner
.github/workflows/  CI
```

## Request flow (knowledge ask)

1. Client `POST /knowledge/ask {query}`
2. `safety_policy.classify_request` evaluates intent.
3. `audit.log_event` records the decision with sensitive patterns redacted.
4. `retrieval.search_knowledge` ranks knowledge documents.
5. `answer_builder.build_grounded_answer` assembles answer + citations + safety note.
6. Response returned with `citations`, `safety_note`, `related_skills`, `related_projects`.

## Request flow (authorized workflow planning)

1. Client `POST /workflow/authorized-plan {request}`
2. `authorized_workflow.validate_scope` checks for local lab / self-asset / authorized scope.
3. If in scope → planning artifact returned; if not → blocked with safe redirect.

## Cross-project relationships

```
        [security-knowledge-base]  ← knowledge + safety + memory + routing
              /        |       \
   [llm-sec-lab]  [log-ai]  [vuln-intel]
```

Each downstream project can consume this project's knowledge documents,
safety classifications, and routing decisions.
