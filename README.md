# Security Knowledge Base & Agent Memory Lab

![CI](https://github.com/suiyisuixing/security-knowledge-base/actions/workflows/ci.yml/badge.svg)

A model-free, local cybersecurity knowledge base with rule-based
reasoning, hybrid retrieval, and a rule-based agent hub — built as a
learning project.

The system does not support unauthorized scanning or exploitation. It supports
local labs, self-owned assets, and explicitly authorized reconnaissance
planning, low-risk security check planning, and safe verification workflows.

> This is a local-only, model-free, defensive, authorized-scope portfolio
> project. It does not use LLMs, perform real scanning, or execute
> exploitation.

---

## How the project is organized

The system grew in stages, each adding one inspectable subsystem:

| Component | What it does |
|---|---|
| Reviewer experience | `sample_outputs/`, `/demo/*` API, Reviewer Mode UI |
| Stability / schema | `schemas/`, schema validator, integrity checker, error model, `/diagnostics/*` |
| Rule-based reasoning | `reasoning/` package, decision tree, risk scoring, evidence chain, `/reasoning/*` |
| Hybrid retrieval | `retrieval/` package (chunk + lexical + semantic-light + grounding + faithfulness + source trust), `/retrieval/*` |
| Agent hub | `agent_hub/` package, skill evidence, portfolio readiness, maturity model, orchestrator, `/agent-hub/*` |

Every component is **model-free**: no LLM connector, no `llm/` directory,
no `model_config.json`. An optional local-model connector is a possible
future direction, deliberately out of scope here.

---

## Reviewer Quick Path (12 steps)

1. Load knowledge domains (`GET /knowledge/domains`).
2. Search for a security concept (`POST /knowledge/search`).
3. Ask a knowledge-grounded question (`POST /knowledge/ask`).
4. Classify an *allowed* request (`POST /safety/classify`).
5. Classify a *needs-confirmation* request (`POST /safety/classify`).
6. Classify a *blocked* request (`POST /safety/classify`).
7. Generate a learning path (`POST /learning-path/generate`).
8. Build an authorized workflow plan (`POST /workflow/authorized-plan`).
9. Route a task to A/B/C/D (`POST /router/route-task`).
10. Run the agent benchmark (`POST /benchmark/run`).
11. Generate the agent readiness report (`POST /report/agent-readiness`).
12. Review portfolio value summary (`GET /demo/portfolio-summary`).

Sample outputs for every step are bundled under `sample_outputs/` and
exposed at `GET /demo/sample-outputs`.

---

## Features

- 32 local Markdown knowledge documents across 6 domains
- YAML front matter with `safe_use` / `forbidden_use` per document
- BM25-like TF-IDF retrieval (no external libraries, no vector DB)
- Knowledge-grounded answer builder with citations and safety notes
- 19-class safety policy classifier (allowed / needs confirmation / blocked)
- Agent memory store (learning profile, skill progress, completed labs)
- Skill taxonomy with 16 skills mapped to four portfolio projects
- Learning-path generator for AI security, detection, vuln intel, and code review
- Authorized workflow planner (local lab, self-owned asset, authorized scope)
- Task router across the four portfolio projects
- Vulnerability reasoning templates (BOLA, dependency, RAG, log, recon, plan)
- 60 benchmark tasks across six categories
- Knowledge quality scoring and citation evaluation
- Reports: knowledge coverage, safety policy, agent readiness
- React + Vite frontend dashboard with card / table / pre-block layout
- 721 pytest tests, GitHub Actions CI

## Model-free architecture

- `reasoning/` — rule engine, decision tree, policy reasoner, risk scoring,
  evidence builder, template renderer, workflow reasoner, explanation builder.
- `retrieval/` — chunker, lexical scoring, light-weight semantic-style
  expansion, hybrid scoring, source trust, citation grounding, faithfulness,
  knowledge conflict, retrieval evaluation.
- `agent_hub/` — project adapter, cross-project context, skill evidence
  tracker, portfolio readiness, agent orchestrator, next-action planner,
  cross-project report, 5-level maturity model, roadmap planner.
- `schemas/` — JSON-schema-like definitions for knowledge metadata,
  safety policy, skill taxonomy, project registry, benchmark tasks,
  memory profile, skill progress, and agent readiness.
- `sample_outputs/` — bundled JSON snapshots for every important API
  surface so reviewers can see the shape without running the pipeline.

---

## Relationship to A/B/C/D

| Project | Focus | Repo |
|---|---|---|
| llm-security-lab | AI / RAG Security Evaluation | https://github.com/suiyisuixing/llm-security-lab |
| security-log-ai-assistant | Detection Engineering / SOC | https://github.com/suiyisuixing/security-log-ai-assistant |
| vulnerability-intelligence-lab | Vulnerability Intelligence / Skill Dataset | https://github.com/suiyisuixing/vulnerability-intelligence-lab |
| **security-knowledge-base** | **Knowledge, Safety, Agent Memory, Routing** | https://github.com/suiyisuixing/security-knowledge-base |

This project (D) is the knowledge, safety policy, agent memory, and task
routing layer for the rest of the portfolio.

---

## Architecture

- `backend/app/` — FastAPI service (32 modules)
- `knowledge/` — Local Markdown knowledge base with YAML metadata
- `data/` — Safety policy, skill taxonomy, project registry, benchmark, templates
- `memory/` — Agent memory (JSON files, no sensitive data)
- `frontend/` — React + Vite dashboard
- `tests/` — pytest suite (721 tests, 69 files)
- `docs/` — Architecture, threat model, safety policy, reviewer guide, etc.
- `reports/` — Security report
- `tools/` — Local-development check runner
- `.github/workflows/ci.yml` — Backend tests + frontend build

---

## Quick Start

> Commands below use `%REPO%` for the directory you cloned into. Set it once
> per shell: `set REPO=%CD%` from the repository root (PowerShell:
> `$env:REPO=$PWD`).

### Create virtual environment

```cmd
cd /d %REPO%
py -3.11 -m venv .venv
```

### Install backend dependencies

```cmd
%REPO%\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

### Run backend

```cmd
cd /d %REPO%\backend
%REPO%\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### Install frontend

```cmd
cd /d %REPO%\frontend
npm install --registry=https://registry.npmmirror.com
```

### Run frontend

```cmd
npm run dev
```

### Run tests

```cmd
cd /d %REPO%
%REPO%\.venv\Scripts\python.exe -m pytest
```

### Build frontend

```cmd
cd /d %REPO%\frontend
npm run build
```

### Local check

```cmd
cd /d %REPO%
%REPO%\.venv\Scripts\python.exe tools\run_checks.py
```

---

## Knowledge Model

Each document is a Markdown file with YAML front matter:

```yaml
---
id: api-bola-001
title: Broken Object Level Authorization
domain: api_security
difficulty: medium
related_projects: [vulnerability-intelligence-lab]
related_skills: [api_authorization_reasoning, safe_verification_planning]
tags: [OWASP API, BOLA, IDOR]
safe_use: [local_lab, authorized_testing, defensive_learning]
forbidden_use: [unauthorized_scanning, credential_theft, exploit_weaponization]
---
```

Body sections: Concept · Why it matters · Common indicators · Safe local example
· Defensive verification approach · Remediation guidance · Safety boundary ·
Related project connection.

## Retrieval Model

Local BM25-like TF-IDF over title, domain, tags, skills, and body. Tokenization
strips short tokens and stop words. No vector store, no external service.

## Safety Policy Model

19 classes split into allowed / needs confirmation / blocked, with keyword-based
classification. Every request is logged through the audit layer with sensitive
patterns redacted before write.

## Agent Memory Model

JSON files under `memory/`. Stores learning profile, skill progress, completed
labs. Never stores tokens, passwords, real targets, or third-party data.

## Task Routing

Keyword router maps a query to project + knowledge domain + skill. Defaults to
`security-knowledge-base` when no specific project matches.

## Authorized Workflow Planning

`POST /workflow/authorized-plan` returns a planning artifact only. Execution is
the responsibility of the authorized human. Public scans without authorization
are blocked with a redirect to local lab or authorized assessment guidance.

## Benchmark

60 tasks across knowledge QA, safety classification, vulnerability reasoning,
safe verification planning, remediation reasoning, and task routing. Run via
`POST /benchmark/run` or `python tools/run_checks.py` (indirectly via tests).

## Reports

- `POST /report/knowledge-coverage`
- `POST /report/safety-policy`
- `POST /report/agent-readiness`

Each report is also available as Markdown via the `markdown` field.

## Testing

- 721 pytest tests in 69 files
- Backend modules, retrieval, safety, memory, router, benchmark, API surface
- Security boundary tests assert no `requests`, `subprocess`, or `shell=True`
  inside `backend/app`, no real API keys, no real target domains, no attack
  command strings.

## Security Boundaries

- No execution of real scans
- No real LLM API calls
- No real external API integrations (NVD, CISA, EPSS, GitHub Advisory, OSV)
- No connection to real targets
- No credential attacks, weaponized exploits, persistence, evasion,
  exfiltration, destructive actions, or malware

## Development Note

This project was developed as an AI-assisted learning and engineering project.
The architecture, security knowledge model, safety policy design, testing
goals, validation process, and final review were directed by the author. AI
tools were used for planning, documentation support, debugging guidance, and
review assistance, while all repository commits and project decisions were
managed by the author.

## Limitations

- Local-only; no production deployment is intended.
- Retrieval uses simple TF-IDF; semantic search is intentionally out of scope.
- Memory and reports are educational; treat as illustrative.

## Portfolio Usage

Use this project as the knowledge, safety, and routing layer when reviewing
the rest of the portfolio. Start at the Reviewer Quick Path above and follow
the 12 steps in order.
