"""Local TF-IDF / BM25-like retrieval over the knowledge base.

No external retrieval or vector libraries are used.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from . import knowledge_loader

_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "to", "for", "on", "with",
    "is", "are", "be", "this", "that", "it", "as", "by", "at", "from", "how",
    "what", "do", "does", "i", "we", "you", "they", "them", "us", "my",
}

_TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    if not text:
        return []
    tokens = [t.lower() for t in _TOKEN_RE.findall(text)]
    return [t for t in tokens if t not in _STOPWORDS and len(t) > 1]


def _doc_text(doc: dict[str, Any]) -> str:
    meta = doc.get("metadata", {})
    parts: list[str] = [
        meta.get("title", ""),
        meta.get("domain", ""),
        " ".join(meta.get("tags", []) or []),
        " ".join(meta.get("related_skills", []) or []),
        doc.get("body", ""),
    ]
    return " ".join(p for p in parts if p)


def compute_idf(docs: list[dict[str, Any]]) -> dict[str, float]:
    n = max(len(docs), 1)
    df: Counter[str] = Counter()
    for d in docs:
        unique_terms = set(tokenize(_doc_text(d)))
        for term in unique_terms:
            df[term] += 1
    return {term: math.log((n + 1) / (count + 1)) + 1.0 for term, count in df.items()}


def score_document(query: str, doc: dict[str, Any], idf: dict[str, float] | None = None) -> float:
    q_tokens = tokenize(query)
    if not q_tokens:
        return 0.0
    d_tokens = tokenize(_doc_text(doc))
    if not d_tokens:
        return 0.0
    d_counts = Counter(d_tokens)
    d_len = max(len(d_tokens), 1)
    if idf is None:
        idf = {}
    score = 0.0
    for term in q_tokens:
        tf = d_counts.get(term, 0)
        if tf == 0:
            continue
        weight = idf.get(term, 1.0)
        # BM25-like saturation
        score += weight * ((tf * 2.2) / (tf + 1.2 * (0.25 + 0.75 * (d_len / 200))))
    return score


def _snippet(body: str, query: str, length: int = 240) -> str:
    body = (body or "").strip()
    q_tokens = tokenize(query)
    lowered = body.lower()
    for term in q_tokens:
        idx = lowered.find(term)
        if idx != -1:
            start = max(0, idx - 60)
            end = min(len(body), start + length)
            snippet = body[start:end].strip()
            return snippet
    return body[:length].strip()


def _all_docs() -> list[dict[str, Any]]:
    return knowledge_loader.get_index()["documents"]


def search_knowledge(query: str, domain: str | None = None, top_k: int = 5) -> list[dict[str, Any]]:
    docs = _all_docs()
    if domain:
        docs = [d for d in docs if d["metadata"].get("domain") == domain]
    if not docs:
        return []
    idf = compute_idf(docs)
    scored = []
    for d in docs:
        s = score_document(query, d, idf)
        if s > 0:
            scored.append((s, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for score, d in scored[: max(1, top_k)]:
        meta = d["metadata"]
        results.append({
            "doc_id": meta["id"],
            "title": meta["title"],
            "domain": meta["domain"],
            "score": round(float(score), 4),
            "snippet": _snippet(d["body"], query),
        })
    return results


def search_by_tags(tags: list[str], top_k: int = 5) -> list[dict[str, Any]]:
    tag_set = {t.lower() for t in (tags or [])}
    if not tag_set:
        return []
    docs = _all_docs()
    matches = []
    for d in docs:
        meta = d["metadata"]
        doc_tags = {str(t).lower() for t in (meta.get("tags", []) or [])}
        overlap = len(tag_set & doc_tags)
        if overlap > 0:
            matches.append((overlap, d))
    matches.sort(key=lambda x: x[0], reverse=True)
    out = []
    for overlap, d in matches[: max(1, top_k)]:
        meta = d["metadata"]
        out.append({
            "doc_id": meta["id"],
            "title": meta["title"],
            "domain": meta["domain"],
            "score": float(overlap),
            "snippet": _snippet(d["body"], " ".join(tags)),
        })
    return out


def explain_search(query: str, results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "query": query,
        "result_count": len(results),
        "tokens": tokenize(query),
        "top_doc_ids": [r["doc_id"] for r in results],
    }
