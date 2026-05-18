from app import vuln_reasoning_templates as vrt


def test_load_templates_returns_list():
    templates = vrt.load_reasoning_templates()
    assert isinstance(templates, list)
    assert len(templates) >= 8


def test_list_templates_alias():
    assert vrt.list_templates() == vrt.load_reasoning_templates()


def test_get_template_existing():
    t = vrt.get_template("api_authorization_review")
    assert t is not None
    assert t["name"]


def test_get_template_missing():
    assert vrt.get_template("nope") is None


def test_each_template_has_steps():
    for t in vrt.list_templates():
        assert t["steps"]


def test_each_template_has_forbidden_steps():
    for t in vrt.list_templates():
        assert t["forbidden_steps"]


def test_recommend_for_bola_query():
    assert vrt.recommend_template_for_query("bola in api") == "api_authorization_review"


def test_recommend_for_dependency_query():
    assert vrt.recommend_template_for_query("dependency cve in sbom") == "dependency_risk_review"


def test_recommend_for_rag_query():
    assert vrt.recommend_template_for_query("rag retrieval") == "rag_security_review"


def test_recommend_for_log_query():
    assert vrt.recommend_template_for_query("sigma log detection") == "log_detection_review"


def test_recommend_for_recon_query():
    assert vrt.recommend_template_for_query("plan reconnaissance for my lab") == "authorized_recon_planning"


def test_recommend_for_verify_query():
    assert vrt.recommend_template_for_query("verify this finding") == "safe_verification_plan"


def test_recommend_for_remediation_query():
    assert vrt.recommend_template_for_query("plan remediation") == "remediation_plan"


def test_recommend_for_unknown_query():
    assert vrt.recommend_template_for_query("totally unrelated") is None


def test_render_template_steps_existing():
    steps = vrt.render_template_steps("safe_verification_plan")
    assert steps


def test_render_template_steps_missing():
    assert vrt.render_template_steps("nope") == []
