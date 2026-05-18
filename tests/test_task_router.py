from app import task_router


def test_route_rag_query():
    r = task_router.route_task("How do I detect prompt injection in my RAG pipeline?")
    assert r["project_id"] == "llm-security-lab"


def test_route_log_query():
    r = task_router.route_task("Help me triage these SOC alerts.")
    assert r["project_id"] == "security-log-ai-assistant"


def test_route_cve_query():
    r = task_router.route_task("Prioritize this CVE list.")
    assert r["project_id"] == "vulnerability-intelligence-lab"


def test_route_api_query():
    r = task_router.route_task("Review this OpenAPI spec for authorization issues.")
    assert r["project_id"] == "vulnerability-intelligence-lab"


def test_route_safety_query():
    r = task_router.route_task("Classify this safety-sensitive request.")
    assert r["project_id"] == "security-knowledge-base"


def test_route_default():
    r = task_router.route_task("totally random unrelated question")
    assert r["project_id"] == "security-knowledge-base"


def test_route_has_domain():
    r = task_router.route_task("Help me triage these SOC alerts.")
    assert r["knowledge_domain"] == "detection_engineering"


def test_route_has_skill():
    r = task_router.route_task("How do I prioritize CVE list?")
    assert r["skill_id"]


def test_route_explanation_string():
    r = task_router.route_task("Help me triage these SOC alerts.")
    assert "project" in r["explanation"].lower()


def test_route_to_project_returns_id():
    assert task_router.route_to_project("rag acl") == "llm-security-lab"


def test_route_to_knowledge_domain_logs():
    assert task_router.route_to_knowledge_domain("review my logs") == "detection_engineering"


def test_route_to_knowledge_domain_default():
    assert task_router.route_to_knowledge_domain("random") == "safe_boundaries"


def test_route_to_skill_returns_string():
    assert isinstance(task_router.route_to_skill("prompt injection"), str)


def test_route_router_for_sigma():
    r = task_router.route_task("Help me write a Sigma rule.")
    assert r["project_id"] == "security-log-ai-assistant"


def test_route_router_for_responsible_disclosure():
    r = task_router.route_task("Explain responsible disclosure.")
    assert r["project_id"] == "security-knowledge-base"
