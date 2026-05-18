# Security Report — Security Knowledge Base & Agent Memory Lab

## What this project does

Provides a local, file-based cybersecurity knowledge base, a transparent
keyword-based safety policy classifier, an agent memory store, a task router
across four portfolio projects, vulnerability reasoning templates, an
authorized-workflow planner, and a small benchmark for evaluating agent
behavior.

## Knowledge model

Markdown documents under `knowledge/` carry YAML front matter with `id`,
`title`, `domain`, `difficulty`, `related_projects`, `related_skills`, `tags`,
`safe_use`, and `forbidden_use`. Each document follows an eight-section body
template (Concept, Why it matters, Common indicators, Safe local example,
Defensive verification, Remediation guidance, Safety boundary, Related
project).

## Retrieval model

Tokenizer + BM25-like TF-IDF scoring with stop-word removal. Optional domain
and tag filters. No vector store, no external services.

## Safety policy model

19 classes split into allowed / needs confirmation / blocked. Classification
uses ordered keyword lookups so that blocked intents are matched before
allow-list intents. Every decision can be audited via `logs/agent_audit.jsonl`.

## Agent memory

JSON files under `memory/` with learning profile, skill progress, completed
labs. No tokens, no passwords, no third-party data.

## Task routing

Keyword router that maps a query to project (A/B/C/D), knowledge domain, and
skill. Defaults to `security-knowledge-base` when no specific project matches.

## Authorized workflow planning

`POST /workflow/authorized-plan` returns planning artifacts only. Execution is
the responsibility of the authorized human. Public scans without
authorization are blocked with a redirect to local labs or authorized
assessment processes.

## Benchmark model

60+ tasks across six categories: knowledge QA, safety classification,
vulnerability reasoning, safe verification planning, remediation reasoning,
task routing. Each task has a deterministic expected output and a small rubric.

## Security boundaries

- No network calls in `backend/app/`.
- No `subprocess`, no `shell=True`, no `os.system`.
- No real API keys committed.
- No real third-party target hostnames or IPs.
- No attack-command strings (nmap, masscan, sqlmap, etc.).

## What this project does not do

- It does not execute scans.
- It does not call real LLM APIs.
- It does not integrate with real CVE / KEV / EPSS feeds.
- It does not support unauthorized testing.
- It is not a production system.

## Limitations

- TF-IDF retrieval has obvious limits for paraphrased queries.
- The classifier is keyword-based and may need additions for new phrasings.
- Memory is illustrative and not production-grade.

## Future improvements

- Multi-language knowledge documents.
- Plug-in reasoning templates per organization.
- Richer evaluation rubric scoring.

## AI-assisted development disclosure

This project was developed as an AI-assisted learning and engineering project.
The architecture, security knowledge model, safety policy design, testing
goals, validation process, and final review were directed by the author. AI
tools were used for planning, documentation support, debugging guidance, and
review assistance, while all repository commits and project decisions were
managed by the author.
