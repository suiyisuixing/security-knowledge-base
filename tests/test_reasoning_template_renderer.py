from reasoning import template_renderer, evidence_builder


def test_grounded_answer_template_includes_safety_footer():
    chain = evidence_builder.build_evidence_chain("Explain BOLA")
    text = template_renderer.render_grounded_answer_template("Explain BOLA", chain)
    assert "Safety boundary" in text


def test_grounded_answer_no_real_scan_command():
    chain = evidence_builder.build_evidence_chain("Explain BOLA")
    text = template_renderer.render_grounded_answer_template("Explain BOLA", chain).lower()
    for forbidden in ("nmap ", "masscan ", "sqlmap ", "ffuf ", "gobuster ", "nikto "):
        assert forbidden not in text


def test_safety_explanation_template_contains_fields():
    decision = {"classification": "allowed_learning", "allowed": True, "reason": "edu",
                "safe_redirect": "explain"}
    text = template_renderer.render_safety_explanation_template("Explain", decision)
    for f in ("Classification", "Allowed", "Reason", "Safe redirect"):
        assert f in text


def test_authorized_workflow_template_includes_blocked_actions():
    wf = {"workflow_id": "x", "allowed": True, "required_scope": "local_lab",
          "steps": ["a"], "blocked_actions": ["no scanning"]}
    text = template_renderer.render_authorized_workflow_template(wf)
    assert "Blocked actions" in text
    assert "no scanning" in text


def test_task_route_template_string():
    route = {"project_id": "x", "knowledge_domain": "y", "skill_id": "z", "explanation": "e"}
    text = template_renderer.render_task_route_template(route)
    assert "x" in text and "y" in text


def test_portfolio_readiness_template():
    rep = {"categories": {"docs": 1.0, "tests": 0.5}, "overall": 0.7}
    text = template_renderer.render_portfolio_readiness_template(rep)
    assert "Overall" in text


def test_skill_gap_template_empty_list():
    text = template_renderer.render_skill_gap_template([])
    assert "No major gaps" in text


def test_skill_gap_template_with_gaps():
    text = template_renderer.render_skill_gap_template([{"skill_id": "x", "reason": "missing"}])
    assert "x" in text
