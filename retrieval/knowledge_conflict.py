"""Knowledge conflict / duplication / staleness detection (v4.5)."""

from __future__ import annotations

import hashlib
from typing import Any

from app import knowledge_loader


def _hash(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def detect_duplicate_documents(docs: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    docs = docs or knowledge_loader.get_index()["documents"]
    seen: dict[str, list[str]] = {}
    for d in docs:
        body = d.get("body", "")[:800]
        h = _hash(body)
        seen.setdefault(h, []).append(d["metadata"]["id"])
    return [{"hash": h, "doc_ids": ids} for h, ids in seen.items() if len(ids) > 1]


def detect_stale_documents(docs: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    docs = docs or knowledge_loader.get_index()["documents"]
    issues: list[dict[str, Any]] = []
    for d in docs:
        body = d.get("body", "")
        if len(body) < 200:
            issues.append({"doc_id": d["metadata"]["id"], "reason": "body too short (<200 chars)"})
    return issues


def detect_conflicting_guidance(docs: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    docs = docs or knowledge_loader.get_index()["documents"]
    pairs: list[dict[str, Any]] = []
    safe_only = []
    forbidden_only = []
    for d in docs:
        meta = d.get("metadata", {})
        safe = set(meta.get("safe_use", []) or [])
        forbidden = set(meta.get("forbidden_use", []) or [])
        if safe and not forbidden:
            safe_only.append(meta["id"])
        elif forbidden and not safe:
            forbidden_only.append(meta["id"])
    return pairs


def detect_policy_conflicts(docs: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    docs = docs or knowledge_loader.get_index()["documents"]
    issues: list[dict[str, Any]] = []
    for d in docs:
        meta = d.get("metadata", {})
        safe = set(meta.get("safe_use", []) or [])
        forbidden = set(meta.get("forbidden_use", []) or [])
        overlap = safe & forbidden
        if overlap:
            issues.append({"doc_id": meta["id"], "overlap": sorted(overlap)})
    return issues


def build_conflict_report() -> dict[str, Any]:
    return {
        "duplicates": detect_duplicate_documents(),
        "stale": detect_stale_documents(),
        "conflicts": detect_conflicting_guidance(),
        "policy_conflicts": detect_policy_conflicts(),
    }
