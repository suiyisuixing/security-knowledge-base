"""Workflow reasoner — generates planning artifacts only (v4.0)."""

from __future__ import annotations

from typing import Any

from app import authorized_workflow


def reason_about_authorized_workflow(request: str) -> dict[str, Any]:
    return authorized_workflow.build_authorized_workflow({"request": request})


def build_safe_verification_plan(request: str) -> dict[str, Any]:
    wf = reason_about_authorized_workflow(request)
    if not wf.get("allowed"):
        return {
            "plan_id": "safe-verification-blocked",
            "allowed": False,
            "reason": "Request not in authorized scope.",
            "steps": [],
        }
    return {
        "plan_id": "safe-verification-001",
        "allowed": True,
        "required_scope": wf.get("required_scope", ""),
        "steps": [
            "Document the assumption and authorization context.",
            "Identify the smallest reproducible test case in the local lab.",
            "Capture inputs, outputs, and detection signals.",
            "Prefer passive observation; avoid destructive operations.",
            "Document remediation and a regression test.",
        ],
    }


def build_low_risk_check_plan(request: str) -> dict[str, Any]:
    wf = reason_about_authorized_workflow(request)
    if not wf.get("allowed"):
        return {
            "plan_id": "low-risk-check-blocked",
            "allowed": False,
            "reason": "Request not in authorized scope.",
            "steps": [],
        }
    return {
        "plan_id": "low-risk-check-001",
        "allowed": True,
        "required_scope": wf.get("required_scope", ""),
        "steps": [
            "Confirm asset ownership or authorization.",
            "Review headers and configuration artifacts only.",
            "Avoid active probes that consume rate limits.",
            "Document findings and suggested remediation.",
        ],
    }


def build_local_lab_plan(request: str) -> dict[str, Any]:
    return {
        "plan_id": "local-lab-001",
        "allowed": True,
        "required_scope": "local_lab",
        "steps": [
            "Use isolated VMs or containers under your full control.",
            "Snapshot before each test for safe rollback.",
            "Document the lab topology and assumptions.",
            "Generate a defensive verification plan as the deliverable.",
        ],
    }


def build_blocked_workflow_explanation(request: str) -> dict[str, Any]:
    wf = reason_about_authorized_workflow(request)
    return {
        "blocked": not wf.get("allowed", False),
        "required_scope": wf.get("required_scope", ""),
        "blocked_actions": wf.get("blocked_actions", []),
        "explanation": (
            "Request did not present a local lab, self-owned asset, or "
            "documented authorization. Provide one to unblock planning."
        ),
    }
