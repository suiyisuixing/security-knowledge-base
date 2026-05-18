# Retrieval Model

## Algorithm

The retrieval module implements a BM25-like TF-IDF scorer in plain Python.

- Tokenization removes short tokens and a small stop-word list.
- Document text is the concatenation of title, domain, tags, related skills,
  and body.
- IDF is computed per document set (optionally filtered by domain).
- The score uses a BM25-style saturation term to dampen high term frequencies.

## Filters

- `domain` filters to a single knowledge domain.
- `search_by_tags` ranks documents by tag overlap.

## Snippets

The snippet around the first query-term match is returned to the client (or a
prefix when no token matches).

## Why no vector store

The project is intentionally self-contained: no external services, no model
downloads, no embeddings. TF-IDF is sufficient for the small curated corpus
and keeps the surface easy to audit.
