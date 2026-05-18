"""Authorized workflow planner (planning artifacts only — no execution)."""

from __future__ import annotations

from typing import Any

from . import safety_policy


_LOCAL_LAB_KEYWORDS = ["my local lab", "in my lab", "local vm", "isolated lab", "home lab"]
_SELF_ASSET_KEYWORDS = [
    "my own server",
    "my own staging",
    "my staging server",
    "my own staging server",
    "my staging",
    "my own asset",
    "my own repo",
    "my own site",
    "my own website",
    "my own host",
    "my own application",
    "my own service",
]
_AUTHORIZED_KEYWORDS = ["i have authorization", "authorized scope", "bug bounty scope", "explicit authorization", "engagement scope"]


def validate_authorization_claim(request: str) -> dict[str, Any]:
    text = (request or "").lower()
    if any(k in text for k in _LOCAL_LAB_KEYWORDS):
        return {"valid": True, "kind": "local_lab"}
    if any(k in text for k in _SELF_ASSET_KEYWORDS):
        return {"valid": True, "kind": "self_owned_asset"}
    if any(k in text for k in _AUTHORIZED_KEYWORDS):
        return {"valid": True, "kind": "authorized_engagement"}
    return {"valid": False, "kind": "unconfirmed"}


def validate_scope(request: str) -> dict[str, Any]:
    classification = safety_policy.classify_request(request)
    auth = validate_authorization_claim(request)
    if not classification["allowed"] and classification["classification"].startswith("blocked_"):
        return {"in_scope": False, "reason": "blocked safety classification", "kind": "blocked"}
    if auth["valid"]:
        return {"in_scope": True, "reason": "explicit local/self/authorized scope claim", "kind": auth["kind"]}
    return {"in_scope": False, "reason": "no explicit scope claim", "kind": "unconfirmed"}


def build_allowed_workflow_steps(request: str) -> list[str]:
    return [
        "Confirm authorization and scope.",
        "Identify assets within scope.",
        "Perform low-risk information collection planning.",
        "Generate safe verification plan.",
        "Prepare remediation report.",
    ]


def build_blocked_actions(request: str) -> list[str]:
    return [
        "No unauthorized public scanning.",
        "No credential attacks.",
        "No exploit weaponization.",
        "No persistence or backdoors.",
        "No detection evasion.",
        "No data exfiltration.",
        "No destructive operations.",
    ]


def build_authorized_workflow(request_payload: dict[str, Any]) -> dict[str, Any]:
    request = request_payload.get("request", "") if isinstance(request_payload, dict) else str(request_payload)
    scope = validate_scope(request)
    if scope["in_scope"]:
        return {
            "workflow_id": f"authz-workflow-{scope['kind']}",
            "allowed": True,
            "required_scope": scope["kind"],
            "steps": build_allowed_workflow_steps(request),
            "blocked_actions": build_blocked_actions(request),
            "summary": "Planning artifact only. Execution remains the responsibility of an authorized human.",
        }
    return {
        "workflow_id": "authz-workflow-blocked",
        "allowed": False,
        "required_scope": "blocked",
        "steps": [],
        "blocked_actions": build_blocked_actions(request) + [
            "Unauthorized scanning of third-party targets is not supported.",
        ],
        "summary": "Request requires local lab, self-owned asset, or documented authorization.",
    }


def summarize_workflow(workflow: dict[str, Any]) -> str:
    allowed = workflow.get("allowed", False)
    scope = workflow.get("required_scope", "")
    return f"allowed={allowed} scope={scope} steps={len(workflow.get('steps', []))}"
