from app import agent_hub_service


def test_get_agent_hub_status():
    s = agent_hub_service.get_agent_hub_status()
    assert s["model_free"] is True
    assert s["projects_tracked"] == 4


def test_build_agent_hub_context_returns_context():
    c = agent_hub_service.build_agent_hub_context("Explain BOLA")
    assert "primary_project" in c
    assert "recommended_route" in c


def test_run_agent_hub_orchestration():
    r = agent_hub_service.run_agent_hub_orchestration("Explain BOLA")
    assert "mode" in r and "classification" in r


def test_skill_evidence_report_nonempty():
    r = agent_hub_service.get_skill_evidence_report()
    assert r["count"] >= 5


def test_missing_evidence_report_returns_list():
    r = agent_hub_service.get_missing_evidence_report()
    assert "missing_skills" in r


def test_portfolio_readiness_report_has_overall():
    r = agent_hub_service.get_portfolio_readiness()
    assert 0.0 <= r["overall"] <= 1.0


def test_cross_project_report_keys():
    r = agent_hub_service.get_cross_project_report()
    for k in ("summary", "relationships", "skills", "capabilities", "readiness", "maturity"):
        assert k in r


def test_next_action_plan_keys():
    r = agent_hub_service.get_next_action_plan()
    assert "items" in r and "safety_boundary" in r


def test_maturity_report_keys():
    r = agent_hub_service.get_maturity_report()
    assert set(r.keys()) >= {"summary", "per_project", "improvements"}


def test_v5_release_report_keys():
    r = agent_hub_service.get_v5_release_report()
    assert set(r.keys()) >= {"roadmap", "release_checklist", "v5_to_v6", "notes"}
