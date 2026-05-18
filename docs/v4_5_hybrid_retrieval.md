# v4.5 — Hybrid Retrieval

## Goal

Upgrade the v3.0 BM25-like retrieval to a *hybrid* approach without
introducing embeddings, vector DBs, or external API calls. Add citation
grounding, faithfulness scoring, source trust, and knowledge-conflict
detection.

## What was added

`retrieval/` package (`chunker`, `lexical`, `semantic_light`, `hybrid`,
`source_trust`, `citation_grounding`, `faithfulness`, `knowledge_conflict`,
`retrieval_eval`).

A bundled security-term synonym map (`data/security_synonyms.json`) and
10 evaluation cases (`data/retrieval_eval_cases.json`).

## How hybrid scoring works

For each chunk:

```
combined = 0.55 * lexical + 0.25 * semantic + 0.10 * trust + 0.10 * quality
```

- `lexical` = BM25-like + tag-match + domain-match.
- `semantic` = synonym-expanded concept overlap + tag-related-skill score.
- `trust` = safety + domain-relevance + freshness (per source doc).
- `quality` = placeholder constant (legacy `knowledge_quality` already
  produces a deeper per-doc score).

## API additions

- `POST /retrieval/hybrid-search`
- `POST /retrieval/compare`
- `POST /retrieval/grounding-report`
- `GET /retrieval/evaluation`
- `GET /retrieval/conflicts`
- `GET /retrieval/source-trust`

## Boundary

Still no embeddings. No vector DB. No external API. Synonyms are bundled
JSON. All scoring is deterministic.
