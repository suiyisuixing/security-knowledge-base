"""Agent orchestrator — rule-based, no LLM (v5.0)."""

from __future__ import annotations

from typing import Any

from app import safety_policy
from app import task_router
from app import retrieval as legacy_retrieval
from app import authorized_workflow

from . import cross_project_context
from . import project_adapter


def classify_task(query: str) -> dict[str, Any]:
    return safety_policy.classify_request(query)


def route_to_project_or_skill(query: str) -> dict[str, Any]:
    return task_router.route_task(query)


def retrieve_supporting_knowledge(query: str) -> list[dict[str, Any]]:
    return legacy_retrieval.search_knowledge(query, top_k=5)


def build_safe_reasoning_context(query: str) -> dict[str, Any]:
    return cross_project_context.merge_knowledge_context_with_project_context(query)


def choose_reasoning_mode(query: str) -> str:
    cls = safety_policy.classify_request(query)
    if not cls["allowed"] and cls["classification"].startswith("blocked_"):
        return "safety_classification"
    if not cls["allowed"]:
        return "safety_classification"
    q = (query or "").lower()
    if any(k in q for k in ("plan", "workflow", "verification", "recon", "in my local lab", "my own staging")):
        return "authorized_workflow"
    if any(k in q for k in ("route", "which project", "where should")):
        return "project_routing"
    if any(k in q for k in ("gap", "missing", "coverage", "readiness")):
        return "portfolio_gap_analysis"
    if any(k in q for k in ("skill", "learn", "next step")):
        return "skill_gap_analysis"
    if any(k in q for k in ("benchmark", "evaluate", "evaluation")):
        return "benchmark_analysis"
    if any(k in q for k in ("explain", "what is", "describe", "concept", "overview")):
        return "rule_based_grounded_answer"
    return "knowledge_only"


def produce_orchestration_result(query: str) -> dict[str, Any]:
    cls = classify_task(query)
    mode = choose_reasoning_mode(query)
    route = route_to_project_or_skill(query)
    docs = retrieve_supporting_knowledge(query) if cls["allowed"] else []
    wf: dict[str, Any] | None = None
    if mode == "authorized_workflow":
        wf = authorized_workflow.build_authorized_workflow({"request": query})
    return {
        "query": query,
        "mode": mode,
        "classification": cls,
        "route": route,
        "retrieved_docs": docs,
        "workflow": wf,
        "primary_project_summary": project_adapter.build_project_adapter_summary(route["project_id"]),
    }


def orchestrate_user_query(query: str) -> dict[str, Any]:
    return produce_orchestration_result(query)
