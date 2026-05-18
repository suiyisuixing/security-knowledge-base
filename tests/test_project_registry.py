from app import project_registry


def test_registry_loads():
    data = project_registry.load_project_registry()
    assert "projects" in data


def test_registry_contains_all_four():
    ids = {p["project_id"] for p in project_registry.list_projects()}
    assert ids >= {
        "llm-security-lab",
        "security-log-ai-assistant",
        "vulnerability-intelligence-lab",
        "security-knowledge-base",
    }


def test_each_project_has_repo_url():
    for p in project_registry.list_projects():
        assert p["repo"].startswith("https://github.com/suiyisuixing/")


def test_each_project_has_skills_list():
    for p in project_registry.list_projects():
        assert isinstance(p.get("skills"), list)


def test_get_project_existing():
    p = project_registry.get_project("llm-security-lab")
    assert p["focus"]


def test_get_project_missing():
    assert project_registry.get_project("no-such") is None


def test_map_skill_to_projects():
    projects = project_registry.map_skill_to_projects("prompt_injection_reasoning")
    assert "llm-security-lab" in projects


def test_map_skill_to_projects_empty():
    assert project_registry.map_skill_to_projects("does-not-exist-skill") == []


def test_recommend_project_for_rag_query():
    assert project_registry.recommend_project_for_query("how do I secure my rag") == "llm-security-lab"


def test_recommend_project_for_log_query():
    assert project_registry.recommend_project_for_query("help with sigma logs") == "security-log-ai-assistant"


def test_recommend_project_for_cve_query():
    assert project_registry.recommend_project_for_query("prioritize this cve") == "vulnerability-intelligence-lab"


def test_recommend_project_default():
    assert project_registry.recommend_project_for_query("classify this safety request") == "security-knowledge-base"
