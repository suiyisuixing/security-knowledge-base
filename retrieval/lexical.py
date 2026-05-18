"""Lexical scoring for chunks (v4.5)."""

from __future__ import annotations

import math
from collections import Counter
from typing import Any

from app import retrieval as legacy_retrieval


def bm25_like_score(query: str, chunk: dict[str, Any]) -> float:
    q_tokens = legacy_retrieval.tokenize(query)
    if not q_tokens:
        return 0.0
    body = chunk.get("text", "")
    d_tokens = legacy_retrieval.tokenize(body)
    if not d_tokens:
        return 0.0
    counts = Counter(d_tokens)
    d_len = max(len(d_tokens), 1)
    score = 0.0
    for term in q_tokens:
        tf = counts.get(term, 0)
        if tf == 0:
            continue
        score += (tf * 2.2) / (tf + 1.2 * (0.25 + 0.75 * (d_len / 200)))
    return score


def keyword_overlap_score(query: str, chunk: dict[str, Any]) -> float:
    q_tokens = set(legacy_retrieval.tokenize(query))
    d_tokens = set(legacy_retrieval.tokenize(chunk.get("text", "")))
    if not q_tokens or not d_tokens:
        return 0.0
    overlap = len(q_tokens & d_tokens)
    return overlap / math.sqrt(len(q_tokens) * len(d_tokens))


def tag_match_score(query: str, chunk: dict[str, Any]) -> float:
    q = (query or "").lower()
    tags = [str(t).lower() for t in chunk.get("tags", []) or []]
    if not tags:
        return 0.0
    matches = sum(1 for t in tags if t in q)
    return float(matches)


def domain_match_score(query: str, chunk: dict[str, Any]) -> float:
    q = (query or "").lower()
    domain = (chunk.get("domain") or "").lower()
    if not domain:
        return 0.0
    return 1.0 if domain.replace("_", " ") in q else 0.0
