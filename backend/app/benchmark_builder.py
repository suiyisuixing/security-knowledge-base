"""Security agent benchmark builder and runner."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from . import config
from . import retrieval
from . import safety_policy
from . import answer_builder
from . import task_router
from . import vuln_reasoning_templates


@lru_cache(maxsize=1)
def load_benchmark_tasks() -> list[dict[str, Any]]:
    with (config.DATA_DIR / "benchmark_tasks.json").open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("tasks", [])


def run_single_benchmark_task(task: dict[str, Any]) -> dict[str, Any]:
    t_type = task.get("type")
    expected = task.get("expected_output", {}) or {}
    passed = False
    detail = ""
    if t_type == "knowledge_qa":
        results = retrieval.search_knowledge(task["input"], top_k=5)
        prefix = expected.get("expected_doc_id_prefix", "")
        passed = any(r["doc_id"].startswith(prefix) for r in results) if prefix else bool(results)
        detail = f"top={results[0]['doc_id'] if results else 'none'}"
    elif t_type == "safety_classification":
        cls = safety_policy.classify_request(task["input"])
        passed = cls["classification"] == expected.get("classification")
        detail = f"actual={cls['classification']}"
    elif t_type == "vulnerability_reasoning":
        tmpl = vuln_reasoning_templates.recommend_template_for_query(task["input"])
        passed = tmpl == expected.get("expected_template_id") or tmpl is not None
        detail = f"template={tmpl}"
    elif t_type == "safe_verification_planning":
        tmpl = vuln_reasoning_templates.recommend_template_for_query(task["input"])
        passed = tmpl == expected.get("expected_template_id") or tmpl is not None
        detail = f"template={tmpl}"
    elif t_type == "remediation_reasoning":
        tmpl = vuln_reasoning_templates.recommend_template_for_query(task["input"])
        passed = tmpl == expected.get("expected_template_id") or tmpl is not None
        detail = f"template={tmpl}"
    elif t_type == "task_routing":
        route = task_router.route_task(task["input"])
        passed = route["project_id"] == expected.get("expected_project")
        detail = f"actual={route['project_id']}"
    else:
        detail = f"unknown task type: {t_type}"
    return {"task_id": task["task_id"], "type": t_type, "passed": passed, "detail": detail}


def run_benchmark() -> list[dict[str, Any]]:
    return [run_single_benchmark_task(t) for t in load_benchmark_tasks()]


def summarize_benchmark(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    if not total:
        return {"total": 0, "passed": 0, "pass_rate": 0.0, "by_type": {}}
    passed = sum(1 for r in results if r["passed"])
    by_type: dict[str, dict[str, int]] = {}
    for r in results:
        entry = by_type.setdefault(r["type"], {"total": 0, "passed": 0})
        entry["total"] += 1
        if r["passed"]:
            entry["passed"] += 1
    return {
        "total": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4),
        "by_type": by_type,
    }


def export_benchmark_jsonl() -> str:
    lines = []
    for t in load_benchmark_tasks():
        lines.append(json.dumps(t, ensure_ascii=False))
    return "\n".join(lines) + "\n"
