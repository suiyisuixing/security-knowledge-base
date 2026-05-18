"""Explanation builder — composes user-friendly explanations (v4.0)."""

from __future__ import annotations

from typing import Any


def build_short_explanation(query: str, decision: dict[str, Any]) -> str:
    return (
        f"Query {query!r} → classification={decision.get('classification')} "
        f"allowed={decision.get('allowed')}"
    )


def build_user_friendly_explanation(query: str, result: dict[str, Any]) -> str:
    decision = result.get("safety_policy_decision") or result.get("decision") or {}
    classification = decision.get("classification") or result.get("classification", "")
    allowed = decision.get("allowed") if "allowed" in decision else result.get("allowed", True)
    lines = [
        f"You asked: {query}",
        "",
        f"Safety classification: {classification}",
        f"Allowed: {allowed}",
    ]
    docs = result.get("retrieved_docs") or []
    if docs:
        lines.append("")
        lines.append("Citations:")
        for d in docs:
            lines.append(f"  - [{d.get('doc_id')}] {d.get('title')}")
    skills = result.get("related_skills") or []
    if skills:
        lines.append("")
        lines.append("Related skills: " + ", ".join(skills))
    projects = result.get("related_projects") or []
    if projects:
        lines.append("Related projects: " + ", ".join(projects))
    return "\n".join(lines)


def build_reviewer_explanation(query: str, result: dict[str, Any]) -> str:
    short = build_short_explanation(query, result.get("safety_policy_decision", {}) or result)
    rule_count = result.get("matched_count", 0)
    summary = result.get("summary", "")
    return f"{short}\nMatched rules: {rule_count}\nSummary: {summary}"


def build_explanation(query: str, evidence: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "query": query,
        "short": build_short_explanation(query, decision),
        "user_friendly": build_user_friendly_explanation(query, evidence),
        "reviewer": build_reviewer_explanation(query, evidence),
    }
