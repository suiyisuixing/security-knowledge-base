# retrieval/ — Hybrid retrieval layer (v4.5)

Model-free; no embeddings; no vector DB; no external API.

| Module | Purpose |
|---|---|
| `chunker.py` | Slice each document into overlapping char chunks. |
| `lexical.py` | BM25-like + keyword overlap + tag + domain match. |
| `semantic_light.py` | Synonym map + term normalisation for deterministic semantic-style boost. |
| `hybrid.py` | Combine lexical + semantic + trust + quality; compare against legacy. |
| `source_trust.py` | Safety / domain / freshness → trust score per source doc. |
| `citation_grounding.py` | Find supporting chunks for each claim, detect uncited claims. |
| `faithfulness.py` | Claim-level support score; hallucination-risk level. |
| `knowledge_conflict.py` | Duplicate / stale / policy-conflict detection. |
| `retrieval_eval.py` | Side-by-side legacy vs hybrid evaluation. |
