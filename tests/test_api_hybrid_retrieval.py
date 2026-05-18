def test_hybrid_search_endpoint(api_client):
    r = api_client.post("/retrieval/hybrid-search", json={"query": "Explain BOLA", "top_k": 5})
    assert r.status_code == 200
    assert isinstance(r.json()["results"], list)


def test_compare_endpoint(api_client):
    r = api_client.post("/retrieval/compare", json={"query": "Explain BOLA"})
    assert r.status_code == 200
    body = r.json()
    assert "legacy" in body and "hybrid" in body


def test_grounding_report_endpoint(api_client):
    r = api_client.post("/retrieval/grounding-report",
                        json={"answer": "BOLA is an API flaw.", "query": "Explain BOLA"})
    assert r.status_code == 200
    assert "grounding" in r.json()


def test_retrieval_evaluation_endpoint(api_client):
    r = api_client.get("/retrieval/evaluation")
    assert r.status_code == 200
    assert "summary" in r.json()


def test_retrieval_conflicts_endpoint(api_client):
    r = api_client.get("/retrieval/conflicts")
    assert r.status_code == 200


def test_retrieval_source_trust_endpoint(api_client):
    r = api_client.get("/retrieval/source-trust")
    assert r.status_code == 200
    assert r.json()["count"] >= 32
