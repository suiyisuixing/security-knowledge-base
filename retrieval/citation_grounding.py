"""Citation grounding (v4.5)."""

from __future__ import annotations

import re
from typing import Any

from app import retrieval as legacy_retrieval


def _tokens(text: str) -> set:
    return set(legacy_retrieval.tokenize(text))


def check_claim_supported_by_chunks(claim: str, chunks: list[dict[str, Any]]) -> dict[str, Any]:
    claim_tokens = _tokens(claim)
    if not claim_tokens:
        return {"supported": False, "support_chunks": [], "score": 0.0}
    best_score = 0.0
    support_chunks: list[str] = []
    for c in chunks:
        chunk_tokens = _tokens(c.get("text", "") or c.get("snippet", ""))
        overlap = len(claim_tokens & chunk_tokens)
        if not chunk_tokens:
            continue
        score = overlap / max(1, len(claim_tokens))
        if score >= 0.3:
            support_chunks.append(c.get("chunk_id") or c.get("doc_id"))
        if score > best_score:
            best_score = score
    return {
        "supported": bool(support_chunks),
        "support_chunks": support_chunks[:5],
        "score": round(best_score, 4),
    }


def build_grounded_citations(answer: str, retrieved_chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    citations: list[dict[str, Any]] = []
    for c in retrieved_chunks:
        doc_id = c.get("doc_id")
        if not doc_id or doc_id in seen:
            continue
        seen.add(doc_id)
        citations.append({
            "doc_id": doc_id,
            "chunk_id": c.get("chunk_id"),
            "title": c.get("title", ""),
            "domain": c.get("domain", ""),
        })
    return citations


def detect_uncited_claims(answer: str, chunks: list[dict[str, Any]]) -> list[str]:
    sentences = re.split(r"(?<=[\.!?])\s+", answer or "")
    uncited: list[str] = []
    for s in sentences:
        s = s.strip()
        if not s or len(s) < 12:
            continue
        if s.lower().startswith(("safety boundary", "based on")):
            continue
        if "[" in s and "]" in s:
            continue  # already references a doc_id
        support = check_claim_supported_by_chunks(s, chunks)
        if not support["supported"]:
            uncited.append(s)
    return uncited[:10]


def estimate_claim_support_score(answer: str, chunks: list[dict[str, Any]]) -> float:
    sentences = [s for s in re.split(r"(?<=[\.!?])\s+", answer or "") if len(s.strip()) > 8]
    if not sentences:
        return 0.0
    supported = 0
    for s in sentences:
        if check_claim_supported_by_chunks(s, chunks)["supported"]:
            supported += 1
    return round(supported / len(sentences), 4)


def build_grounding_report(answer: str, chunks: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "citations": build_grounded_citations(answer, chunks),
        "support_score": estimate_claim_support_score(answer, chunks),
        "uncited_claims": detect_uncited_claims(answer, chunks),
    }
