"""Retrieval evaluation: legacy vs hybrid (v4.5)."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from app import config
from app import retrieval as legacy_retrieval
from . import hybrid


@lru_cache(maxsize=1)
def load_retrieval_eval_cases() -> list[dict[str, Any]]:
    path = config.DATA_DIR / "retrieval_eval_cases.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get("cases", []))


def _doc_prefix_match(prefix: str, doc_id: str) -> bool:
    return doc_id.startswith(prefix)


def evaluate_legacy_retrieval() -> dict[str, Any]:
    cases = load_retrieval_eval_cases()
    if not cases:
        return {"total": 0, "passed": 0, "pass_rate": 0.0, "details": []}
    details = []
    passed = 0
    for c in cases:
        results = legacy_retrieval.search_knowledge(c["query"], top_k=5)
        prefix = c.get("expected_doc_id_prefix", "")
        hit = any(_doc_prefix_match(prefix, r["doc_id"]) for r in results)
        if hit:
            passed += 1
        details.append({"case_id": c["case_id"], "hit": hit, "top_ids": [r["doc_id"] for r in results]})
    return {"total": len(cases), "passed": passed, "pass_rate": round(passed / len(cases), 4), "details": details}


def evaluate_hybrid_retrieval() -> dict[str, Any]:
    cases = load_retrieval_eval_cases()
    if not cases:
        return {"total": 0, "passed": 0, "pass_rate": 0.0, "details": []}
    details = []
    passed = 0
    for c in cases:
        results = hybrid.hybrid_search(c["query"], top_k=5)
        prefix = c.get("expected_doc_id_prefix", "")
        hit = any(_doc_prefix_match(prefix, r["doc_id"]) for r in results)
        if hit:
            passed += 1
        details.append({"case_id": c["case_id"], "hit": hit, "top_ids": [r["doc_id"] for r in results]})
    return {"total": len(cases), "passed": passed, "pass_rate": round(passed / len(cases), 4), "details": details}


def compare_retrieval_methods() -> dict[str, Any]:
    return {
        "legacy": evaluate_legacy_retrieval(),
        "hybrid": evaluate_hybrid_retrieval(),
    }


def build_retrieval_eval_report() -> dict[str, Any]:
    cmp = compare_retrieval_methods()
    return {
        "summary": {
            "legacy_pass_rate": cmp["legacy"]["pass_rate"],
            "hybrid_pass_rate": cmp["hybrid"]["pass_rate"],
            "delta": round(cmp["hybrid"]["pass_rate"] - cmp["legacy"]["pass_rate"], 4),
        },
        "details": cmp,
    }
