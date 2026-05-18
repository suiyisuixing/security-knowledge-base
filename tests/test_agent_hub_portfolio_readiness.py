from agent_hub import portfolio_readiness


def test_calculate_project_maturity_security_kb():
    m = portfolio_readiness.calculate_project_maturity("security-knowledge-base")
    assert m["level"] >= 1


def test_calculate_skill_coverage_in_range():
    s = portfolio_readiness.calculate_skill_coverage()
    assert 0.0 <= s <= 1.0


def test_calculate_documentation_score_in_range():
    s = portfolio_readiness.calculate_documentation_score()
    assert 0.0 <= s <= 1.0


def test_calculate_testing_score_in_range():
    s = portfolio_readiness.calculate_testing_score()
    assert 0.0 <= s <= 1.0


def test_calculate_safety_score_positive():
    s = portfolio_readiness.calculate_safety_score()
    assert s > 0


def test_calculate_demo_score_in_range():
    s = portfolio_readiness.calculate_demo_score()
    assert 0.0 <= s <= 1.0


def test_calculate_overall_portfolio_readiness_keys():
    o = portfolio_readiness.calculate_overall_portfolio_readiness()
    assert "categories" in o
    assert "overall" in o
    assert 0.0 <= o["overall"] <= 1.0


def test_portfolio_readiness_overall_above_threshold():
    o = portfolio_readiness.calculate_overall_portfolio_readiness()
    assert o["overall"] >= 0.6


def test_build_portfolio_readiness_report_includes_per_project():
    r = portfolio_readiness.build_portfolio_readiness_report()
    assert "per_project" in r
    assert len(r["per_project"]) == 4
