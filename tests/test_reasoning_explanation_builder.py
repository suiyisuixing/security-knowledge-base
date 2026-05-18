from reasoning import explanation_builder, evidence_builder


def test_build_short_explanation_string():
    s = explanation_builder.build_short_explanation("q", {"classification": "x", "allowed": True})
    assert "x" in s


def test_build_user_friendly_explanation_includes_query():
    chain = evidence_builder.build_evidence_chain("Explain BOLA")
    s = explanation_builder.build_user_friendly_explanation("Explain BOLA", chain)
    assert "Explain BOLA" in s


def test_build_reviewer_explanation_string():
    chain = evidence_builder.build_evidence_chain("Explain BOLA")
    s = explanation_builder.build_reviewer_explanation("Explain BOLA", chain)
    assert isinstance(s, str)


def test_build_explanation_returns_three_kinds():
    chain = evidence_builder.build_evidence_chain("Explain BOLA")
    decision = chain["safety_policy_decision"]
    exp = explanation_builder.build_explanation("Explain BOLA", chain, decision)
    assert set(exp.keys()) >= {"short", "user_friendly", "reviewer"}
