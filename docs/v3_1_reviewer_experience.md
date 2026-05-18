# v3.1 — Reviewer Experience

## Goal

Make the project easy to evaluate in under 20 minutes:

- A documented Reviewer Quick Path.
- Pre-generated sample outputs that show the shape of every important API.
- A bundled portfolio summary explaining cross-project value.
- A `Reviewer Mode` UI panel that loads samples without running the live pipeline.

## What was added

- `sample_outputs/` with six subdirectories:
  - `api_responses/`, `reports/`, `benchmark/`, `agent_readiness/`,
    `router_examples/`, `authorized_workflows/`.
- `backend/app/demo_assets.py` — `list_demo_samples()`, `get_demo_sample()`,
  `build_reviewer_path()`, `build_portfolio_demo_summary()`,
  `validate_sample_outputs()`.
- API endpoints: `/demo/reviewer-path`, `/demo/sample-outputs`,
  `/demo/sample-output/{sample_id}`, `/demo/portfolio-summary`.
- Frontend `Reviewer Mode` panel that loads sample outputs.

## Boundaries

All sample outputs are local JSON. No external API call is performed; no real
target is referenced. Reviewer Mode is read-only.
