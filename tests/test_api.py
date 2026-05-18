def test_root_endpoint(api_client):
    r = api_client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_health_endpoint(api_client):
    r = api_client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_health_version_field(api_client):
    r = api_client.get("/health")
    assert "version" in r.json()


def test_knowledge_domains(api_client):
    r = api_client.get("/knowledge/domains")
    assert r.status_code == 200
    assert "ai_security" in r.json()["domains"]


def test_knowledge_docs(api_client):
    r = api_client.get("/knowledge/docs")
    assert r.status_code == 200
    assert r.json()["count"] >= 32


def test_knowledge_docs_domain_filter(api_client):
    r = api_client.get("/knowledge/docs?domain=api_security")
    assert r.status_code == 200
    for d in r.json()["documents"]:
        assert d["domain"] == "api_security"


def test_knowledge_doc_existing(api_client):
    r = api_client.get("/knowledge/docs/api-bola-001")
    assert r.status_code == 200
    assert r.json()["metadata"]["id"] == "api-bola-001"


def test_knowledge_doc_missing(api_client):
    r = api_client.get("/knowledge/docs/no-such-doc")
    assert r.status_code == 404


def test_knowledge_search(api_client):
    r = api_client.post("/knowledge/search", json={"query": "prompt injection", "top_k": 5})
    assert r.status_code == 200
    assert r.json()["results"]


def test_knowledge_ask(api_client):
    r = api_client.post("/knowledge/ask", json={"query": "Explain BOLA.", "top_k": 5})
    assert r.status_code == 200
    body = r.json()
    assert body["citations"]
    assert body["safety_note"]


def test_safety_classify_blocked(api_client):
    r = api_client.post("/safety/classify", json={"text": "Scan this public IP for vulnerabilities."})
    assert r.status_code == 200
    assert r.json()["allowed"] is False


def test_safety_classify_allowed(api_client):
    r = api_client.post("/safety/classify", json={"text": "Explain what BOLA is."})
    assert r.status_code == 200
    assert r.json()["allowed"] is True


def test_safety_policy(api_client):
    r = api_client.get("/safety/policy")
    assert r.status_code == 200
    assert "classes" in r.json()


def test_safety_evaluation_get(api_client):
    r = api_client.get("/safety/evaluation")
    assert r.status_code == 200
    assert "results" in r.json()


def test_safety_evaluate_post(api_client):
    r = api_client.post("/safety/evaluate")
    assert r.status_code == 200
    assert "summary" in r.json()


def test_memory_profile(api_client):
    r = api_client.get("/memory/profile")
    assert r.status_code == 200
    assert "skill_progress" in r.json()


def test_memory_skill_progress(api_client):
    r = api_client.get("/memory/skill-progress")
    assert r.status_code == 200


def test_memory_audit(api_client):
    r = api_client.get("/memory/audit")
    assert r.status_code == 200


def test_projects_list(api_client):
    r = api_client.get("/projects")
    assert r.status_code == 200
    ids = [p["project_id"] for p in r.json()["projects"]]
    assert "llm-security-lab" in ids


def test_projects_get(api_client):
    r = api_client.get("/projects/llm-security-lab")
    assert r.status_code == 200


def test_projects_get_missing(api_client):
    r = api_client.get("/projects/no-such-project")
    assert r.status_code == 404


def test_skills_list(api_client):
    r = api_client.get("/skills")
    assert r.status_code == 200
    assert len(r.json()["skills"]) >= 16


def test_skills_get(api_client):
    r = api_client.get("/skills/prompt_injection_reasoning")
    assert r.status_code == 200


def test_skills_get_missing(api_client):
    r = api_client.get("/skills/no-such-skill")
    assert r.status_code == 404


def test_skills_recommend(api_client):
    r = api_client.post("/skills/recommend", json={"goal": "ai security"})
    assert r.status_code == 200
    assert r.json()["recommended_skills"]
