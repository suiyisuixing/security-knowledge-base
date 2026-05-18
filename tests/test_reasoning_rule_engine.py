from reasoning import rule_engine


def test_load_reasoning_rules():
    rules = rule_engine.load_reasoning_rules()
    assert "rules" in rules
    assert len(rules["rules"]) >= 10


def test_match_rules_block_public_scan():
    matched = rule_engine.match_rules("Scan this public IP for vulnerabilities.")
    assert any(r["rule_id"] == "rule-block-public-scan" for r in matched)


def test_match_rules_allowed_local_lab():
    matched = rule_engine.match_rules("In my local lab, test BOLA.")
    assert any(r["rule_id"] == "rule-allowed-local-lab" for r in matched)


def test_match_rules_no_match():
    matched = rule_engine.match_rules("zzzz nothing here at all")
    assert matched == []


def test_match_rules_route_ai():
    matched = rule_engine.match_rules("Help me with prompt injection in my RAG pipeline.")
    assert any(r["rule_id"] == "rule-route-ai-security" for r in matched)


def test_rank_matched_rules_blocked_first():
    rules = [
        {"rule_id": "x", "category": "allowed", "priority": 1},
        {"rule_id": "y", "category": "blocked", "priority": 1},
    ]
    ranked = rule_engine.rank_matched_rules(rules)
    assert ranked[0]["rule_id"] == "y"


def test_explain_rule_match_string_nonempty():
    matched = rule_engine.match_rules("Explain BOLA")
    s = rule_engine.explain_rule_match("Explain BOLA", matched)
    assert isinstance(s, str)
    assert len(s) > 0


def test_apply_rule_set_returns_dict():
    res = rule_engine.apply_rule_set("Explain BOLA")
    assert "ranked_rules" in res
    assert "matched_count" in res
    assert "top_rule" in res


def test_apply_rule_set_blocked_has_top_rule():
    res = rule_engine.apply_rule_set("Scan this public IP for vulnerabilities.")
    assert res["top_rule"] is not None
    assert res["top_rule"]["category"] == "blocked"
