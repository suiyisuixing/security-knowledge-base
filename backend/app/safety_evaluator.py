"""Safety policy evaluation harness."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from . import config
from . import safety_policy


@lru_cache(maxsize=1)
def load_safety_evaluation_cases() -> list[dict[str, Any]]:
    with (config.DATA_DIR / "benchmark_tasks.json").open("r", encoding="utf-8") as f:
        data = json.load(f)
    return [t for t in data.get("tasks", []) if t.get("type") == "safety_classification"]


def evaluate_single_safety_case(case: dict[str, Any]) -> dict[str, Any]:
    cls = safety_policy.classify_request(case["input"])
    expected = case.get("expected_output", {}).get("classification")
    return {
        "case_id": case["task_id"],
        "expected": expected,
        "actual": cls["classification"],
        "passed": cls["classification"] == expected,
    }


def evaluate_safety_policy() -> list[dict[str, Any]]:
    return [evaluate_single_safety_case(c) for c in load_safety_evaluation_cases()]


def summarize_safety_evaluation(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    if not total:
        return {"total": 0, "passed": 0, "pass_rate": 0.0}
    passed = sum(1 for r in results if r["passed"])
    return {"total": total, "passed": passed, "pass_rate": round(passed / total, 4)}
