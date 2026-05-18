# v5.0 — Reviewer Guide

Estimated time: 15–20 minutes.

## 1. Read the value summary

Open the frontend (or `GET /demo/portfolio-summary`). The first three
cards establish:

- What the project does.
- What it does *not* do (model-free, no real scanning).
- How D relates to A / B / C.

## 2. Walk the 12-step Reviewer Quick Path

`GET /demo/reviewer-path` returns the full path. The same path is rendered
in the *Reviewer Mode* panel of the frontend. Each step lists the exact
endpoint used.

## 3. Look at sample outputs without running the pipeline

`GET /demo/sample-outputs` lists pre-generated samples. Click any chip in
the frontend to load the JSON shape.

## 4. Run live calls

The 12-step path drives:

- Knowledge search (legacy and hybrid).
- Knowledge-grounded answer with citations.
- Safety classification for allowed / needs-confirmation / blocked.
- Learning path generation.
- Authorized workflow planning.
- Task routing → A / B / C / D.
- Benchmark run (60 tasks).
- Agent readiness report.

## 5. Verify boundaries

`GET /diagnostics/integrity` confirms:

- No forbidden imports (`requests`, `urllib.request`, `subprocess`).
- No external API URLs.
- No real scanning-tool strings.
- No model-integration patterns.
- All required files present.

## 6. Verify schemas

`GET /diagnostics/schema-validation` validates the knowledge metadata,
safety policy, skill taxonomy, project registry, benchmark tasks, and
memory profile against bundled JSON-schema-like definitions.

## 7. Verify agent hub

`GET /agent-hub/portfolio-readiness` produces a single 0..1 overall score
across 10 categories. `GET /agent-hub/maturity` and `GET /agent-hub/cross-project-report`
show how the four projects are connected.

## 8. Build report

`GET /agent-hub/v5-release-report` returns the roadmap, release checklist,
and v5→v6 plan.

## 9. (Optional) Run tests

`pytest` — 720+ tests, all pass, no skips, no xfails.
