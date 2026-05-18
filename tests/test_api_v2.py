def test_learning_path_ai(api_client):
    r = api_client.post("/learning-path/generate", json={"goal": "ai security"})
    assert r.status_code == 200
    assert r.json()["steps"]


def test_learning_path_detection(api_client):
    r = api_client.post("/learning-path/generate", json={"goal": "detection engineering"})
    assert r.status_code == 200
    ids = [s["skill_id"] for s in r.json()["steps"]]
    assert "log_analysis" in ids


def test_context_build_query(api_client):
    r = api_client.post("/context/build", json={"query": "bola authorization", "top_k": 3})
    assert r.status_code == 200
    assert r.json()["retrieved"]


def test_context_build_includes_safety(api_client):
    r = api_client.post("/context/build", json={"query": "Scan this public IP.", "top_k": 3})
    assert r.json()["safety_classification"].startswith("blocked_")


def test_quality_knowledge_list(api_client):
    r = api_client.get("/quality/knowledge")
    assert r.status_code == 200
    assert "summary" in r.json()


def test_quality_knowledge_doc_existing(api_client):
    r = api_client.get("/quality/knowledge/api-bola-001")
    assert r.status_code == 200
    assert "score" in r.json()


def test_quality_knowledge_doc_missing(api_client):
    r = api_client.get("/quality/knowledge/no-such-doc")
    assert r.status_code == 404


def test_quality_citations_evaluate(api_client):
    fake_answer = {
        "citations": [{"doc_id": "api-bola-001", "title": "BOLA", "domain": "api_security"}],
        "answer": "answer body",
        "safety_note": "boundary",
    }
    r = api_client.post("/quality/citations/evaluate", json=fake_answer)
    assert r.status_code == 200
    assert r.json()["cited_docs_exist"] is True


def test_reasoning_templates_list(api_client):
    r = api_client.get("/reasoning/templates")
    assert r.status_code == 200
    assert r.json()["templates"]


def test_reasoning_template_get(api_client):
    r = api_client.get("/reasoning/templates/api_authorization_review")
    assert r.status_code == 200


def test_reasoning_template_missing(api_client):
    r = api_client.get("/reasoning/templates/nope")
    assert r.status_code == 404


def test_workflow_authorized_plan_local(api_client):
    r = api_client.post("/workflow/authorized-plan", json={"request": "Plan a review in my local lab."})
    assert r.status_code == 200
    assert r.json()["allowed"] is True


def test_workflow_authorized_plan_blocked(api_client):
    r = api_client.post("/workflow/authorized-plan", json={"request": "Scan this public IP for vulnerabilities."})
    assert r.status_code == 200
    assert r.json()["allowed"] is False


def test_router_route_task_logs(api_client):
    r = api_client.post("/router/route-task", json={"query": "Help me triage these SOC alerts."})
    assert r.status_code == 200
    assert r.json()["project_id"] == "security-log-ai-assistant"


def test_router_route_task_rag(api_client):
    r = api_client.post("/router/route-task", json={"query": "How do I detect prompt injection in my RAG?"})
    assert r.status_code == 200
    assert r.json()["project_id"] == "llm-security-lab"


def test_benchmark_tasks_list(api_client):
    r = api_client.get("/benchmark/tasks")
    assert r.status_code == 200
    assert len(r.json()["tasks"]) >= 60


def test_benchmark_run(api_client):
    r = api_client.post("/benchmark/run")
    assert r.status_code == 200
    assert "summary" in r.json()


def test_benchmark_export_jsonl(api_client):
    r = api_client.get("/benchmark/export-jsonl")
    assert r.status_code == 200
    assert "\n" in r.json()["jsonl"]


def test_report_knowledge_coverage(api_client):
    r = api_client.post("/report/knowledge-coverage")
    assert r.status_code == 200
    assert "markdown" in r.json()


def test_report_safety_policy(api_client):
    r = api_client.post("/report/safety-policy")
    assert r.status_code == 200


def test_report_agent_readiness(api_client):
    r = api_client.post("/report/agent-readiness")
    assert r.status_code == 200


def test_evaluation_scenarios(api_client):
    r = api_client.get("/evaluation/scenarios")
    assert r.status_code == 200
    assert "scenarios" in r.json()


def test_evaluation_run(api_client):
    r = api_client.post("/evaluation/run")
    assert r.status_code == 200
    assert "summary" in r.json()


def test_api_surface_lists_endpoints(api_client):
    r = api_client.get("/api/surface")
    assert r.status_code == 200
    paths = {e["path"] for e in r.json()["endpoints"]}
    for path in ("/health", "/knowledge/search", "/safety/classify",
                 "/benchmark/run", "/report/agent-readiness",
                 "/workflow/authorized-plan", "/router/route-task"):
        assert path in paths


def test_memory_update_skill_roundtrip(api_client):
    r = api_client.post("/memory/update-skill", json={
        "skill_id": "log_analysis", "status": "in_progress", "notes": "test"
    })
    assert r.status_code == 200
