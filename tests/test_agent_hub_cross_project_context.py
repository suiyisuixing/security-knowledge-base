from agent_hub import cross_project_context


def test_build_context_for_projects():
    ctx = cross_project_context.build_context_for_projects(["security-knowledge-base"])
    assert len(ctx["projects"]) == 1


def test_build_cross_project_context_route_rag_to_A():
    ctx = cross_project_context.build_cross_project_context("Help me with prompt injection in my RAG pipeline.")
    assert ctx["primary_project"] == "llm-security-lab"


def test_build_cross_project_context_route_safety_to_D():
    ctx = cross_project_context.build_cross_project_context("How does the safety policy classify a public scan?")
    assert ctx["primary_project"] == "security-knowledge-base"


def test_attach_retrieval_citations_adds_field():
    ctx = cross_project_context.build_cross_project_context("Explain BOLA")
    cross_project_context.attach_retrieval_citations(ctx)
    assert "citations" in ctx


def test_attach_related_skills_field():
    ctx = cross_project_context.build_cross_project_context("Explain prompt injection")
    cross_project_context.attach_related_skills(ctx)
    assert "related_skills" in ctx


def test_attach_safety_classification_field():
    ctx = cross_project_context.build_cross_project_context("Explain BOLA")
    cross_project_context.attach_safety_classification(ctx)
    assert ctx["safety"]["allowed"] is True


def test_merge_knowledge_context_includes_route():
    ctx = cross_project_context.merge_knowledge_context_with_project_context("Explain BOLA")
    assert "recommended_route" in ctx
    assert "knowledge_summary" in ctx
