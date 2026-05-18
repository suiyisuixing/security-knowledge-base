"""Route security tasks to portfolio projects and skills."""

from __future__ import annotations

from typing import Any

from . import project_registry
from . import skill_mapper


_PROJECT_RULES: list[tuple[str, list[str]]] = [
    ("llm-security-lab", ["rag", "prompt injection", "llm", "indirect injection", "retrieval augmented", "rag acl"]),
    ("security-log-ai-assistant", ["log", "alert", "soc", "sigma", "mitre", "triage", "detection"]),
    ("vulnerability-intelligence-lab", ["cve", "cvss", "kev", "epss", "sbom", "dependency", "openapi", "bola", "bfla", "mass assignment", "ssrf", "rate limit", "api "]),
    ("security-knowledge-base", ["concept", "learning", "safety", "policy", "classify", "boundary", "responsible disclosure", "task routing"]),
]

_DOMAIN_RULES: list[tuple[str, list[str]]] = [
    ("ai_security", ["rag", "prompt injection", "llm", "retrieval"]),
    ("detection_engineering", ["log", "alert", "sigma", "mitre", "triage", "detection"]),
    ("vulnerability_intelligence", ["cve", "cvss", "kev", "epss", "sbom"]),
    ("api_security", ["api ", "bola", "bfla", "mass assignment", "ssrf", "rate limit", "openapi"]),
    ("secure_coding", ["code review", "input validation", "secrets", "logging"]),
    ("safe_boundaries", ["safety", "policy", "boundary", "responsible disclosure", "authorized recon"]),
]


def route_to_project(query: str) -> str:
    q = (query or "").lower()
    for project_id, keywords in _PROJECT_RULES:
        if any(k in q for k in keywords):
            return project_id
    return "security-knowledge-base"


def route_to_knowledge_domain(query: str) -> str:
    q = (query or "").lower()
    for domain, keywords in _DOMAIN_RULES:
        if any(k in q for k in keywords):
            return domain
    return "safe_boundaries"


def route_to_skill(query: str) -> str:
    skills = skill_mapper.map_query_to_skills(query)
    if skills:
        return skills[0]
    return "safety_boundary_classification"


def explain_route(query: str, route: dict[str, Any]) -> str:
    return (
        f"Routed query to project={route['project_id']} domain={route['knowledge_domain']} "
        f"skill={route['skill_id']} based on keyword rules."
    )


def route_task(query: str) -> dict[str, Any]:
    project_id = route_to_project(query)
    domain = route_to_knowledge_domain(query)
    skill = route_to_skill(query)
    project = project_registry.get_project(project_id) or {"name": project_id}
    route = {
        "query": query,
        "project_id": project_id,
        "knowledge_domain": domain,
        "skill_id": skill,
        "explanation": "",
    }
    route["explanation"] = explain_route(query, route) + f" Target: {project.get('name', project_id)}."
    return route
