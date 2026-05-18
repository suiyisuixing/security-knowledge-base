from app import reasoning_service


def test_run_rule_based_reasoning_returns_ranked():
    r = reasoning_service.run_rule_based_reasoning("Scan this public IP for vulnerabilities.")
    assert "ranked_rules" in r


def test_build_reasoned_answer_has_evidence_and_decision():
    r = reasoning_service.build_reasoned_answer("Explain BOLA")
    assert "evidence" in r
    assert "decision" in r
    assert "answer" in r


def test_build_policy_reasoning_returns_dict():
    r = reasoning_service.build_policy_reasoning("Explain BOLA")
    assert "safety" in r


def test_build_workflow_reasoning_includes_risk():
    r = reasoning_service.build_workflow_reasoning("In my local lab, plan a review.")
    assert "workflow" in r
    assert "risk" in r


def test_build_task_route_reasoning_includes_route():
    r = reasoning_service.build_task_route_reasoning("Help with RAG security.")
    assert "route" in r
    assert "rendered" in r


def test_build_evidence_based_report_includes_risk():
    r = reasoning_service.build_evidence_based_report("Explain BOLA")
    assert "evidence" in r
    assert "risk" in r


def test_build_decision_path_returns_structured():
    r = reasoning_service.build_decision_path("Explain BOLA")
    assert "decision" in r
    assert "safety_path" in r
