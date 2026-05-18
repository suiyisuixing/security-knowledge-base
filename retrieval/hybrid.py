"""Hybrid retrieval — combines lexical + semantic-light + trust + quality."""

from __future__ import annotations

from typing import Any

from app import knowledge_loader
from . import chunker
from . import lexical
from . import semantic_light
from . import source_trust


def _all_chunks(domain: str | None = None) -> list[dict[str, Any]]:
    docs = knowledge_loader.get_index()["documents"]
    if domain:
        docs = [d for d in docs if d["metadata"].get("domain") == domain]
    return chunker.chunk_all_documents(docs)


def combine_scores(lex: float, sem: float, trust: float, quality: float) -> float:
    return 0.55 * lex + 0.25 * sem + 0.1 * trust + 0.1 * quality


def hybrid_search(query: str, domain: str | None = None, top_k: int = 8) -> list[dict[str, Any]]:
    if not (query or "").strip():
        return []
    chunks = _all_chunks(domain)
    scored: list[dict[str, Any]] = []
    for c in chunks:
        lex = lexical.bm25_like_score(query, c) + 0.5 * lexical.tag_match_score(query, c) + 0.5 * lexical.domain_match_score(query, c)
        sem = semantic_light.concept_overlap_score(query, c) + semantic_light.related_skill_score(query, c)
        if lex == 0 and sem == 0:
            continue
        doc = knowledge_loader.get_document_by_id(c["doc_id"]) or {}
        trust = source_trust.score_source_trust(doc)
        quality = 0.5  # placeholder constant — knowledge_quality handles the deep score
        combined = combine_scores(lex, sem, trust, quality)
        scored.append({
            "chunk_id": c["chunk_id"],
            "doc_id": c["doc_id"],
            "title": c.get("title"),
            "domain": c.get("domain"),
            "snippet": c["text"][:240],
            "score": round(combined, 4),
            "components": {
                "lexical": round(lex, 4),
                "semantic": round(sem, 4),
                "trust": round(trust, 4),
                "quality": round(quality, 4),
            },
        })
    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored[: max(1, top_k)]


def rerank_results(query: str, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(results, key=lambda r: r.get("score", 0.0), reverse=True)


def explain_hybrid_score(result: dict[str, Any]) -> str:
    comps = result.get("components", {})
    return (
        f"score={result.get('score', 0.0)} "
        f"lex={comps.get('lexical', 0)} sem={comps.get('semantic', 0)} "
        f"trust={comps.get('trust', 0)} quality={comps.get('quality', 0)}"
    )


def compare_legacy_and_hybrid(query: str) -> dict[str, Any]:
    from app import retrieval as legacy
    legacy_results = legacy.search_knowledge(query, top_k=5)
    hybrid_results = hybrid_search(query, top_k=5)
    legacy_ids = [r["doc_id"] for r in legacy_results]
    hybrid_ids = [r["doc_id"] for r in hybrid_results]
    overlap = len(set(legacy_ids) & set(hybrid_ids))
    return {
        "query": query,
        "legacy": legacy_results,
        "hybrid": hybrid_results,
        "overlap_count": overlap,
        "legacy_only": [d for d in legacy_ids if d not in hybrid_ids],
        "hybrid_only": [d for d in hybrid_ids if d not in legacy_ids],
    }
