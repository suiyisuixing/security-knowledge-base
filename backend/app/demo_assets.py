"""Demo sample outputs and reviewer-mode helpers (v3.1).

Pre-generated, deterministic sample outputs let reviewers see expected
shapes without running the full pipeline. All samples are bundled under
``sample_outputs/`` and are read locally only.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from . import config


_SAMPLE_SUBDIRS = (
    "api_responses",
    "reports",
    "benchmark",
    "agent_readiness",
    "router_examples",
    "authorized_workflows",
)


@lru_cache(maxsize=1)
def _scan_samples() -> dict[str, dict[str, Any]]:
    base = config.SAMPLE_OUTPUTS_DIR
    out: dict[str, dict[str, Any]] = {}
    if not base.exists():
        return out
    for sub in _SAMPLE_SUBDIRS:
        sub_dir = base / sub
        if not sub_dir.exists():
            continue
        for path in sorted(sub_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            sample_id = data.get("sample_id") or path.stem
            data["_group"] = sub
            data["_path"] = f"sample_outputs/{sub}/{path.name}"
            out[sample_id] = data
    return out


def list_demo_samples() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for sid, data in _scan_samples().items():
        items.append({
            "sample_id": sid,
            "group": data.get("_group", ""),
            "endpoint": data.get("endpoint", ""),
            "path": data.get("_path", ""),
        })
    items.sort(key=lambda x: (x["group"], x["sample_id"]))
    return items


def get_demo_sample(sample_id: str) -> dict[str, Any] | None:
    return _scan_samples().get(sample_id)


def build_reviewer_path() -> dict[str, Any]:
    return {
        "version": config.get_project_version(),
        "title": "Reviewer Quick Path",
        "steps": [
            {"step": 1, "action": "Load knowledge domains", "endpoint": "GET /knowledge/domains"},
            {"step": 2, "action": "Search for a security concept", "endpoint": "POST /knowledge/search"},
            {"step": 3, "action": "Ask a knowledge-grounded question", "endpoint": "POST /knowledge/ask"},
            {"step": 4, "action": "Classify an allowed request", "endpoint": "POST /safety/classify"},
            {"step": 5, "action": "Classify a needs-confirmation request", "endpoint": "POST /safety/classify"},
            {"step": 6, "action": "Classify a blocked request", "endpoint": "POST /safety/classify"},
            {"step": 7, "action": "Generate a learning path", "endpoint": "POST /learning-path/generate"},
            {"step": 8, "action": "Build an authorized workflow plan", "endpoint": "POST /workflow/authorized-plan"},
            {"step": 9, "action": "Route a task to A/B/C/D", "endpoint": "POST /router/route-task"},
            {"step": 10, "action": "Run benchmark", "endpoint": "POST /benchmark/run"},
            {"step": 11, "action": "Generate agent readiness report", "endpoint": "POST /report/agent-readiness"},
            {"step": 12, "action": "Review portfolio value summary", "endpoint": "GET /demo/portfolio-summary"},
        ],
        "safety_boundary": (
            "Local-only, model-free, defensive. The system does not support "
            "unauthorized scanning or exploitation."
        ),
    }


def build_portfolio_demo_summary() -> dict[str, Any]:
    return {
        "version": config.get_project_version(),
        "name": "Security Knowledge Base & Agent Memory Lab",
        "tagline": "Local cybersecurity knowledge base, retrieval, safety policy, agent memory, task routing, and benchmark platform.",
        "value": [
            "Defensive, model-free architecture suitable for public portfolio review.",
            "Knowledge-grounded answers with citations and explicit safety notes.",
            "Rule-based safety policy classifier with 20 categories.",
            "Authorized workflow planner (planning artifacts only — no execution).",
            "Task router across the A/B/C/D portfolio.",
            "Agent memory tracker with skill progress.",
            "60-task benchmark suite covering knowledge, safety, reasoning, planning, and routing.",
        ],
        "portfolio_links": [
            {"project_id": "llm-security-lab", "focus": "AI/RAG Security Evaluation"},
            {"project_id": "security-log-ai-assistant", "focus": "Detection Engineering / SOC Workflow"},
            {"project_id": "vulnerability-intelligence-lab", "focus": "Vulnerability Intelligence"},
            {"project_id": "security-knowledge-base", "focus": "Knowledge / Safety / Memory / Routing / Agent Hub"},
        ],
        "boundary": (
            "This is a local-only, model-free, defensive, authorized-scope portfolio "
            "project. It does not use LLMs, perform real scanning, or execute exploitation."
        ),
    }


def validate_sample_outputs() -> dict[str, Any]:
    samples = _scan_samples()
    issues: list[str] = []
    required_groups = set(_SAMPLE_SUBDIRS)
    seen_groups = {s.get("_group", "") for s in samples.values()}
    for missing in sorted(required_groups - seen_groups):
        issues.append(f"missing group: {missing}")
    for sid, data in samples.items():
        if "endpoint" not in data and "response" not in data and "report_excerpt" not in data:
            issues.append(f"sample '{sid}' missing endpoint or response payload")
    return {
        "total": len(samples),
        "groups": sorted(seen_groups),
        "issues": issues,
        "ok": not issues,
    }
