"""Decision-tree reasoning (v4.0)."""

from __future__ import annotations

from typing import Any

from app import safety_policy
from app import authorized_workflow
from app import task_router


def _node(name: str, matched: bool, detail: str) -> dict[str, Any]:
    return {"node": name, "matched": matched, "detail": detail}


def build_safety_decision_path(query: str) -> list[dict[str, Any]]:
    path: list[dict[str, Any]] = []
    blocked = safety_policy.detect_blocked_intent(query)
    path.append(_node("detect_blocked_intent", bool(blocked), blocked or "no blocked intent detected"))
    if blocked:
        return path
    if safety_policy.requires_authorization_confirmation(query):
        path.append(_node("requires_authorization_confirmation", True, "needs_authorization_confirmation"))
        return path
    if safety_policy.requires_scope_confirmation(query):
        path.append(_node("requires_scope_confirmation", True, "needs_scope_confirmation"))
        return path
    cls = safety_policy.classify_request(query)
    path.append(_node("classify_request", True, cls["classification"]))
    return path


def build_authorization_decision_path(query: str) -> list[dict[str, Any]]:
    path: list[dict[str, Any]] = []
    scope = authorized_workflow.validate_scope(query)
    path.append(_node("validate_scope", scope["in_scope"], scope["kind"]))
    auth = authorized_workflow.validate_authorization_claim(query)
    path.append(_node("validate_authorization_claim", auth["valid"], auth["kind"]))
    return path


def build_routing_decision_path(query: str) -> list[dict[str, Any]]:
    route = task_router.route_task(query)
    return [
        _node("route_to_project", True, route["project_id"]),
        _node("route_to_knowledge_domain", True, route["knowledge_domain"]),
        _node("route_to_skill", True, route["skill_id"]),
    ]


def explain_decision_path(path: list[dict[str, Any]]) -> str:
    if not path:
        return "empty decision path"
    return " → ".join(f"{n['node']}={n['detail']}" for n in path)


def classify_with_decision_tree(query: str) -> dict[str, Any]:
    safety = build_safety_decision_path(query)
    auth = build_authorization_decision_path(query)
    routing = build_routing_decision_path(query)
    cls = safety_policy.classify_request(query)
    confidence = 0.95 if safety[0]["matched"] else 0.8
    return {
        "input": query,
        "matched_conditions": [n["node"] for n in safety + auth + routing if n["matched"]],
        "decision": cls["classification"],
        "allowed": cls["allowed"],
        "confidence": confidence,
        "safe_redirect": cls.get("safe_redirect", ""),
        "next_step": "Use rule-based reasoning to construct a grounded answer or workflow plan.",
        "safety_path": safety,
        "authorization_path": auth,
        "routing_path": routing,
        "explanation": explain_decision_path(safety + auth + routing),
    }
