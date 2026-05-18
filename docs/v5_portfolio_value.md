# v5.0 — Portfolio Value

## What this project demonstrates

1. **Architectural maturity** — clear layering (data → domain → reasoning →
   retrieval → agent hub → API → frontend).
2. **Determinism** — every output is rule-based and deterministic; CI is
   reliable across runs.
3. **Safety-by-construction** — backend imports are restricted; tests
   enforce the boundary; uniform error envelope; uniform safety footer.
4. **Cross-project thinking** — D is not just a knowledge base; it is the
   control plane that ties A/B/C/D together via skills, projects, and
   routing rules.
5. **Reviewer empathy** — Reviewer Mode, sample outputs, portfolio summary,
   12-step quick path, and bilingual safety banner so a reviewer with no
   prior context can evaluate the project in under 20 minutes.
6. **Portfolio readiness scoring** — quantitative readiness across 10
   categories, plus a 5-level maturity model.
7. **Hybrid retrieval** — model-free, embedding-free, but more than just
   BM25 thanks to chunking, synonym expansion, source trust, and
   faithfulness scoring.
8. **Engineering hygiene** — JSON schemas, integrity checks, diagnostics
   reports, 720+ tests with no skips.

## Why model-free now

LLM connectors are reserved for v6.0. Until then, the project's value
comes from clarity, determinism, and provable boundaries. Reviewers can
inspect the rules, replay the same answer twice, and verify that no
external service is contacted.
