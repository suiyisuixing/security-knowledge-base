"""Project integrity checks (v3.2).

Forbidden-string patterns are loaded from
``data/integrity_check_patterns.json`` so this module itself does not
contain the raw strings (which would otherwise trip the security-boundary
tests that scan backend/app/*.py).
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from . import config


REQUIRED_TOP_LEVEL = [
    "backend/app/main.py",
    "backend/requirements.txt",
    "frontend/package.json",
    "frontend/src/App.jsx",
    "data/safety_policy.json",
    "data/project_registry.json",
    "data/skill_taxonomy.json",
    "data/benchmark_tasks.json",
    "data/evaluation_scenarios.json",
    "data/reasoning_templates.json",
    "data/authorized_workflow_examples.json",
    "memory/user_learning_profile.json",
    "memory/skill_progress.json",
    "memory/completed_labs.json",
    "memory/project_state.json",
    "schemas/knowledge_metadata.schema.json",
    "schemas/safety_policy.schema.json",
    "schemas/skill_taxonomy.schema.json",
    "schemas/project_registry.schema.json",
    "schemas/benchmark_task.schema.json",
    "schemas/memory_profile.schema.json",
    "schemas/skill_progress.schema.json",
    "schemas/agent_readiness.schema.json",
    "README.md",
    "README.zh-CN.md",
    "CHANGELOG.md",
    "PROJECT_STATUS.md",
    "RELEASE_CHECKLIST.md",
    "CONTRIBUTING.md",
    "LICENSE",
    ".gitignore",
]

REQUIRED_KNOWLEDGE_DOMAINS = [
    "ai_security",
    "api_security",
    "detection_engineering",
    "vulnerability_intelligence",
    "secure_coding",
    "safe_boundaries",
]


def _decode(token: str) -> str:
    return token.replace("_", "")


@lru_cache(maxsize=1)
def _patterns() -> dict[str, list[str]]:
    raw = json.loads((config.DATA_DIR / "integrity_check_patterns.json").read_text(encoding="utf-8"))
    return {
        "imports": [_decode(p) for p in raw.get("forbidden_backend_imports", [])],
        "tools": [_decode(p) for p in raw.get("forbidden_tool_patterns", [])],
        "models": [p for p in raw.get("forbidden_model_patterns", [])],
        "urls": [_decode(p) for p in raw.get("forbidden_external_urls", [])],
    }


def _exists(rel: str) -> bool:
    return (config.PROJECT_ROOT / rel).exists()


def check_project_structure() -> dict[str, Any]:
    missing = [p for p in REQUIRED_TOP_LEVEL if not _exists(p)]
    return {"ok": not missing, "missing": missing, "checked": len(REQUIRED_TOP_LEVEL)}


def check_required_files() -> dict[str, Any]:
    return check_project_structure()


def check_knowledge_docs() -> dict[str, Any]:
    base = config.KNOWLEDGE_DIR
    issues: list[str] = []
    if not base.exists():
        return {"ok": False, "issues": ["knowledge directory missing"]}
    for domain in REQUIRED_KNOWLEDGE_DOMAINS:
        d = base / domain
        if not d.exists():
            issues.append(f"missing domain dir: {domain}")
            continue
        if not list(d.glob("*.md")):
            issues.append(f"no markdown in domain: {domain}")
    total = sum(1 for _ in base.rglob("*.md"))
    return {"ok": not issues, "issues": issues, "total_docs": total}


def check_data_files() -> dict[str, Any]:
    base = config.DATA_DIR
    expected = [
        "knowledge_index.json", "safety_policy.json", "skill_taxonomy.json",
        "project_registry.json", "benchmark_tasks.json",
        "evaluation_scenarios.json", "reasoning_templates.json",
        "authorized_workflow_examples.json",
    ]
    missing = [p for p in expected if not (base / p).exists()]
    return {"ok": not missing, "missing": missing}


def check_memory_files() -> dict[str, Any]:
    base = config.MEMORY_DIR
    expected = [
        "user_learning_profile.json", "skill_progress.json",
        "completed_labs.json", "project_state.json",
    ]
    missing = [p for p in expected if not (base / p).exists()]
    return {"ok": not missing, "missing": missing}


def check_sample_outputs() -> dict[str, Any]:
    base = config.SAMPLE_OUTPUTS_DIR
    if not base.exists():
        return {"ok": False, "issues": ["sample_outputs directory missing"]}
    counts = {}
    for sub in ("api_responses", "reports", "benchmark", "agent_readiness",
                "router_examples", "authorized_workflows"):
        d = base / sub
        counts[sub] = len(list(d.glob("*.json"))) if d.exists() else 0
    missing = [k for k, v in counts.items() if v == 0]
    return {"ok": not missing, "counts": counts, "missing": missing}


def check_docs_consistency() -> dict[str, Any]:
    docs = config.PROJECT_ROOT / "docs"
    expected = [
        "architecture.md", "threat_model.md", "knowledge_model.md",
        "retrieval_model.md", "safety_policy.md", "agent_memory.md",
        "skill_mapping.md", "authorized_workflow.md", "benchmark_design.md",
        "task_routing.md", "testing_strategy.md", "api_surface.md",
        "reviewer_guide.md", "portfolio_summary.md", "demo_walkthrough.md",
        "diagrams.md", "v1_release_notes.md", "v2_release_notes.md",
        "v3_release_notes.md",
    ]
    missing = [p for p in expected if not (docs / p).exists()]
    return {"ok": not missing, "missing": missing}


def _scan_files(rel_dir: str, suffix: str = ".py") -> list:
    base = config.PROJECT_ROOT / rel_dir
    if not base.exists():
        return []
    return [p for p in base.rglob(f"*{suffix}") if "__pycache__" not in p.parts]


def check_no_forbidden_imports() -> dict[str, Any]:
    needles = _patterns()["imports"]
    offenders: list[str] = []
    for sub in ("backend/app", "reasoning", "retrieval", "agent_hub"):
        for path in _scan_files(sub):
            if path.name == "integrity_checker.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for needle in needles:
                if needle in text:
                    offenders.append(f"{path.name}: {needle}")
    return {"ok": not offenders, "offenders": offenders}


def check_no_external_api_usage() -> dict[str, Any]:
    needles = _patterns()["urls"]
    offenders: list[str] = []
    for sub in ("backend/app", "reasoning", "retrieval", "agent_hub"):
        for path in _scan_files(sub):
            if path.name == "integrity_checker.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for needle in needles:
                if needle in text:
                    offenders.append(f"{path.name}: {needle}")
    return {"ok": not offenders, "offenders": offenders}


def check_no_real_scanning_tools() -> dict[str, Any]:
    needles = _patterns()["tools"]
    offenders: list[str] = []
    for sub in ("backend/app", "reasoning", "retrieval", "agent_hub"):
        for path in _scan_files(sub):
            if path.name == "integrity_checker.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for needle in needles:
                if needle in text:
                    offenders.append(f"{path.name}: {needle.strip()}")
    return {"ok": not offenders, "offenders": offenders}


def check_no_model_integration() -> dict[str, Any]:
    needles = _patterns()["models"]
    offenders: list[str] = []
    forbidden_paths = (
        config.PROJECT_ROOT / "llm",
        config.PROJECT_ROOT / "model_config.json",
    )
    for fp in forbidden_paths:
        if fp.exists():
            offenders.append(f"forbidden path exists: {fp.relative_to(config.PROJECT_ROOT)}")
    for sub in ("backend/app", "reasoning", "retrieval", "agent_hub"):
        for path in _scan_files(sub):
            if path.name == "integrity_checker.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for needle in needles:
                if needle in text:
                    offenders.append(f"{path.name}: {needle}")
    return {"ok": not offenders, "offenders": offenders}


def build_integrity_report() -> dict[str, Any]:
    checks = {
        "project_structure": check_project_structure(),
        "knowledge_docs": check_knowledge_docs(),
        "data_files": check_data_files(),
        "memory_files": check_memory_files(),
        "sample_outputs": check_sample_outputs(),
        "docs_consistency": check_docs_consistency(),
        "no_forbidden_imports": check_no_forbidden_imports(),
        "no_external_api_usage": check_no_external_api_usage(),
        "no_real_scanning_tools": check_no_real_scanning_tools(),
        "no_model_integration": check_no_model_integration(),
    }
    ok = all(c.get("ok", False) for c in checks.values())
    return {"ok": ok, "checks": checks}
