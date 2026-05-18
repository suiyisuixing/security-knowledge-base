"""Pydantic models for API requests, responses, and internal data."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class KnowledgeMetadata(BaseModel):
    id: str
    title: str
    domain: str
    difficulty: str = "easy"
    related_projects: list[str] = Field(default_factory=list)
    related_skills: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    safe_use: list[str] = Field(default_factory=list)
    forbidden_use: list[str] = Field(default_factory=list)


class KnowledgeDocument(BaseModel):
    metadata: KnowledgeMetadata
    body: str
    path: str


class SearchRequest(BaseModel):
    query: str
    domain: str | None = None
    top_k: int = 5


class SearchResult(BaseModel):
    doc_id: str
    title: str
    domain: str
    score: float
    snippet: str


class Citation(BaseModel):
    doc_id: str
    title: str
    domain: str


class AskRequest(BaseModel):
    query: str
    domain: str | None = None
    top_k: int = 5


class AskResponse(BaseModel):
    query: str
    answer: str
    citations: list[Citation]
    safety_note: str
    related_skills: list[str]
    related_projects: list[str]


class SafetyClassificationRequest(BaseModel):
    text: str


class SafetyClassificationResponse(BaseModel):
    classification: str
    allowed: bool
    reason: str
    safe_redirect: str
    explanation: str


class SkillProgress(BaseModel):
    skill_id: str
    status: str
    notes: str | None = None


class MemoryProfile(BaseModel):
    profile_id: str
    display_name: str
    goals: list[str]
    preferences: dict[str, Any]
    skill_progress: list[SkillProgress]
    completed_labs: list[dict[str, Any]]


class SkillUpdateRequest(BaseModel):
    skill_id: str
    status: str
    notes: str | None = None


class SkillItem(BaseModel):
    skill_id: str
    name: str
    domain: str
    description: str
    related_projects: list[str]


class ProjectRegistryItem(BaseModel):
    project_id: str
    name: str
    focus: str
    repo: str
    skills: list[str]
    status: str


class LearningPathRequest(BaseModel):
    goal: str
    current_skills: list[str] | None = None


class LearningPathStep(BaseModel):
    step: int
    skill_id: str
    title: str
    notes: str


class LearningPathResponse(BaseModel):
    goal: str
    steps: list[LearningPathStep]
    summary: str


class ContextBuildRequest(BaseModel):
    query: str
    top_k: int = 3


class ContextBuildResponse(BaseModel):
    query: str
    retrieved: list[SearchResult]
    related_skills: list[str]
    related_projects: list[str]
    safety_classification: str
    safety_allowed: bool
    safe_boundary: str
    recommended_next_step: str


class KnowledgeQualityResult(BaseModel):
    doc_id: str
    score: float
    components: dict[str, float]


class CitationEvaluationResult(BaseModel):
    cited_docs_exist: bool
    safety_note_present: bool
    unsupported_claims: list[str]
    notes: str


class SafetyEvaluationResult(BaseModel):
    case_id: str
    expected: str
    actual: str
    passed: bool


class ReasoningTemplate(BaseModel):
    template_id: str
    name: str
    domain: str
    steps: list[str]
    forbidden_steps: list[str]


class AuthorizedWorkflowRequest(BaseModel):
    request: str
    declared_scope: str | None = None


class AuthorizedWorkflowResponse(BaseModel):
    workflow_id: str
    allowed: bool
    required_scope: str
    steps: list[str]
    blocked_actions: list[str]
    summary: str


class TaskRouteRequest(BaseModel):
    query: str


class TaskRouteResponse(BaseModel):
    query: str
    project_id: str
    knowledge_domain: str
    skill_id: str
    explanation: str


class BenchmarkTask(BaseModel):
    task_id: str
    domain: str
    type: str
    input: str
    expected_output: dict[str, Any]
    rubric: dict[str, Any]


class BenchmarkRunResult(BaseModel):
    task_id: str
    type: str
    passed: bool
    detail: str


class ReportResponse(BaseModel):
    title: str
    sections: list[dict[str, Any]]
    markdown: str


class ApiSurfaceItem(BaseModel):
    method: str
    path: str
    summary: str
