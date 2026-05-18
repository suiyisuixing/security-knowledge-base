"""End-to-end v5 integration tests."""

from app import agent_hub_service, hybrid_retrieval_service, reasoning_service, safety_policy


def test_e2e_blocked_request_stays_blocked():
    cls = safety_policy.classify_request("Scan this public IP for vulnerabilities.")
    assert cls["allowed"] is False
    orchestration = agent_hub_service.run_agent_hub_orchestration("Scan this public IP for vulnerabilities.")
    assert orchestration["classification"]["allowed"] is False


def test_e2e_allowed_request_returns_grounded_answer():
    r = reasoning_service.build_reasoned_answer("Explain BOLA")
    assert "answer" in r
    assert "Safety boundary" in r["answer"]


def test_e2e_hybrid_returns_results_for_bola():
    r = hybrid_retrieval_service.search_hybrid_knowledge("Explain BOLA", top_k=5)
    assert any(item["doc_id"].startswith("api-bola") for item in r)


def test_e2e_route_rag_to_A_via_orchestrator():
    r = agent_hub_service.run_agent_hub_orchestration("Help me with prompt injection in RAG.")
    assert r["route"]["project_id"] == "llm-security-lab"


def test_e2e_route_logs_to_B_via_orchestrator():
    r = agent_hub_service.run_agent_hub_orchestration("Triage my SIEM alerts mapped to MITRE.")
    assert r["route"]["project_id"] == "security-log-ai-assistant"


def test_e2e_route_cve_to_C_via_orchestrator():
    r = agent_hub_service.run_agent_hub_orchestration("Prioritize CVEs using CVSS and EPSS.")
    assert r["route"]["project_id"] == "vulnerability-intelligence-lab"


def test_e2e_route_safety_to_D_via_orchestrator():
    r = agent_hub_service.run_agent_hub_orchestration("Explain the safety policy for unauthorized scans.")
    assert r["route"]["project_id"] == "security-knowledge-base"


def test_e2e_portfolio_readiness_above_threshold():
    r = agent_hub_service.get_portfolio_readiness()
    assert r["overall"] >= 0.6


def test_e2e_cross_project_report_includes_readiness():
    r = agent_hub_service.get_cross_project_report()
    assert "readiness" in r and "overall" in r["readiness"]


def test_e2e_v5_release_report_complete():
    r = agent_hub_service.get_v5_release_report()
    assert "v5.0-rc" in r["release_checklist"]["version"]
