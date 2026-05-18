"""Evaluation scenarios runner."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from . import config
from . import retrieval
from . import safety_policy
from . import answer_builder
from . import task_router


@lru_cache(maxsize=1)
def load_evaluation_scenarios() -> dict[str, Any]:
    with (config.DATA_DIR / "evaluation_scenarios.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def run_single_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    s_type = scenario.get("type")
    passed = False
    detail = ""
    if s_type == "knowledge_search":
        results = retrieval.search_knowledge(scenario["input"], top_k=5)
        prefix = scenario.get("expected_doc_id_prefix", "")
        passed = any(r["doc_id"].startswith(prefix) for r in results) if prefix else bool(results)
        detail = f"top={results[0]['doc_id'] if results else 'none'}"
    elif s_type == "safety_classification":
        cls = safety_policy.classify_request(scenario["input"])
        expected = scenario.get("expected_classification")
        passed = cls["classification"] == expected
        detail = f"actual={cls['classification']} expected={expected}"
    elif s_type == "answer_citations":
        results = retrieval.search_knowledge(scenario["input"], top_k=5)
        answer = answer_builder.build_grounded_answer(scenario["input"], results)
        min_c = scenario.get("expected_min_citations", 1)
        has_note = bool(answer.get("safety_note"))
        passed = len(answer["citations"]) >= min_c and (has_note if scenario.get("must_include_safety_note") else True)
        detail = f"citations={len(answer['citations'])}, safety_note={has_note}"
    elif s_type == "task_routing":
        route = task_router.route_task(scenario["input"])
        expected = scenario.get("expected_project")
        passed = route["project_id"] == expected
        detail = f"actual={route['project_id']} expected={expected}"
    elif s_type == "boundary_presence":
        results = retrieval.search_knowledge(scenario["input"], top_k=5)
        answer = answer_builder.build_grounded_answer(scenario["input"], results)
        passed = "safety boundary" in answer["answer"].lower()
        detail = f"boundary_present={passed}"
    else:
        detail = f"unknown scenario type: {s_type}"
    return {
        "scenario_id": scenario.get("scenario_id"),
        "type": s_type,
        "passed": passed,
        "detail": detail,
    }


def run_all_scenarios() -> list[dict[str, Any]]:
    scenarios = load_evaluation_scenarios().get("scenarios", [])
    return [run_single_scenario(s) for s in scenarios]


def summarize_evaluation(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    pass_rate = (passed / total) if total else 0.0
    return {"total": total, "passed": passed, "pass_rate": round(pass_rate, 4)}
