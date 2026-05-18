from app import error_model


def test_make_error_basic_shape():
    e = error_model.make_error("not_found", "doc missing", "list docs")
    assert e["error"] is True
    assert e["code"] == "not_found"
    assert e["message"] == "doc missing"
    assert e["safe_redirect"] == "list docs"
    assert e["details"] == {}


def test_make_error_with_details():
    e = error_model.make_error("validation_error", "bad input", "fix it", {"field": "x"})
    assert e["details"]["field"] == "x"


def test_make_error_unknown_code_defaults():
    e = error_model.make_error("totally-unknown", "msg")
    assert e["code"] == "internal_error"


def test_not_found_helper():
    e = error_model.not_found("document")
    assert e["code"] == "not_found"
    assert "document" in e["message"]


def test_validation_error_helper():
    e = error_model.validation_error("query", "too short")
    assert e["code"] == "validation_error"
    assert e["details"]["field"] == "query"


def test_blocked_by_policy_helper():
    e = error_model.blocked_by_policy("blocked_unauthorized_public_scan", "use local lab")
    assert e["code"] == "blocked_by_policy"
    assert e["safe_redirect"] == "use local lab"
    assert e["details"]["classification"] == "blocked_unauthorized_public_scan"


def test_valid_codes_set_complete():
    expected = {"not_found", "validation_error", "blocked_by_policy",
                "needs_confirmation", "schema_invalid", "integrity_failure",
                "internal_error"}
    assert expected.issubset(error_model.VALID_CODES)
