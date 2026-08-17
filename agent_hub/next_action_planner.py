"""Next action planner (v5.0)."""

from __future__ import annotations

from typing import Any

from . import portfolio_readiness
from . import skill_evidence


_SAFE_BOUNDARY_NOTE = (
    "All suggestions stay within the local-only, model-free, authorized-scope "
    "boundary. No real scanning, no exploit code, no external API."
)


def recommend_next_project_actions() -> list[dict[str, Any]]:
    readiness = portfolio_readiness.calculate_overall_portfolio_readiness()
    cats = readiness["categories"]
    actions = []
    for k, v in sorted(cats.items(), key=lambda kv: kv[1]):
        if v < 0.9:
            actions.append({"category": k, "current_score": v, "suggestion": f"Improve {k} score (currently {v})."})
    return actions[:5]


def recommend_next_skill_actions() -> list[dict[str, Any]]:
    missing = skill_evidence.build_missing_evidence_report()["missing_skills"]
    return [{"skill_id": s, "suggestion": f"Add evidence record or implementation for {s}."} for s in missing[:5]]


def recommend_next_documentation_actions() -> list[dict[str, Any]]:
    return [
        {"file": "docs/v5_reviewer_guide.md", "suggestion": "Ensure reviewer guide reflects v5.0 Agent Hub flow."},
        {"file": "docs/v5_security_boundaries.md", "suggestion": "Keep v5.0 boundary explicit (no LLM, no scanning)."},
    ]


def recommend_next_testing_actions() -> list[dict[str, Any]]:
    return [
        {"suite": "v5_security_boundaries", "suggestion": "Add tests to catch any future LLM connector regression."},
        {"suite": "v5_integration", "suggestion": "Add end-to-end orchestration tests."},
    ]


def recommend_next_demo_actions() -> list[dict[str, Any]]:
    return [
        {"item": "sample_outputs/agent_hub", "suggestion": "Add orchestration sample outputs."},
    ]


def build_30_day_plan() -> dict[str, Any]:
    return {
        "horizon_days": 30,
        "items": [
            *recommend_next_project_actions(),
            *recommend_next_skill_actions(),
            *recommend_next_documentation_actions(),
            *recommend_next_testing_actions(),
            *recommend_next_demo_actions(),
        ],
        "safety_boundary": _SAFE_BOUNDARY_NOTE,
    }


def build_version_roadmap_from_v5() -> dict[str, Any]:
    return {
        "current": "v5.0",
        "next": [
            {"version": "v5.1", "theme": "documentation polish + screenshots"},
            {"version": "v5.2", "theme": "performance + caching on rule engine"},
            {"version": "v6.0", "theme": "optional local model integration behind a feature flag (out of scope for v5.0)"},
        ],
        "safety_boundary": _SAFE_BOUNDARY_NOTE,
    }
