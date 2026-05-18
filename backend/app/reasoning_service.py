"""Reasoning service — orchestrates the reasoning/ package via the API (v4.0)."""

from __future__ import annotations

from typing import Any

from reasoning import (
    rule_engine,
    decision_tree,
    policy_reasoner,
    risk_scoring,
    evidence_builder,
    template_renderer,
    workflow_reasoner,
    explanation_builder,
)

from . import retrieval
from . import safety_policy


def run_rule_based_reasoning(query: str) -> dict[str, Any]:
    return rule_engine.apply_rule_set(query)


def build_reasoned_answer(query: str) -> dict[str, Any]:
    docs = retrieval.search_knowledge(query, top_k=5)
    decision = safety_policy.classify_request(query)
    evidence = evidence_builder.build_evidence_chain(query, docs, decision)
    rendered = template_renderer.render_grounded_answer_template(query, evidence)
    explanation = explanation_builder.build_user_friendly_explanation(query, evidence)
    return {
        "query": query,
        "answer": rendered,
        "evidence": evidence,
        "decision": decision,
        "explanation": explanation,
    }


def build_policy_reasoning(query: str) -> dict[str, Any]:
    return policy_reasoner.build_policy_explanation(query)


def build_workflow_reasoning(request: str) -> dict[str, Any]:
    wf = workflow_reasoner.reason_about_authorized_workflow(request)
    rendered = template_renderer.render_authorized_workflow_template(wf)
    risk = risk_scoring.score_workflow_risk(wf)
    return {"request": request, "workflow": wf, "rendered": rendered, "risk": risk}


def build_task_route_reasoning(query: str) -> dict[str, Any]:
    from . import task_router
    route = task_router.route_task(query)
    rendered = template_renderer.render_task_route_template(route)
    return {"query": query, "route": route, "rendered": rendered}


def build_evidence_based_report(query: str) -> dict[str, Any]:
    docs = retrieval.search_knowledge(query, top_k=5)
    decision = safety_policy.classify_request(query)
    evidence = evidence_builder.build_evidence_chain(query, docs, decision)
    risk = risk_scoring.score_request_risk(query)
    return {
        "query": query,
        "evidence": evidence,
        "risk": risk,
        "decision": decision,
    }


def build_decision_path(query: str) -> dict[str, Any]:
    return decision_tree.classify_with_decision_tree(query)
