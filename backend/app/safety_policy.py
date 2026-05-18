"""Safety policy classifier.

Classifies requests as allowed, needs confirmation, or blocked, with a
documented reason and safe redirect. Keyword-based for transparency.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from . import config

# Order matters: most specific intent first.
BLOCKED_ORDER = [
    "blocked_malware",
    "blocked_destructive_action",
    "blocked_exfiltration",
    "blocked_evasion",
    "blocked_persistence",
    "blocked_exploit_weaponization",
    "blocked_credential_attack",
    "blocked_unauthorized_public_scan",
]

NEEDS_ORDER = [
    "needs_rate_limit_confirmation",
    "needs_target_ownership_confirmation",
    "needs_authorization_confirmation",
    "needs_scope_confirmation",
]

ALLOWED_ORDER = [
    "allowed_authorized_recon_planning",
    "allowed_authorized_low_risk_check_planning",
    "allowed_authorized_testing",
    "allowed_local_lab",
    "allowed_code_review",
    "allowed_report_generation",
    "allowed_defensive",
    "allowed_learning",
]


@lru_cache(maxsize=1)
def load_safety_policy() -> dict[str, Any]:
    path = config.DATA_DIR / "safety_policy.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _lower(text: str) -> str:
    return (text or "").lower()


def _matches_any(text: str, keywords: list[str]) -> bool:
    return any(k.lower() in text for k in keywords)


def detect_blocked_intent(text: str) -> str | None:
    policy = load_safety_policy()
    keywords = policy.get("keywords", {})
    lowered = _lower(text)
    for cls in BLOCKED_ORDER:
        if _matches_any(lowered, keywords.get(cls, [])):
            return cls
    return None


def requires_authorization_confirmation(text: str) -> bool:
    policy = load_safety_policy()
    keywords = policy.get("keywords", {})
    lowered = _lower(text)
    return _matches_any(lowered, keywords.get("needs_authorization_confirmation", []))


def requires_scope_confirmation(text: str) -> bool:
    policy = load_safety_policy()
    keywords = policy.get("keywords", {})
    lowered = _lower(text)
    return _matches_any(lowered, keywords.get("needs_scope_confirmation", []))


def classify_request(text: str) -> dict[str, Any]:
    policy = load_safety_policy()
    classes = policy.get("classes", {})
    keywords = policy.get("keywords", {})
    lowered = _lower(text)

    blocked = detect_blocked_intent(text)
    if blocked:
        entry = classes.get(blocked, {})
        return {
            "classification": blocked,
            "allowed": False,
            "reason": entry.get("reason", ""),
            "safe_redirect": entry.get("safe_redirect", ""),
        }

    for cls in NEEDS_ORDER:
        if _matches_any(lowered, keywords.get(cls, [])):
            entry = classes.get(cls, {})
            return {
                "classification": cls,
                "allowed": False,
                "reason": entry.get("reason", ""),
                "safe_redirect": entry.get("safe_redirect", ""),
            }

    for cls in ALLOWED_ORDER:
        if _matches_any(lowered, keywords.get(cls, [])):
            entry = classes.get(cls, {})
            return {
                "classification": cls,
                "allowed": True,
                "reason": entry.get("reason", ""),
                "safe_redirect": entry.get("safe_redirect", ""),
            }

    entry = classes.get("allowed_learning", {})
    return {
        "classification": "allowed_learning",
        "allowed": True,
        "reason": entry.get("reason", "General educational query."),
        "safe_redirect": entry.get("safe_redirect", "Provide concept explanation."),
    }


def build_safe_redirect(classification: str) -> str:
    policy = load_safety_policy()
    classes = policy.get("classes", {})
    entry = classes.get(classification, {})
    return entry.get("safe_redirect", "Refer to safe boundary policy.")


def explain_policy_decision(text: str, classification: dict[str, Any]) -> str:
    cls = classification.get("classification", "unknown")
    allowed = classification.get("allowed", False)
    reason = classification.get("reason", "")
    redirect = classification.get("safe_redirect", "")
    decision = "ALLOWED" if allowed else "NOT ALLOWED"
    return (
        f"Decision: {decision}. Classification: {cls}. Reason: {reason} "
        f"Safe redirect: {redirect}"
    )
