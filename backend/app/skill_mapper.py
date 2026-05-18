"""Skill taxonomy and mapping helpers."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from . import config
from . import project_registry


@lru_cache(maxsize=1)
def load_skill_taxonomy() -> dict[str, Any]:
    path = config.DATA_DIR / "skill_taxonomy.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def list_skills() -> list[dict[str, Any]]:
    return list(load_skill_taxonomy().get("skills", []))


def get_skill(skill_id: str) -> dict[str, Any] | None:
    for s in list_skills():
        if s["skill_id"] == skill_id:
            return s
    return None


_QUERY_KEYWORDS = {
    "prompt_injection_reasoning": ["prompt injection", "injection", "jailbreak"],
    "rag_access_control": ["rag acl", "rag access", "retrieval acl", "rag security"],
    "secure_retrieval_design": ["retrieval design", "rag", "retrieval"],
    "log_analysis": ["log", "logs"],
    "mitre_mapping": ["mitre", "att&ck", "attack framework"],
    "alert_triage": ["alert", "triage"],
    "detection_engineering": ["detection", "sigma", "siem"],
    "api_authorization_reasoning": ["bola", "bfla", "authorization", "idor", "api auth"],
    "vulnerability_prioritization": ["cve", "kev", "epss", "prioritize", "cvss"],
    "safe_verification_planning": ["verify", "verification", "safe verification"],
    "secure_code_review": ["code review", "secure code"],
    "configuration_review": ["configuration", "config review", "nginx", "apache"],
    "dependency_risk_reasoning": ["dependency", "sbom"],
    "authorized_recon_planning": ["recon", "reconnaissance"],
    "safety_boundary_classification": ["safety", "policy", "classify"],
    "task_routing": ["route", "routing"],
}


def map_query_to_skills(query: str) -> list[str]:
    q = (query or "").lower()
    out: list[str] = []
    for skill_id, keywords in _QUERY_KEYWORDS.items():
        if any(k in q for k in keywords):
            out.append(skill_id)
    return out


def map_document_to_skills(doc: dict[str, Any]) -> list[str]:
    meta = doc.get("metadata", {}) if doc else {}
    return list(meta.get("related_skills", []) or [])


def map_project_to_skills(project_id: str) -> list[str]:
    project = project_registry.get_project(project_id)
    if not project:
        return []
    return list(project.get("skills", []) or [])


def recommend_skills_for_goal(goal: str) -> list[str]:
    g = (goal or "").lower()
    recs: list[str] = []
    if "ai" in g or "rag" in g or "llm" in g:
        recs.extend(["prompt_injection_reasoning", "rag_access_control", "secure_retrieval_design"])
    if "detection" in g or "soc" in g:
        recs.extend(["log_analysis", "mitre_mapping", "alert_triage", "detection_engineering"])
    if "vulnerability" in g or "cve" in g or "patch" in g:
        recs.extend(["vulnerability_prioritization", "dependency_risk_reasoning"])
    if "code" in g or "secure coding" in g:
        recs.extend(["secure_code_review", "configuration_review"])
    if "safety" in g or "policy" in g or "boundary" in g:
        recs.extend(["safety_boundary_classification", "safe_verification_planning"])
    seen: set[str] = set()
    deduped: list[str] = []
    for s in recs:
        if s not in seen:
            seen.add(s)
            deduped.append(s)
    return deduped
