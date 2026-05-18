"""Cross-project reports (v5.0)."""

from __future__ import annotations

from typing import Any

from . import project_adapter
from . import skill_evidence
from . import portfolio_readiness
from . import maturity_model


def build_cross_project_summary_report() -> dict[str, Any]:
    samples = project_adapter.load_project_status_samples().get("samples", [])
    items = [project_adapter.build_project_adapter_summary(s["project_id"]) for s in samples]
    return {
        "title": "Cross-project Summary",
        "projects": items,
    }


def build_project_relationship_report() -> dict[str, Any]:
    samples = project_adapter.load_project_status_samples().get("samples", [])
    edges = []
    for s in samples:
        for skill in s.get("skill_coverage", []):
            edges.append({"project_id": s["project_id"], "skill_id": skill})
    return {
        "title": "Project Relationship Report",
        "edges": edges,
        "edge_count": len(edges),
    }


def build_skill_coverage_report() -> dict[str, Any]:
    return skill_evidence.build_skill_evidence_report()


def build_security_agent_capability_report() -> dict[str, Any]:
    capabilities = []
    for s in project_adapter.load_project_status_samples().get("samples", []):
        capabilities.extend(s.get("capabilities", []))
    return {
        "title": "Security Agent Capabilities",
        "capabilities": sorted(set(capabilities)),
    }


def build_v5_agent_hub_report() -> dict[str, Any]:
    return {
        "title": "v5.0 Agent Hub Report",
        "summary": build_cross_project_summary_report(),
        "relationships": build_project_relationship_report(),
        "skills": build_skill_coverage_report(),
        "capabilities": build_security_agent_capability_report(),
        "readiness": portfolio_readiness.build_portfolio_readiness_report(),
        "maturity": maturity_model.score_all_projects(),
        "boundary_note": (
            "Local-only, model-free, defensive, authorized-scope project. "
            "Does not use LLMs, real scanning, or exploitation."
        ),
    }
