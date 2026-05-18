"""Portfolio maturity model (v5.0)."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from app import config
from . import project_adapter


@lru_cache(maxsize=1)
def load_maturity_model() -> dict[str, Any]:
    return json.loads((config.DATA_DIR / "portfolio_maturity_model.json").read_text(encoding="utf-8"))


def _level_name(level: int) -> str:
    for lv in load_maturity_model().get("levels", []):
        if lv.get("level") == level:
            return lv.get("name", "")
    return ""


def score_project_against_model(project_id: str) -> dict[str, Any]:
    summary = project_adapter.build_project_adapter_summary(project_id)
    level = int(summary.get("maturity_level", 1))
    return {
        "project_id": project_id,
        "level": level,
        "name": _level_name(level),
        "skills": summary.get("skill_coverage", []),
        "capabilities": summary.get("capabilities", []),
    }


def score_all_projects() -> list[dict[str, Any]]:
    samples = project_adapter.load_project_status_samples().get("samples", [])
    return [score_project_against_model(s["project_id"]) for s in samples]


def summarize_maturity_scores() -> dict[str, Any]:
    scores = score_all_projects()
    by_level: dict[int, int] = {}
    for s in scores:
        by_level[s["level"]] = by_level.get(s["level"], 0) + 1
    return {
        "total": len(scores),
        "by_level": by_level,
        "avg_level": round(sum(s["level"] for s in scores) / max(1, len(scores)), 2),
    }


def recommend_maturity_improvements() -> list[dict[str, Any]]:
    suggestions: list[dict[str, Any]] = []
    for s in score_all_projects():
        if s["level"] < 5:
            suggestions.append({
                "project_id": s["project_id"],
                "current_level": s["level"],
                "target_level": min(5, s["level"] + 1),
                "suggestion": (
                    f"Promote {s['project_id']} from level {s['level']} ({_level_name(s['level'])}) "
                    f"to level {min(5, s['level'] + 1)} ({_level_name(min(5, s['level'] + 1))})."
                ),
            })
    return suggestions
