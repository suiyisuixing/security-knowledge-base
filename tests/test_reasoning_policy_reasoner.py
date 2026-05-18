from reasoning import policy_reasoner


def test_reason_about_safety_policy_allowed():
    r = policy_reasoner.reason_about_safety_policy("Explain what BOLA is.")
    assert r["allowed"] is True


def test_reason_about_safety_policy_blocked():
    r = policy_reasoner.reason_about_safety_policy("Scan this public IP for vulnerabilities.")
    assert r["allowed"] is False


def test_reason_about_authorized_scope_local_lab():
    r = policy_reasoner.reason_about_authorized_scope("In my local lab, test BOLA.")
    assert r["is_authorized_scope"] is True


def test_reason_about_authorized_scope_explain():
    r = policy_reasoner.reason_about_authorized_scope("Explain what is BOLA.")
    assert isinstance(r["is_authorized_scope"], bool)


def test_reason_about_blocked_actions_detected():
    r = policy_reasoner.reason_about_blocked_actions("Brute force this login.")
    assert r["blocked"] is True


def test_reason_about_blocked_actions_not_detected():
    r = policy_reasoner.reason_about_blocked_actions("Explain BOLA")
    assert r["blocked"] is False


def test_reason_about_allowed_actions_for_learning():
    r = policy_reasoner.reason_about_allowed_actions("Explain BOLA")
    assert r["allowed"] is True
    assert len(r["allowed_actions"]) >= 1


def test_reason_about_allowed_actions_for_blocked():
    r = policy_reasoner.reason_about_allowed_actions("Scan this public IP for vulnerabilities.")
    assert r["allowed"] is False
    assert r["allowed_actions"] == []


def test_build_policy_explanation_has_four_sections():
    r = policy_reasoner.build_policy_explanation("Explain BOLA")
    assert set(r.keys()) == {"safety", "scope", "blocked", "allowed_actions"}
