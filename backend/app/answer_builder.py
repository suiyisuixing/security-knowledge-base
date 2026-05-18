"""Build knowledge-grounded answers with citations and safety notes."""

from __future__ import annotations

from typing import Any

from . import knowledge_loader

SAFETY_NOTE = (
    "Safety boundary: this answer is for local labs, defensive analysis, "
    "and explicitly authorized work. The system does not support unauthorized "
    "scanning or exploitation."
)


def build_citations(search_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    citations: list[dict[str, Any]] = []
    seen: set[str] = set()
    for r in search_results:
        doc_id = r.get("doc_id")
        if not doc_id or doc_id in seen:
            continue
        seen.add(doc_id)
        citations.append({
            "doc_id": doc_id,
            "title": r.get("title", ""),
            "domain": r.get("domain", ""),
        })
    return citations


def build_safety_note(search_results: list[dict[str, Any]]) -> str:
    return SAFETY_NOTE


def build_related_skills(search_results: list[dict[str, Any]]) -> list[str]:
    skills: list[str] = []
    seen: set[str] = set()
    for r in search_results:
        doc = knowledge_loader.get_document_by_id(r.get("doc_id", ""))
        if not doc:
            continue
        for s in doc["metadata"].get("related_skills", []) or []:
            if s not in seen:
                seen.add(s)
                skills.append(s)
    return skills


def build_related_projects(search_results: list[dict[str, Any]]) -> list[str]:
    projects: list[str] = []
    seen: set[str] = set()
    for r in search_results:
        doc = knowledge_loader.get_document_by_id(r.get("doc_id", ""))
        if not doc:
            continue
        for p in doc["metadata"].get("related_projects", []) or []:
            if p not in seen:
                seen.add(p)
                projects.append(p)
    return projects


def build_grounded_answer(query: str, search_results: list[dict[str, Any]]) -> dict[str, Any]:
    if not search_results:
        return {
            "query": query,
            "answer": (
                "No matching knowledge documents were found locally for this query. "
                "Try a different phrasing or browse the knowledge domains."
            ),
            "citations": [],
            "safety_note": SAFETY_NOTE,
            "related_skills": [],
            "related_projects": [],
        }
    lines: list[str] = []
    lines.append(f"Answer to: {query.strip()}")
    lines.append("")
    lines.append("Based on local knowledge documents:")
    for r in search_results:
        lines.append(f"- [{r['doc_id']}] {r['title']} ({r['domain']})")
        snippet = r.get("snippet", "").replace("\n", " ").strip()
        if snippet:
            lines.append(f"  - {snippet[:240]}")
    lines.append("")
    lines.append(SAFETY_NOTE)
    return {
        "query": query,
        "answer": "\n".join(lines),
        "citations": build_citations(search_results),
        "safety_note": SAFETY_NOTE,
        "related_skills": build_related_skills(search_results),
        "related_projects": build_related_projects(search_results),
    }
