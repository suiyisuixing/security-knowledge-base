from app import agent_report


def test_knowledge_coverage_report_shape():
    r = agent_report.build_knowledge_coverage_report()
    assert r["title"]
    assert r["sections"]


def test_safety_policy_report_shape():
    r = agent_report.build_safety_policy_report()
    assert r["title"] == "Safety Policy Report"


def test_skill_mapping_report_shape():
    r = agent_report.build_skill_mapping_report()
    assert r["title"] == "Skill Mapping Report"


def test_skill_mapping_report_mentions_projects():
    r = agent_report.build_skill_mapping_report()
    body_text = " ".join(s["body"] for s in r["sections"])
    assert "llm-security-lab" in body_text


def test_benchmark_report_shape():
    r = agent_report.build_benchmark_report()
    assert r["title"] == "Benchmark Report"


def test_agent_readiness_report_shape():
    r = agent_report.build_agent_readiness_report()
    assert r["title"] == "Agent Readiness Report"


def test_reports_contain_ai_disclosure_text():
    r = agent_report.build_skill_mapping_report()
    body_text = " ".join(s["body"] for s in r["sections"])
    assert "AI-assisted" in body_text


def test_reports_do_not_mention_claude():
    for r in (agent_report.build_knowledge_coverage_report(),
              agent_report.build_skill_mapping_report(),
              agent_report.build_benchmark_report(),
              agent_report.build_agent_readiness_report()):
        body_text = " ".join(s["body"] for s in r["sections"])
        assert "Claude" not in body_text


def test_reports_do_not_mention_anthropic():
    for r in (agent_report.build_knowledge_coverage_report(),
              agent_report.build_agent_readiness_report()):
        body_text = " ".join(s["body"] for s in r["sections"])
        assert "Anthropic" not in body_text


def test_skill_mapping_report_lists_skills():
    r = agent_report.build_skill_mapping_report()
    body_text = " ".join(s["body"] for s in r["sections"])
    assert "prompt_injection_reasoning" in body_text
