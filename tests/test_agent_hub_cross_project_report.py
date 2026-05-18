from agent_hub import cross_project_report


def test_cross_project_summary_has_four_projects():
    r = cross_project_report.build_cross_project_summary_report()
    assert len(r["projects"]) == 4


def test_project_relationship_report_has_edges():
    r = cross_project_report.build_project_relationship_report()
    assert r["edge_count"] >= 4


def test_skill_coverage_report_keys():
    r = cross_project_report.build_skill_coverage_report()
    assert "count" in r and "items" in r


def test_security_agent_capability_report_lists_caps():
    r = cross_project_report.build_security_agent_capability_report()
    assert len(r["capabilities"]) >= 5


def test_v5_agent_hub_report_keys():
    r = cross_project_report.build_v5_agent_hub_report()
    for k in ("summary", "relationships", "skills", "capabilities", "readiness", "maturity", "boundary_note"):
        assert k in r


def test_v5_agent_hub_report_boundary_mentions_no_llm():
    r = cross_project_report.build_v5_agent_hub_report()
    assert "LLM" in r["boundary_note"] or "model-free" in r["boundary_note"].lower()
