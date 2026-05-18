"""Learning path generation."""

from __future__ import annotations

from typing import Any

from . import skill_mapper


def _to_step(idx: int, skill_id: str, title: str, notes: str) -> dict[str, Any]:
    return {"step": idx, "skill_id": skill_id, "title": title, "notes": notes}


def generate_ai_security_path() -> list[dict[str, Any]]:
    return [
        _to_step(1, "prompt_injection_reasoning", "Prompt Injection Reasoning", "Study direct injection in a local RAG."),
        _to_step(2, "rag_access_control", "RAG Access Control", "Enforce ACLs at retrieval time."),
        _to_step(3, "secure_retrieval_design", "Secure Retrieval Design", "Design provenance-aware pipelines."),
    ]


def generate_detection_engineering_path() -> list[dict[str, Any]]:
    return [
        _to_step(1, "log_analysis", "Log Analysis", "Practice on synthetic logs."),
        _to_step(2, "mitre_mapping", "MITRE Mapping", "Map detections to ATT&CK."),
        _to_step(3, "alert_triage", "Alert Triage", "Build a triage playbook."),
        _to_step(4, "detection_engineering", "Detection Engineering", "Write Sigma rules and test them."),
    ]


def generate_vulnerability_intelligence_path() -> list[dict[str, Any]]:
    return [
        _to_step(1, "vulnerability_prioritization", "Vulnerability Prioritization", "Combine CVSS, KEV, EPSS."),
        _to_step(2, "dependency_risk_reasoning", "Dependency Risk Reasoning", "Apply SBOM reasoning."),
        _to_step(3, "safe_verification_planning", "Safe Verification Planning", "Draft minimal verification plans."),
    ]


def generate_secure_code_review_path() -> list[dict[str, Any]]:
    return [
        _to_step(1, "secure_code_review", "Secure Code Review", "Review handlers for auth and validation."),
        _to_step(2, "configuration_review", "Configuration Review", "Compare against a baseline."),
        _to_step(3, "api_authorization_reasoning", "API Authorization Reasoning", "Cover BOLA, BFLA, BOPLA."),
    ]


def generate_learning_path(goal: str, current_skills: list[str] | None = None) -> dict[str, Any]:
    g = (goal or "").lower()
    current = set(current_skills or [])
    if "detection" in g or "soc" in g:
        steps = generate_detection_engineering_path()
    elif "vulnerability" in g or "cve" in g or "patch" in g:
        steps = generate_vulnerability_intelligence_path()
    elif "code" in g or "secure coding" in g:
        steps = generate_secure_code_review_path()
    elif "ai" in g or "rag" in g or "llm" in g:
        steps = generate_ai_security_path()
    else:
        recs = skill_mapper.recommend_skills_for_goal(goal) or [
            "safety_boundary_classification", "safe_verification_planning", "task_routing",
        ]
        steps = [
            _to_step(i + 1, s, s.replace("_", " ").title(), "Recommended for stated goal.")
            for i, s in enumerate(recs)
        ]
    if current:
        for s in steps:
            if s["skill_id"] in current:
                s["notes"] = "Already in progress: " + s["notes"]
    summary = f"Learning path with {len(steps)} steps for goal: {goal.strip() or 'general'}."
    return {"goal": goal, "steps": steps, "summary": summary}


def summarize_learning_path(path: dict[str, Any]) -> str:
    steps = path.get("steps", [])
    return f"{len(steps)} steps targeting goal: {path.get('goal', '')}"
