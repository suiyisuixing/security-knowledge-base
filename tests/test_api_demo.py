def test_demo_reviewer_path_200(api_client):
    r = api_client.get("/demo/reviewer-path")
    assert r.status_code == 200
    body = r.json()
    assert body["title"] == "Reviewer Quick Path"
    assert len(body["steps"]) == 12


def test_demo_sample_outputs_200(api_client):
    r = api_client.get("/demo/sample-outputs")
    assert r.status_code == 200
    assert len(r.json()["samples"]) >= 15


def test_demo_sample_output_known_200(api_client):
    r = api_client.get("/demo/sample-output/knowledge_search_bola")
    assert r.status_code == 200
    body = r.json()
    assert body["sample_id"] == "knowledge_search_bola"


def test_demo_sample_output_missing_404(api_client):
    r = api_client.get("/demo/sample-output/does-not-exist")
    assert r.status_code == 404


def test_demo_portfolio_summary_200(api_client):
    r = api_client.get("/demo/portfolio-summary")
    assert r.status_code == 200
    body = r.json()
    assert len(body["portfolio_links"]) == 4
    assert body["version"]
