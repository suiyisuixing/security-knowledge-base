from agent_hub import agent_orchestrator


def test_classify_task_blocked():
    cls = agent_orchestrator.classify_task("Scan this public IP for vulnerabilities.")
    assert cls["allowed"] is False


def test_classify_task_allowed():
    cls = agent_orchestrator.classify_task("Explain BOLA")
    assert cls["allowed"] is True


def test_route_to_project_rag():
    r = agent_orchestrator.route_to_project_or_skill("Explain prompt injection in RAG.")
    assert r["project_id"] == "llm-security-lab"


def test_retrieve_supporting_knowledge_returns_list():
    docs = agent_orchestrator.retrieve_supporting_knowledge("Explain BOLA")
    assert isinstance(docs, list)


def test_choose_reasoning_mode_blocked():
    assert agent_orchestrator.choose_reasoning_mode("Scan this public IP for vulnerabilities.") == "safety_classification"


def test_choose_reasoning_mode_workflow():
    assert agent_orchestrator.choose_reasoning_mode("Plan a safe review in my local lab.") == "authorized_workflow"


def test_choose_reasoning_mode_grounded_answer():
    assert agent_orchestrator.choose_reasoning_mode("Explain what BOLA is.") == "rule_based_grounded_answer"


def test_choose_reasoning_mode_portfolio_gap():
    assert agent_orchestrator.choose_reasoning_mode("Show me the portfolio readiness gap.") == "portfolio_gap_analysis"


def test_produce_orchestration_result_for_allowed():
    r = agent_orchestrator.produce_orchestration_result("Explain BOLA")
    for k in ("mode", "classification", "route", "retrieved_docs", "primary_project_summary"):
        assert k in r


def test_produce_orchestration_result_for_blocked():
    r = agent_orchestrator.produce_orchestration_result("Scan this public IP for vulnerabilities.")
    assert r["mode"] == "safety_classification"
    assert r["classification"]["allowed"] is False
