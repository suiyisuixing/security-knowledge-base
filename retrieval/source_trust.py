"""Source trust scoring (v4.5)."""

from __future__ import annotations

from typing import Any


def score_source_safety(doc: dict[str, Any]) -> float:
    meta = doc.get("metadata", {}) if doc else {}
    safe = list(meta.get("safe_use", []) or [])
    forbidden = list(meta.get("forbidden_use", []) or [])
    if not safe and not forbidden:
        return 0.3
    score = 0.5 + 0.05 * len(safe) + 0.05 * len(forbidden)
    return min(score, 1.0)


def score_source_domain_relevance(doc: dict[str, Any]) -> float:
    meta = doc.get("metadata", {}) if doc else {}
    domain = (meta.get("domain") or "").strip()
    if not domain:
        return 0.2
    return 0.8


def score_source_freshness(doc: dict[str, Any]) -> float:
    # Bundled local docs are managed in-tree; treat as 'fresh enough'.
    return 0.75


def score_source_trust(doc: dict[str, Any]) -> float:
    if not doc:
        return 0.0
    safety = score_source_safety(doc)
    domain = score_source_domain_relevance(doc)
    fresh = score_source_freshness(doc)
    return round(0.45 * safety + 0.35 * domain + 0.2 * fresh, 4)


def build_source_trust_report(docs: list[dict[str, Any]]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for d in docs:
        items.append({
            "doc_id": d["metadata"]["id"],
            "title": d["metadata"].get("title", ""),
            "domain": d["metadata"].get("domain", ""),
            "safety": score_source_safety(d),
            "domain_relevance": score_source_domain_relevance(d),
            "freshness": score_source_freshness(d),
            "trust": score_source_trust(d),
        })
    return {"count": len(items), "items": items}
