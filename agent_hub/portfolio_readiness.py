"""Portfolio readiness scoring (v5.0)."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from app import config
from app import knowledge_loader
from . import project_adapter
from . import skill_evidence


@lru_cache(maxsize=1)
def _load_model() -> dict[str, Any]:
    return json.loads((config.DATA_DIR / "portfolio_maturity_model.json").read_text(encoding="utf-8"))


def calculate_project_maturity(project_id: str) -> dict[str, Any]:
    summary = project_adapter.build_project_adapter_summary(project_id)
    return {
        "project_id": project_id,
        "level": summary.get("maturity_level", 1),
        "skill_coverage_count": len(summary.get("skill_coverage", [])),
        "capabilities_count": len(summary.get("capabilities", [])),
    }


def calculate_skill_coverage() -> float:
    from app import skill_mapper
    skills = [s["skill_id"] for s in skill_mapper.list_skills()]
    if not skills:
        return 0.0
    covered = sum(1 for s in skills if skill_evidence.get_evidence_for_skill(s))
    return round(covered / len(skills), 4)


def calculate_documentation_score() -> float:
    docs_dir = config.PROJECT_ROOT / "docs"
    if not docs_dir.exists():
        return 0.0
    count = len(list(docs_dir.glob("*.md")))
    return min(1.0, round(count / 20.0, 4))


def calculate_testing_score() -> float:
    tests_dir = config.PROJECT_ROOT / "tests"
    if not tests_dir.exists():
        return 0.0
    count = len(list(tests_dir.glob("test_*.py")))
    return min(1.0, round(count / 30.0, 4))


def calculate_safety_score() -> float:
    safety = config.DATA_DIR / "safety_policy.json"
    if not safety.exists():
        return 0.0
    return 0.95


def calculate_demo_score() -> float:
    base = config.SAMPLE_OUTPUTS_DIR
    if not base.exists():
        return 0.0
    total = sum(1 for _ in base.rglob("*.json"))
    return min(1.0, round(total / 15.0, 4))


def calculate_overall_portfolio_readiness() -> dict[str, Any]:
    categories = {
        "project_structure": 1.0 if (config.PROJECT_ROOT / "backend").exists() else 0.0,
        "documentation": calculate_documentation_score(),
        "tests": calculate_testing_score(),
        "security_boundaries": calculate_safety_score(),
        "demo_quality": calculate_demo_score(),
        "skill_coverage": calculate_skill_coverage(),
        "cross_project_integration": 1.0 if (config.DATA_DIR / "project_status_samples.json").exists() else 0.0,
        "retrieval_quality": 1.0 if (config.PROJECT_ROOT / "retrieval" / "hybrid.py").exists() else 0.0,
        "rule_based_reasoning": 1.0 if (config.PROJECT_ROOT / "reasoning" / "rule_engine.py").exists() else 0.0,
        "reviewer_experience": 1.0 if (config.PROJECT_ROOT / "sample_outputs").exists() else 0.0,
    }
    weights = _load_model().get("category_weights", {})
    overall = 0.0
    for k, v in categories.items():
        overall += v * weights.get(k, 0.1)
    return {
        "categories": categories,
        "overall": round(min(overall, 1.0), 4),
        "version": config.get_project_version(),
    }


def build_portfolio_readiness_report() -> dict[str, Any]:
    base = calculate_overall_portfolio_readiness()
    by_project = []
    for s in project_adapter.load_project_status_samples().get("samples", []):
        by_project.append(calculate_project_maturity(s["project_id"]))
    return {
        **base,
        "per_project": by_project,
        "knowledge_summary": knowledge_loader.summarize_knowledge_base(),
    }
