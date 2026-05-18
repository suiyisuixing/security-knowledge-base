"""Policy reasoner — human-readable explanations for safety decisions (v4.0)."""

from __future__ import annotations

from typing import Any

from app import safety_policy


def reason_about_safety_policy(query: str) -> dict[str, Any]:
    cls = safety_policy.classify_request(query)
    return {
        "query": query,
        "classification": cls["classification"],
        "allowed": cls["allowed"],
        "reason": cls["reason"],
        "safe_redirect": cls["safe_redirect"],
    }


def reason_about_authorized_scope(query: str) -> dict[str, Any]:
    cls = safety_policy.classify_request(query)
    is_authorized_kind = cls["classification"] in (
        "allowed_local_lab",
        "allowed_authorized_testing",
        "allowed_authorized_recon_planning",
        "allowed_authorized_low_risk_check_planning",
    )
    return {
        "query": query,
        "is_authorized_scope": is_authorized_kind,
        "classification": cls["classification"],
        "explanation": (
            "Authorized scope detected. Planning artifacts may be generated."
            if is_authorized_kind
            else "No authorized scope detected. Recommend local lab or authorization confirmation."
        ),
    }


def reason_about_blocked_actions(query: str) -> dict[str, Any]:
    blocked = safety_policy.detect_blocked_intent(query)
    return {
        "query": query,
        "blocked": bool(blocked),
        "classification": blocked or "",
        "explanation": (
            f"Detected blocked intent: {blocked}." if blocked
            else "No blocked intent detected."
        ),
    }


def reason_about_allowed_actions(query: str) -> dict[str, Any]:
    cls = safety_policy.classify_request(query)
    if not cls["allowed"]:
        return {
            "query": query,
            "allowed": False,
            "allowed_actions": [],
            "explanation": "Request is not in an allowed category.",
        }
    actions: list[str] = []
    klass = cls["classification"]
    if klass == "allowed_learning":
        actions = ["explain concept", "cite local knowledge", "recommend related skills"]
    elif klass == "allowed_local_lab":
        actions = ["draft local lab plan", "suggest safe verification steps"]
    elif klass == "allowed_code_review":
        actions = ["analyze code for vulnerabilities", "suggest remediation"]
    elif klass == "allowed_defensive":
        actions = ["suggest detection rules", "build triage playbook"]
    elif klass == "allowed_authorized_recon_planning":
        actions = ["draft recon plan", "list scope guardrails"]
    elif klass == "allowed_authorized_low_risk_check_planning":
        actions = ["draft low-risk check plan", "prefer passive observation"]
    elif klass == "allowed_report_generation":
        actions = ["structure the report", "review boundary statements"]
    elif klass == "allowed_authorized_testing":
        actions = ["draft test plan", "list authorization requirements"]
    return {
        "query": query,
        "allowed": True,
        "allowed_actions": actions,
        "explanation": f"Allowed category {klass}; safe action list generated.",
    }


def build_policy_explanation(query: str) -> dict[str, Any]:
    return {
        "safety": reason_about_safety_policy(query),
        "scope": reason_about_authorized_scope(query),
        "blocked": reason_about_blocked_actions(query),
        "allowed_actions": reason_about_allowed_actions(query),
    }
