"""Roadmap planner (v5.0)."""

from __future__ import annotations

from typing import Any


def build_v5_roadmap() -> dict[str, Any]:
    return {
        "version": "v5.0-rc",
        "themes": [
            "Rule-based agent hub",
            "Hybrid retrieval with citation grounding",
            "Cross-project skill evidence tracking",
            "Portfolio readiness scoring",
        ],
        "milestones": [
            {"id": "v3.1", "done": True, "title": "Reviewer Experience"},
            {"id": "v3.2", "done": True, "title": "Stability / Schema"},
            {"id": "v4.0", "done": True, "title": "Rule-based Reasoning"},
            {"id": "v4.5", "done": True, "title": "Hybrid Retrieval"},
            {"id": "v5.0", "done": True, "title": "Agent Hub Control Plane"},
        ],
    }


def build_v5_to_v6_roadmap() -> dict[str, Any]:
    return {
        "from": "v5.0-rc",
        "to": "v6.0",
        "key_decision": "v6.0 introduces an *optional* local LLM connector behind a feature flag; it stays off by default.",
        "milestones": [
            {"id": "v5.1", "title": "Docs polish + screenshots"},
            {"id": "v5.2", "title": "Caching for rule engine + hybrid retrieval"},
            {"id": "v6.0", "title": "Optional local model connector behind a feature flag; default off"},
        ],
        "constraints": [
            "Default build never calls a model.",
            "Feature flag must be off in CI and in the bundled distribution.",
            "Safety policy and authorized workflow remain authoritative.",
        ],
    }


def build_release_checklist(version: str) -> dict[str, Any]:
    return {
        "version": version,
        "items": [
            "pytest pass",
            "compileall pass",
            "npm run build pass",
            "tools/run_checks.py pass",
            "no .venv / node_modules / dist / .vite committed",
            "no real secrets / API keys / target data",
            "no unauthorized scanning",
            "no exploit code",
            "README + README.zh-CN render",
            "CHANGELOG updated",
            "Author = suiyisuixing",
        ],
    }


def build_github_release_notes(version: str) -> str:
    return (
        f"# {version}\n\n"
        "Model-free agent hub release. Adds rule-based reasoning, hybrid retrieval, "
        "cross-project skill evidence, portfolio readiness scoring, and an "
        "orchestrator that routes queries across the A/B/C/D portfolio without any "
        "external API or model.\n\n"
        "## Boundaries\n\n"
        "Local-only, defensive, deterministic. No LLM, no real scanning, no exploit code.\n"
    )
