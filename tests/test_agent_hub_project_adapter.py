from agent_hub import project_adapter


def test_load_project_status_samples_has_four():
    data = project_adapter.load_project_status_samples()
    ids = {s["project_id"] for s in data["samples"]}
    assert ids == {
        "llm-security-lab",
        "security-log-ai-assistant",
        "vulnerability-intelligence-lab",
        "security-knowledge-base",
    }


def test_get_capabilities_for_each_project():
    for pid in ("llm-security-lab", "security-log-ai-assistant",
                "vulnerability-intelligence-lab", "security-knowledge-base"):
        assert len(project_adapter.get_project_capabilities(pid)) >= 1


def test_get_known_artifacts_for_each_project():
    for pid in ("llm-security-lab", "security-log-ai-assistant",
                "vulnerability-intelligence-lab", "security-knowledge-base"):
        assert len(project_adapter.get_project_known_artifacts(pid)) >= 1


def test_get_skill_coverage_for_each_project():
    for pid in ("llm-security-lab", "security-log-ai-assistant",
                "vulnerability-intelligence-lab", "security-knowledge-base"):
        assert len(project_adapter.get_project_skill_coverage(pid)) >= 1


def test_build_project_adapter_summary_includes_repo():
    s = project_adapter.build_project_adapter_summary("security-knowledge-base")
    assert s["project_id"] == "security-knowledge-base"
    assert "repo" in s


def test_unknown_project_returns_empty_lists():
    assert project_adapter.get_project_capabilities("nope") == []
    assert project_adapter.get_project_known_artifacts("nope") == []
    assert project_adapter.get_project_skill_coverage("nope") == []
