"""Vulnerability reasoning templates."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from . import config


@lru_cache(maxsize=1)
def load_reasoning_templates() -> list[dict[str, Any]]:
    with (config.DATA_DIR / "reasoning_templates.json").open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("templates", [])


def list_templates() -> list[dict[str, Any]]:
    return list(load_reasoning_templates())


def get_template(template_id: str) -> dict[str, Any] | None:
    for t in list_templates():
        if t.get("template_id") == template_id:
            return t
    return None


_RECOMMENDATION_KEYWORDS = {
    "api_authorization_review": ["bola", "bfla", "authorization", "idor", "endpoint", "api "],
    "dependency_risk_review": ["dependency", "sbom", "cve", "kev"],
    "configuration_risk_review": ["config", "configuration", "nginx", "apache", "secrets"],
    "rag_security_review": ["rag", "retrieval", "prompt injection", "llm"],
    "log_detection_review": ["log", "sigma", "siem", "detection", "alert"],
    "authorized_recon_planning": ["recon", "reconnaissance"],
    "safe_verification_plan": ["verify", "verification"],
    "remediation_plan": ["remediation", "patch", "fix"],
}


def recommend_template_for_query(query: str) -> str | None:
    q = (query or "").lower()
    for template_id, keywords in _RECOMMENDATION_KEYWORDS.items():
        if any(k in q for k in keywords):
            return template_id
    return None


def render_template_steps(template_id: str) -> list[str]:
    t = get_template(template_id)
    if not t:
        return []
    return list(t.get("steps", []))
