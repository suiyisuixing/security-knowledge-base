"""Project adapter — bundled metadata only (v5.0)."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from app import config
from app import project_registry as legacy_registry


@lru_cache(maxsize=1)
def load_project_status_samples() -> dict[str, Any]:
    path = config.DATA_DIR / "project_status_samples.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_project_registry() -> dict[str, Any]:
    return legacy_registry.load_project_registry()


def _get_sample(project_id: str) -> dict[str, Any] | None:
    for s in load_project_status_samples().get("samples", []):
        if s["project_id"] == project_id:
            return s
    return None


def get_project_capabilities(project_id: str) -> list[str]:
    sample = _get_sample(project_id) or {}
    return list(sample.get("capabilities", []) or [])


def get_project_known_artifacts(project_id: str) -> list[str]:
    sample = _get_sample(project_id) or {}
    return list(sample.get("known_artifacts", []) or [])


def get_project_skill_coverage(project_id: str) -> list[str]:
    sample = _get_sample(project_id) or {}
    return list(sample.get("skill_coverage", []) or [])


def build_project_adapter_summary(project_id: str) -> dict[str, Any]:
    sample = _get_sample(project_id) or {}
    registry = legacy_registry.get_project(project_id) or {}
    return {
        "project_id": project_id,
        "name": sample.get("name") or registry.get("name") or project_id,
        "focus": sample.get("focus") or registry.get("focus") or "",
        "capabilities": get_project_capabilities(project_id),
        "known_artifacts": get_project_known_artifacts(project_id),
        "skill_coverage": get_project_skill_coverage(project_id),
        "maturity_level": sample.get("maturity_level", 1),
        "status": sample.get("status") or registry.get("status") or "",
        "repo": registry.get("repo", ""),
    }
