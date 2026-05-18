from app import demo_assets


def test_list_demo_samples_nonempty():
    items = demo_assets.list_demo_samples()
    assert len(items) >= 15


def test_list_demo_samples_have_sample_id():
    for item in demo_assets.list_demo_samples():
        assert item["sample_id"]
        assert item["group"]


def test_get_demo_sample_existing():
    samples = demo_assets.list_demo_samples()
    sid = samples[0]["sample_id"]
    assert demo_assets.get_demo_sample(sid) is not None


def test_get_demo_sample_missing():
    assert demo_assets.get_demo_sample("nope-missing-xyz") is None


def test_reviewer_path_has_12_steps():
    path = demo_assets.build_reviewer_path()
    assert len(path["steps"]) == 12


def test_reviewer_path_steps_have_endpoint():
    path = demo_assets.build_reviewer_path()
    for step in path["steps"]:
        assert "endpoint" in step


def test_reviewer_path_boundary_present():
    path = demo_assets.build_reviewer_path()
    assert "Local-only" in path["safety_boundary"] or "local-only" in path["safety_boundary"]


def test_portfolio_summary_has_value_list():
    s = demo_assets.build_portfolio_demo_summary()
    assert len(s["value"]) >= 5


def test_portfolio_summary_links_all_four():
    s = demo_assets.build_portfolio_demo_summary()
    ids = {item["project_id"] for item in s["portfolio_links"]}
    assert ids == {
        "llm-security-lab",
        "security-log-ai-assistant",
        "vulnerability-intelligence-lab",
        "security-knowledge-base",
    }


def test_validate_sample_outputs_ok():
    result = demo_assets.validate_sample_outputs()
    assert result["ok"], result["issues"]


def test_sample_groups_present():
    result = demo_assets.validate_sample_outputs()
    expected = {"api_responses", "reports", "benchmark", "agent_readiness",
                "router_examples", "authorized_workflows"}
    assert expected.issubset(set(result["groups"]))


def test_sample_outputs_have_endpoint_field():
    for sid, _ in demo_assets._scan_samples().items():  # noqa: SLF001
        sample = demo_assets.get_demo_sample(sid)
        assert sample is not None
        assert sample.get("endpoint") or sample.get("response") or sample.get("report_excerpt")
