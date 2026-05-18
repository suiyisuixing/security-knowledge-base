from app import evaluation


def test_load_scenarios_returns_list():
    data = evaluation.load_evaluation_scenarios()
    assert isinstance(data.get("scenarios"), list)
    assert len(data["scenarios"]) >= 10


def test_run_all_scenarios_returns_results():
    results = evaluation.run_all_scenarios()
    assert isinstance(results, list)
    assert all("scenario_id" in r for r in results)
    assert all("passed" in r for r in results)


def test_summarize_evaluation_shape():
    results = evaluation.run_all_scenarios()
    summary = evaluation.summarize_evaluation(results)
    assert "total" in summary
    assert "passed" in summary
    assert "pass_rate" in summary


def test_summarize_evaluation_pass_rate_range():
    results = evaluation.run_all_scenarios()
    summary = evaluation.summarize_evaluation(results)
    assert 0.0 <= summary["pass_rate"] <= 1.0


def test_run_single_scenario_knowledge_search():
    scenario = {
        "scenario_id": "test-knowledge",
        "type": "knowledge_search",
        "input": "prompt injection",
        "expected_doc_id_prefix": "ai-prompt-injection",
    }
    result = evaluation.run_single_scenario(scenario)
    assert result["passed"] is True


def test_run_single_scenario_safety_classification():
    scenario = {
        "scenario_id": "test-safety",
        "type": "safety_classification",
        "input": "Scan this public IP for vulnerabilities.",
        "expected_classification": "blocked_unauthorized_public_scan",
    }
    result = evaluation.run_single_scenario(scenario)
    assert result["passed"] is True


def test_run_single_scenario_task_routing():
    scenario = {
        "scenario_id": "test-route",
        "type": "task_routing",
        "input": "Help me triage these SOC alerts.",
        "expected_project": "security-log-ai-assistant",
    }
    result = evaluation.run_single_scenario(scenario)
    assert result["passed"] is True


def test_run_single_scenario_unknown_type():
    scenario = {"scenario_id": "x", "type": "nope", "input": "x"}
    result = evaluation.run_single_scenario(scenario)
    assert result["passed"] is False


def test_summary_empty_results():
    summary = evaluation.summarize_evaluation([])
    assert summary["total"] == 0
    assert summary["pass_rate"] == 0.0


def test_evaluation_includes_boundary_scenario():
    data = evaluation.load_evaluation_scenarios()
    types = {s["type"] for s in data["scenarios"]}
    assert "boundary_presence" in types
