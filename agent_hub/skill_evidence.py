"""Skill evidence tracker (v5.0)."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from app import config


@lru_cache(maxsize=1)
def _load() -> dict[str, Any]:
    return json.loads((config.DATA_DIR / "skill_evidence_map.json").read_text(encoding="utf-8"))


def load_skill_evidence_map() -> dict[str, Any]:
    return _load()


def get_evidence_for_skill(skill_id: str) -> list[dict[str, Any]]:
    return [r for r in _load().get("records", []) if r.get("skill_id") == skill_id]


def get_evidence_for_project(project_id: str) -> list[dict[str, Any]]:
    return [r for r in _load().get("records", []) if r.get("project_id") == project_id]


_DYNAMIC_RECORDS: list[dict[str, Any]] = []


def add_evidence_record(skill_id: str, project_id: str, artifact_path: str,
                        evidence_type: str = "code", confidence: float = 0.5) -> dict[str, Any]:
    record = {
        "skill_id": skill_id,
        "project_id": project_id,
        "evidence_type": evidence_type,
        "artifacts": [artifact_path],
        "confidence": float(confidence),
        "status": "implemented" if confidence >= 0.8 else "documented",
    }
    _DYNAMIC_RECORDS.append(record)
    return record


def score_skill_evidence(skill_id: str) -> float:
    records = get_evidence_for_skill(skill_id) + [r for r in _DYNAMIC_RECORDS if r["skill_id"] == skill_id]
    if not records:
        return 0.0
    return round(sum(r.get("confidence", 0.0) for r in records) / len(records), 4)


def score_project_evidence(project_id: str) -> float:
    records = get_evidence_for_project(project_id) + [r for r in _DYNAMIC_RECORDS if r["project_id"] == project_id]
    if not records:
        return 0.0
    return round(sum(r.get("confidence", 0.0) for r in records) / len(records), 4)


def build_skill_evidence_report() -> dict[str, Any]:
    records = list(_load().get("records", [])) + list(_DYNAMIC_RECORDS)
    by_skill: dict[str, list[dict[str, Any]]] = {}
    for r in records:
        by_skill.setdefault(r["skill_id"], []).append(r)
    items: list[dict[str, Any]] = []
    for skill_id, recs in sorted(by_skill.items()):
        items.append({
            "skill_id": skill_id,
            "records": recs,
            "score": round(sum(r.get("confidence", 0.0) for r in recs) / len(recs), 4),
        })
    return {"count": len(items), "items": items}


def build_missing_evidence_report() -> dict[str, Any]:
    from app import skill_mapper
    all_skills = {s["skill_id"] for s in skill_mapper.list_skills()}
    covered = {r["skill_id"] for r in _load().get("records", [])} | {r["skill_id"] for r in _DYNAMIC_RECORDS}
    missing = sorted(all_skills - covered)
    return {"count": len(missing), "missing_skills": missing}
