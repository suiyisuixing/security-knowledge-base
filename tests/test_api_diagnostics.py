def test_health_endpoint(api_client):
    r = api_client.get("/diagnostics/health")
    assert r.status_code == 200
    assert r.json()["backend"]["model_free"] is True


def test_integrity_endpoint(api_client):
    r = api_client.get("/diagnostics/integrity")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_schema_validation_endpoint(api_client):
    r = api_client.get("/diagnostics/schema-validation")
    assert r.status_code == 200
    assert r.json()["all_valid"] is True


def test_project_status_endpoint(api_client):
    r = api_client.get("/diagnostics/project-status")
    assert r.status_code == 200
    body = r.json()
    assert "integrity" in body
    assert "schema_validation" in body
    assert "health" in body
