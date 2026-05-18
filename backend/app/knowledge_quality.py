"""Knowledge quality scoring."""

from __future__ import annotations

from typing import Any

from . import knowledge_loader


def score_document_quality(doc: dict[str, Any]) -> dict[str, Any]:
    meta = doc.get("metadata", {})
    body = doc.get("body", "") or ""
    components: dict[str, float] = {}
    components["metadata_completeness"] = 1.0 if all(
        meta.get(k) for k in ("id", "title", "domain", "difficulty")
    ) else 0.6
    components["domain_clarity"] = 1.0 if meta.get("domain") else 0.0
    components["related_skills"] = 1.0 if meta.get("related_skills") else 0.0
    components["safe_use_forbidden_use"] = 1.0 if (meta.get("safe_use") and meta.get("forbidden_use")) else 0.0
    components["remediation_guidance"] = 1.0 if "remediation" in body.lower() else 0.5
    components["citation_readiness"] = 1.0 if "safety boundary" in body.lower() else 0.5
    total = sum(components.values()) / len(components)
    return {
        "doc_id": meta.get("id"),
        "score": round(total, 4),
        "components": {k: round(v, 4) for k, v in components.items()},
    }


def score_all_documents() -> list[dict[str, Any]]:
    return [score_document_quality(d) for d in knowledge_loader.get_index()["documents"]]


def summarize_quality_scores(results: list[dict[str, Any]]) -> dict[str, Any]:
    if not results:
        return {"count": 0, "average": 0.0}
    total = sum(r["score"] for r in results)
    return {
        "count": len(results),
        "average": round(total / len(results), 4),
        "min": round(min(r["score"] for r in results), 4),
        "max": round(max(r["score"] for r in results), 4),
    }
