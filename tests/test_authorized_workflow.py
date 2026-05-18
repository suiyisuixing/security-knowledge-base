from app import authorized_workflow as aw


def _build(text):
    return aw.build_authorized_workflow({"request": text})


def test_local_lab_allowed():
    wf = _build("Plan a safe review in my local lab.")
    assert wf["allowed"] is True
    assert wf["required_scope"] == "local_lab"


def test_self_owned_asset_allowed():
    wf = _build("Plan a low-risk security check for my own staging server.")
    assert wf["allowed"] is True
    assert wf["required_scope"] == "self_owned_asset"


def test_authorized_engagement_allowed():
    wf = _build("Plan limited recon inside my bug bounty scope.")
    assert wf["allowed"] is True
    assert wf["required_scope"] == "authorized_engagement"


def test_public_scan_blocked():
    wf = _build("Scan this public IP for vulnerabilities.")
    assert wf["allowed"] is False
    assert wf["required_scope"] == "blocked"


def test_unconfirmed_scope_blocked():
    wf = _build("Just take a look at this site.")
    assert wf["allowed"] is False


def test_steps_present_when_allowed():
    wf = _build("In my local lab, review this configuration.")
    assert wf["steps"]


def test_steps_empty_when_blocked():
    wf = _build("Scan this public IP for vulnerabilities.")
    assert wf["steps"] == []


def test_blocked_actions_always_present():
    wf = _build("Plan a review in my local lab.")
    assert wf["blocked_actions"]


def test_validate_scope_local_lab():
    scope = aw.validate_scope("In my local lab, check authentication.")
    assert scope["in_scope"] is True


def test_validate_authorization_claim_invalid():
    auth = aw.validate_authorization_claim("Check this random site.")
    assert auth["valid"] is False


def test_summarize_workflow_string():
    wf = _build("In my local lab, review this configuration.")
    assert "allowed=True" in aw.summarize_workflow(wf)


def test_build_workflow_accepts_plain_string_dict_only():
    wf = aw.build_authorized_workflow({"request": "Plan a review in my local lab."})
    assert isinstance(wf, dict)
