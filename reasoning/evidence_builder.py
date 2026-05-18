"""Evidence chain builder (v4.0)."""

from __future__ import annotations

from typing import Any

from app import retrieval
from app import skill_mapper
from app import project_registry
from app import safety_policy


def select_supporting_documents(query: str, docs: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    if docs is not None:
        return docs[:5]
    return retrieval.search_knowledge(query, top_k=5)


def select_relevant_skills(query: str) -> list[str]:
    return skill_mapper.map_query_to_skills(query)


def select_related_projects(query: str) -> list[str]:
    pid = project_registry.recommend_project_for_query(query)
    return [pid]


def build_evidence_summary(evidence: dict[str, Any]) -> str:
    docs = evidence.get("retrieved_docs", [])
    skills = evidence.get("related_skills", [])
    projects = evidence.get("related_projects", [])
    return (
        f"docs={len(docs)} skills={len(skills)} projects={len(projects)} "
        f"policy={evidence.get('safety_policy_decision', {}).get('classification', '')}"
    )


def build_evidence_chain(
    query: str,
    retrieved_docs: list[dict[str, Any]] | None = None,
    policy_decision: dict[str, Any] | None = None,
) -> dict[str, Any]:
    docs = select_supporting_documents(query, retrieved_docs)
    cited = [d["doc_id"] for d in docs]
    skills = select_relevant_skills(query)
    projects = select_related_projects(query)
    decision = policy_decision if policy_decision is not None else safety_policy.classify_request(query)
    evidence = {
        "query": query,
        "retrieved_docs": docs,
        "cited_doc_ids": cited,
        "related_skills": skills,
        "related_projects": projects,
        "safety_policy_decision": decision,
        "limitations": [
            "Local knowledge only; no external sources consulted.",
            "Rule-based reasoning; no model inference.",
        ],
        "recommended_next_step": (
            "Refer to the cited documents and the safe boundary policy."
        ),
    }
    evidence["summary"] = build_evidence_summary(evidence)
    return evidence
