from reasoning import workflow_reasoner


def test_reason_about_authorized_workflow_local_lab():
    wf = workflow_reasoner.reason_about_authorized_workflow("Plan a review in my local lab.")
    assert wf["allowed"] is True


def test_reason_about_authorized_workflow_blocked():
    wf = workflow_reasoner.reason_about_authorized_workflow("Scan this public IP for vulnerabilities.")
    assert wf["allowed"] is False


def test_build_safe_verification_plan_allowed():
    plan = workflow_reasoner.build_safe_verification_plan("In my local lab, observe SSRF.")
    assert plan["allowed"] is True
    assert len(plan["steps"]) >= 4


def test_build_safe_verification_plan_blocked():
    plan = workflow_reasoner.build_safe_verification_plan("Scan this public IP for vulnerabilities.")
    assert plan["allowed"] is False
    assert plan["steps"] == []


def test_build_low_risk_check_plan_allowed():
    plan = workflow_reasoner.build_low_risk_check_plan("Plan a low-risk check for my own staging server.")
    assert plan["allowed"] is True


def test_build_local_lab_plan_always_allowed():
    plan = workflow_reasoner.build_local_lab_plan("In my local lab.")
    assert plan["allowed"] is True
    assert plan["required_scope"] == "local_lab"


def test_build_blocked_workflow_explanation_blocked():
    exp = workflow_reasoner.build_blocked_workflow_explanation("Scan this public IP for vulnerabilities.")
    assert exp["blocked"] is True


def test_build_blocked_workflow_explanation_includes_actions():
    exp = workflow_reasoner.build_blocked_workflow_explanation("Scan this public IP for vulnerabilities.")
    assert len(exp["blocked_actions"]) >= 1
