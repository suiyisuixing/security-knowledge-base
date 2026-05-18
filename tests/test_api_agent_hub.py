def test_agent_hub_status_endpoint(api_client):
    r = api_client.get("/agent-hub/status")
    assert r.status_code == 200
    assert r.json()["model_free"] is True


def test_agent_hub_context_endpoint(api_client):
    r = api_client.post("/agent-hub/context", json={"query": "Explain BOLA"})
    assert r.status_code == 200
    assert "primary_project" in r.json()


def test_agent_hub_orchestrate_endpoint(api_client):
    r = api_client.post("/agent-hub/orchestrate", json={"query": "Explain BOLA"})
    assert r.status_code == 200
    body = r.json()
    assert "mode" in body and "classification" in body


def test_agent_hub_skill_evidence_endpoint(api_client):
    r = api_client.get("/agent-hub/skill-evidence")
    assert r.status_code == 200
    assert r.json()["count"] >= 5


def test_agent_hub_missing_evidence_endpoint(api_client):
    r = api_client.get("/agent-hub/missing-evidence")
    assert r.status_code == 200


def test_agent_hub_portfolio_readiness_endpoint(api_client):
    r = api_client.get("/agent-hub/portfolio-readiness")
    assert r.status_code == 200
    assert "overall" in r.json()


def test_agent_hub_cross_project_report_endpoint(api_client):
    r = api_client.get("/agent-hub/cross-project-report")
    assert r.status_code == 200


def test_agent_hub_maturity_endpoint(api_client):
    r = api_client.get("/agent-hub/maturity")
    assert r.status_code == 200
    assert r.json()["summary"]["total"] == 4


def test_agent_hub_next_actions_endpoint(api_client):
    r = api_client.get("/agent-hub/next-actions")
    assert r.status_code == 200


def test_agent_hub_v5_release_report_endpoint(api_client):
    r = api_client.get("/agent-hub/v5-release-report")
    assert r.status_code == 200
