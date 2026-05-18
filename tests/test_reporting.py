from app import reporting


def test_build_knowledge_report_shape():
    r = reporting.build_knowledge_report()
    assert r["title"] == "Knowledge Coverage Report"
    assert r["sections"]


def test_build_safety_policy_report_shape():
    r = reporting.build_safety_policy_report()
    assert r["title"] == "Safety Policy Report"
    assert r["sections"]


def test_build_agent_readiness_report_shape():
    r = reporting.build_agent_readiness_report()
    assert r["title"] == "Agent Readiness Report"
    assert r["sections"]


def test_markdown_report_contains_title():
    r = reporting.build_knowledge_report()
    md = reporting.build_markdown_report(r)
    assert md.startswith("# Knowledge Coverage Report")


def test_markdown_report_includes_headings():
    r = reporting.build_safety_policy_report()
    md = reporting.build_markdown_report(r)
    assert "## " in md


def test_json_report_is_valid_json_string():
    import json as _json
    r = reporting.build_knowledge_report()
    j = reporting.build_json_report(r)
    parsed = _json.loads(j)
    assert parsed["title"] == r["title"]


def test_reports_contain_ai_disclosure_text():
    md = reporting.build_markdown_report(reporting.build_knowledge_report())
    assert "AI-assisted" in md


def test_reports_do_not_mention_claude():
    md = reporting.build_markdown_report(reporting.build_safety_policy_report())
    assert "Claude" not in md
    assert "Anthropic" not in md


def test_reports_do_not_contain_api_keys():
    md = reporting.build_markdown_report(reporting.build_agent_readiness_report())
    import re
    assert not re.search(r"sk-[A-Za-z0-9]{8,}", md)


def test_agent_readiness_report_mentions_projects():
    md = reporting.build_markdown_report(reporting.build_agent_readiness_report())
    assert "security-knowledge-base" in md
