"""Agent hub service — API-facing wrapper (v5.0)."""

from __future__ import annotations

from typing import Any

from agent_hub import (
    project_adapter,
    cross_project_context,
    skill_evidence,
    portfolio_readiness,
    agent_orchestrator,
    next_action_planner,
    cross_project_report,
    maturity_model,
    roadmap_planner,
)

from . import config


def get_agent_hub_status() -> dict[str, Any]:
    samples = project_adapter.load_project_status_samples().get("samples", [])
    return {
        "version": config.get_project_version(),
        "model_free": True,
        "fully_local": True,
        "projects_tracked": len(samples),
        "primary_project": "security-knowledge-base",
    }


def build_agent_hub_context(query: str) -> dict[str, Any]:
    return cross_project_context.merge_knowledge_context_with_project_context(query)


def run_agent_hub_orchestration(query: str) -> dict[str, Any]:
    return agent_orchestrator.orchestrate_user_query(query)


def get_skill_evidence_report() -> dict[str, Any]:
    return skill_evidence.build_skill_evidence_report()


def get_missing_evidence_report() -> dict[str, Any]:
    return skill_evidence.build_missing_evidence_report()


def get_portfolio_readiness() -> dict[str, Any]:
    return portfolio_readiness.build_portfolio_readiness_report()


def get_cross_project_report() -> dict[str, Any]:
    return cross_project_report.build_v5_agent_hub_report()


def get_next_action_plan() -> dict[str, Any]:
    return next_action_planner.build_30_day_plan()


def get_maturity_report() -> dict[str, Any]:
    return {
        "summary": maturity_model.summarize_maturity_scores(),
        "per_project": maturity_model.score_all_projects(),
        "improvements": maturity_model.recommend_maturity_improvements(),
    }


def get_v5_release_report() -> dict[str, Any]:
    return {
        "roadmap": roadmap_planner.build_v5_roadmap(),
        "release_checklist": roadmap_planner.build_release_checklist("v5.0-rc"),
        "v5_to_v6": roadmap_planner.build_v5_to_v6_roadmap(),
        "notes": roadmap_planner.build_github_release_notes("v5.0-rc"),
    }
