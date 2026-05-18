"""Agent memory store (JSON files under memory/).

No databases, no sensitive personal data. All paths constrained to MEMORY_DIR.
"""

from __future__ import annotations

import json
from typing import Any

from . import config

PROFILE_FILE = "user_learning_profile.json"
SKILL_PROGRESS_FILE = "skill_progress.json"
COMPLETED_LABS_FILE = "completed_labs.json"
PROJECT_STATE_FILE = "project_state.json"


def _read(filename: str) -> dict[str, Any]:
    path = config.safe_resolve_memory_path(filename)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write(filename: str, data: dict[str, Any]) -> None:
    path = config.safe_resolve_memory_path(filename)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_memory_profile() -> dict[str, Any]:
    profile = _read(PROFILE_FILE)
    progress = _read(SKILL_PROGRESS_FILE).get("skills", [])
    completed = _read(COMPLETED_LABS_FILE).get("completed_labs", [])
    return {
        "profile_id": profile.get("profile_id", "default-learning-profile"),
        "display_name": profile.get("display_name", "Portfolio Author"),
        "goals": profile.get("goals", []),
        "preferences": profile.get("preferences", {}),
        "skill_progress": progress,
        "completed_labs": completed,
    }


def save_memory_profile(profile: dict[str, Any]) -> None:
    base = {
        "profile_id": profile.get("profile_id", "default-learning-profile"),
        "display_name": profile.get("display_name", "Portfolio Author"),
        "goals": profile.get("goals", []),
        "preferences": profile.get("preferences", {}),
        "created_at": profile.get("created_at", ""),
        "notes": profile.get("notes", ""),
    }
    _write(PROFILE_FILE, base)


def get_skill_progress() -> list[dict[str, Any]]:
    return _read(SKILL_PROGRESS_FILE).get("skills", [])


def update_skill_progress(skill_id: str, status: str, notes: str | None = None) -> list[dict[str, Any]]:
    data = _read(SKILL_PROGRESS_FILE)
    skills = data.get("skills", [])
    found = False
    for s in skills:
        if s.get("skill_id") == skill_id:
            s["status"] = status
            if notes is not None:
                s["notes"] = notes
            found = True
            break
    if not found:
        skills.append({"skill_id": skill_id, "status": status, "notes": notes or ""})
    data["skills"] = skills
    _write(SKILL_PROGRESS_FILE, data)
    return skills


def add_completed_lab(lab_id: str, related_project: str) -> list[dict[str, Any]]:
    data = _read(COMPLETED_LABS_FILE)
    labs = data.get("completed_labs", [])
    for existing in labs:
        if existing.get("lab_id") == lab_id:
            existing["related_project"] = related_project
            _write(COMPLETED_LABS_FILE, data)
            return labs
    labs.append({"lab_id": lab_id, "related_project": related_project, "completed_at": ""})
    data["completed_labs"] = labs
    _write(COMPLETED_LABS_FILE, data)
    return labs


def recommend_next_skills() -> list[str]:
    progress = get_skill_progress()
    return [s["skill_id"] for s in progress if s.get("status") == "planned"]


def summarize_memory() -> dict[str, Any]:
    profile = load_memory_profile()
    progress = profile.get("skill_progress", [])
    completed = profile.get("completed_labs", [])
    by_status: dict[str, int] = {}
    for s in progress:
        by_status[s.get("status", "unknown")] = by_status.get(s.get("status", "unknown"), 0) + 1
    return {
        "profile_id": profile.get("profile_id"),
        "skill_count": len(progress),
        "by_status": by_status,
        "completed_lab_count": len(completed),
    }
