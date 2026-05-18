"""Build agent context for queries, projects, and skills."""

from __future__ import annotations

from typing import Any

from . import knowledge_loader
from . import project_registry
from . import retrieval
from . import safety_policy
from . import skill_mapper


BOUNDARY = (
    "Local lab, defensive analysis, code review, authorized testing, "
    "authorized reconnaissance planning, or safe verification planning only."
)


def build_context_for_query(query: str, top_k: int = 3) -> dict[str, Any]:
    results = retrieval.search_knowledge(query, top_k=top_k)
    classification = safety_policy.classify_request(query)
    skill_ids: list[str] = []
    project_ids: list[str] = []
    for r in results:
        doc = knowledge_loader.get_document_by_id(r["doc_id"])
        if doc:
            for s in doc["metadata"].get("related_skills", []) or []:
                if s not in skill_ids:
                    skill_ids.append(s)
            for p in doc["metadata"].get("related_projects", []) or []:
                if p not in project_ids:
                    project_ids.append(p)
    next_step = (
        "Provide concept explanation."
        if classification["allowed"]
        else "Confirm scope/authorization or decline and redirect."
    )
    return {
        "query": query,
        "retrieved": results,
        "related_skills": skill_ids,
        "related_projects": project_ids,
        "safety_classification": classification["classification"],
        "safety_allowed": classification["allowed"],
        "safe_boundary": BOUNDARY,
        "recommended_next_step": next_step,
    }


def build_context_for_project(project_id: str) -> dict[str, Any]:
    project = project_registry.get_project(project_id)
    if not project:
        return {"project_id": project_id, "found": False}
    skills = skill_mapper.map_project_to_skills(project_id)
    return {
        "project_id": project_id,
        "found": True,
        "name": project.get("name"),
        "focus": project.get("focus"),
        "skills": skills,
        "safe_boundary": BOUNDARY,
    }


def build_context_for_skill(skill_id: str) -> dict[str, Any]:
    skill = skill_mapper.get_skill(skill_id)
    if not skill:
        return {"skill_id": skill_id, "found": False}
    projects = project_registry.map_skill_to_projects(skill_id)
    return {
        "skill_id": skill_id,
        "found": True,
        "name": skill.get("name"),
        "domain": skill.get("domain"),
        "projects": projects,
        "safe_boundary": BOUNDARY,
    }


def build_agent_context(query: str) -> dict[str, Any]:
    return build_context_for_query(query, top_k=5)
