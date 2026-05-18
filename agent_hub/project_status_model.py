"""Pydantic models for project status (v5.0)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ProjectCapability(BaseModel):
    name: str
    description: str = ""


class ProjectArtifact(BaseModel):
    path: str
    kind: str = "file"


class ProjectSkillEvidence(BaseModel):
    skill_id: str
    project_id: str
    evidence_type: str
    artifacts: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    status: str = "documented"


class ProjectMaturityScore(BaseModel):
    project_id: str
    level: int
    name: str = ""
    notes: str = ""


class ProjectStatus(BaseModel):
    project_id: str
    name: str
    focus: str = ""
    capabilities: list[str] = Field(default_factory=list)
    known_artifacts: list[str] = Field(default_factory=list)
    skill_coverage: list[str] = Field(default_factory=list)
    maturity_level: int = 1
    status: str = ""


def validate_project_status(status: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if not status.get("project_id"):
        issues.append("missing project_id")
    if not status.get("name"):
        issues.append("missing name")
    if status.get("maturity_level") is not None and not isinstance(status["maturity_level"], int):
        issues.append("maturity_level must be int")
    return issues


def summarize_project_status(status: dict[str, Any]) -> str:
    return (
        f"{status.get('project_id','?')} (level {status.get('maturity_level','?')}) — "
        f"{status.get('focus','')}"
    )
