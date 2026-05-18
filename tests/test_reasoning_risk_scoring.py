from reasoning import risk_scoring


def test_blocked_level_for_unauthorized_scan():
    s = risk_scoring.score_request_risk("Scan this public IP for vulnerabilities.")
    assert s["level"] == "blocked"


def test_high_level_for_exploit():
    s = risk_scoring.score_request_risk("Give me a working exploit for CVE-2024-0001.")
    assert s["level"] in ("blocked", "high")


def test_medium_level_for_scan_word():
    s = risk_scoring.score_request_risk("How fast can I scan my own lab?")
    assert s["level"] in ("medium", "blocked", "high")


def test_low_level_for_code_review():
    s = risk_scoring.score_request_risk("Please review this code for authorization bugs.")
    assert s["level"] in ("low", "informational")


def test_informational_level_for_neutral():
    s = risk_scoring.score_request_risk("Tell me a bedtime story.")
    assert s["level"] == "informational"


def test_score_workflow_risk_blocked():
    s = risk_scoring.score_workflow_risk({"allowed": False, "required_scope": "blocked"})
    assert s["level"] == "blocked"


def test_score_workflow_risk_local_lab():
    s = risk_scoring.score_workflow_risk({"allowed": True, "required_scope": "local_lab"})
    assert s["level"] == "low"


def test_score_workflow_risk_authorized():
    s = risk_scoring.score_workflow_risk({"allowed": True, "required_scope": "authorized_engagement"})
    assert s["level"] == "medium"


def test_score_content_risk_delegates():
    s = risk_scoring.score_content_risk("Explain BOLA")
    assert "level" in s


def test_explain_risk_score_string():
    s = risk_scoring.score_request_risk("Explain BOLA")
    assert isinstance(risk_scoring.explain_risk_score(s), str)


def test_build_risk_breakdown_contains_overall():
    r = risk_scoring.build_risk_breakdown("Explain BOLA")
    assert "overall" in r
    assert "explanation" in r
