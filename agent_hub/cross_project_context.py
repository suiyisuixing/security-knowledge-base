"""Cross-project context (v5.0)."""

from __future__ import annotations

from typing import Any

from app import knowledge_loader
from app import retrieval as legacy_retrieval
from app import safety_policy
from app import skill_mapper
from app import project_registry
from . import project_adapter


def build_context_for_projects(project_ids: list[str]) -> dict[str, Any]:
    summaries = [project_adapter.build_project_adapter_summary(pid) for pid in project_ids]
    return {"projects": summaries}


def build_cross_project_context(query: str) -> dict[str, Any]:
    project = project_registry.recommend_project_for_query(query)
    summaries = build_context_for_projects([project])
    return {
        "query": query,
        "primary_project": project,
        "projects": summaries["projects"],
    }


def attach_retrieval_citations(context: dict[str, Any]) -> dict[str, Any]:
    query = context.get("query", "")
    docs = legacy_retrieval.search_knowledge(query, top_k=5)
    context["citations"] = [{"doc_id": d["doc_id"], "title": d["title"], "domain": d["domain"]} for d in docs]
    return context


def attach_related_skills(context: dict[str, Any]) -> dict[str, Any]:
    query = context.get("query", "")
    context["related_skills"] = skill_mapper.map_query_to_skills(query)
    return context


def attach_safety_classification(context: dict[str, Any]) -> dict[str, Any]:
    query = context.get("query", "")
    context["safety"] = safety_policy.classify_request(query)
    return context


def attach_recommended_project_route(context: dict[str, Any]) -> dict[str, Any]:
    from app import task_router
    query = context.get("query", "")
    context["recommended_route"] = task_router.route_task(query)
    return context


def merge_knowledge_context_with_project_context(query: str) -> dict[str, Any]:
    context = build_cross_project_context(query)
    attach_retrieval_citations(context)
    attach_related_skills(context)
    attach_safety_classification(context)
    attach_recommended_project_route(context)
    context["knowledge_summary"] = knowledge_loader.summarize_knowledge_base()
    return context
