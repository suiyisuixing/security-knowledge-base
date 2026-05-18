"""Portfolio project registry (A/B/C/D)."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from . import config


@lru_cache(maxsize=1)
def load_project_registry() -> dict[str, Any]:
    path = config.DATA_DIR / "project_registry.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def list_projects() -> list[dict[str, Any]]:
    return list(load_project_registry().get("projects", []))


def get_project(project_id: str) -> dict[str, Any] | None:
    for p in list_projects():
        if p["project_id"] == project_id:
            return p
    return None


def map_skill_to_projects(skill_id: str) -> list[str]:
    out: list[str] = []
    for p in list_projects():
        if skill_id in (p.get("skills") or []):
            out.append(p["project_id"])
    return out


def recommend_project_for_query(query: str) -> str:
    q = (query or "").lower()
    if any(k in q for k in ["rag", "prompt injection", "llm", "indirect injection", "retrieval augmented"]):
        return "llm-security-lab"
    if any(k in q for k in ["log", "alert", "soc", "sigma", "mitre", "triage", "detection"]):
        return "security-log-ai-assistant"
    if any(k in q for k in ["cve", "cvss", "kev", "epss", "sbom", "dependency", "openapi", "api ", "bola", "bfla", "mass assignment", "ssrf", "rate limit"]):
        return "vulnerability-intelligence-lab"
    return "security-knowledge-base"
