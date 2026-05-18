from app import context_builder, knowledge_loader


def setup_module(module):
    knowledge_loader.build_knowledge_index()


def test_context_for_query_shape():
    ctx = context_builder.build_context_for_query("prompt injection")
    for key in ("query", "retrieved", "related_skills", "related_projects",
                "safety_classification", "safety_allowed",
                "safe_boundary", "recommended_next_step"):
        assert key in ctx


def test_context_retrieved_nonempty():
    ctx = context_builder.build_context_for_query("bola authorization")
    assert ctx["retrieved"]


def test_context_includes_related_skills():
    ctx = context_builder.build_context_for_query("bola authorization")
    assert "api_authorization_reasoning" in ctx["related_skills"]


def test_context_includes_related_projects():
    ctx = context_builder.build_context_for_query("bola authorization")
    assert "vulnerability-intelligence-lab" in ctx["related_projects"]


def test_context_safety_blocked_for_scan():
    ctx = context_builder.build_context_for_query("Scan this public IP for vulnerabilities.")
    assert ctx["safety_classification"].startswith("blocked_")
    assert ctx["safety_allowed"] is False


def test_context_safety_allowed_for_learning():
    ctx = context_builder.build_context_for_query("Explain prompt injection.")
    assert ctx["safety_allowed"] is True


def test_context_for_project_found():
    out = context_builder.build_context_for_project("llm-security-lab")
    assert out["found"] is True
    assert out["focus"]


def test_context_for_project_missing():
    out = context_builder.build_context_for_project("nope")
    assert out["found"] is False


def test_context_for_skill_found():
    out = context_builder.build_context_for_skill("prompt_injection_reasoning")
    assert out["found"] is True


def test_context_for_skill_missing():
    out = context_builder.build_context_for_skill("nope")
    assert out["found"] is False


def test_build_agent_context_alias():
    ctx = context_builder.build_agent_context("prompt injection")
    assert "retrieved" in ctx
