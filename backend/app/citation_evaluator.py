"""Citation quality evaluation for grounded answers."""

from __future__ import annotations

from typing import Any

from . import knowledge_loader


def check_cited_docs_exist(answer: dict[str, Any]) -> bool:
    citations = answer.get("citations") or []
    if not citations:
        return False
    for c in citations:
        if not knowledge_loader.get_document_by_id(c.get("doc_id", "")):
            return False
    return True


def check_safety_note_present(answer: dict[str, Any]) -> bool:
    return bool((answer.get("safety_note") or "").strip())


def check_unsupported_claims(answer: dict[str, Any]) -> list[str]:
    citations = answer.get("citations") or []
    answer_text = (answer.get("answer") or "").lower()
    unsupported: list[str] = []
    if not citations and answer_text.strip():
        unsupported.append("answer text present but no citations")
    return unsupported


def evaluate_answer_citations(answer: dict[str, Any]) -> dict[str, Any]:
    cited_exist = check_cited_docs_exist(answer)
    note_present = check_safety_note_present(answer)
    unsupported = check_unsupported_claims(answer)
    notes = "ok" if cited_exist and note_present and not unsupported else "review required"
    return {
        "cited_docs_exist": cited_exist,
        "safety_note_present": note_present,
        "unsupported_claims": unsupported,
        "notes": notes,
    }


def summarize_citation_quality(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    if not total:
        return {"total": 0, "ok": 0, "ok_rate": 0.0}
    ok = sum(1 for r in results if r["cited_docs_exist"] and r["safety_note_present"] and not r["unsupported_claims"])
    return {"total": total, "ok": ok, "ok_rate": round(ok / total, 4)}
