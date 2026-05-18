def test_rule_match_endpoint(api_client):
    r = api_client.post("/reasoning/rule-match", json={"query": "Scan this public IP for vulnerabilities."})
    assert r.status_code == 200
    assert r.json()["matched_count"] >= 1


def test_decision_path_endpoint(api_client):
    r = api_client.post("/reasoning/decision-path", json={"query": "Explain BOLA"})
    assert r.status_code == 200
    assert "decision" in r.json()


def test_risk_score_endpoint(api_client):
    r = api_client.post("/reasoning/risk-score", json={"query": "Scan this public IP for vulnerabilities."})
    assert r.status_code == 200
    assert r.json()["overall"]["level"] == "blocked"


def test_evidence_chain_endpoint(api_client):
    r = api_client.post("/reasoning/evidence-chain", json={"query": "Explain BOLA"})
    assert r.status_code == 200
    assert "evidence" in r.json()


def test_reasoned_answer_endpoint(api_client):
    r = api_client.post("/reasoning/reasoned-answer", json={"query": "Explain BOLA"})
    assert r.status_code == 200
    body = r.json()
    assert "answer" in body
    assert "Safety boundary" in body["answer"]


def test_policy_explanation_endpoint(api_client):
    r = api_client.post("/reasoning/policy-explanation", json={"query": "Explain BOLA"})
    assert r.status_code == 200
    body = r.json()
    assert "safety" in body
    assert "scope" in body
