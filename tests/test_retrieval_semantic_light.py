from retrieval import semantic_light


def test_normalize_security_terms_authz():
    assert "authorization" in semantic_light.normalize_security_terms("Explain authz flaws")


def test_normalize_security_terms_authn():
    assert "authentication" in semantic_light.normalize_security_terms("Explain authn flaws")


def test_normalize_security_terms_mitre():
    assert "mitre" in semantic_light.normalize_security_terms("ATT&CK technique mapping")


def test_map_synonyms_idor():
    syn = semantic_light.map_synonyms("Explain IDOR")
    assert any("bola" in s for s in syn)


def test_map_synonyms_prompt_injection():
    syn = semantic_light.map_synonyms("Explain prompt injection")
    assert any("instruction override" in s or "jailbreak" in s for s in syn)


def test_expand_security_query_keeps_original_words():
    out = semantic_light.expand_security_query("Explain IDOR")
    assert "explain" in out
    assert "bola" in out


def test_concept_overlap_score_positive_when_expanded():
    chunk = {"text": "broken object level authorization is a class of api authz flaw"}
    score = semantic_light.concept_overlap_score("Explain IDOR", chunk)
    assert score > 0


def test_related_skill_score_positive_when_tag_token_in_query():
    chunk = {"text": "anything", "tags": ["BOLA"]}
    score = semantic_light.related_skill_score("What is bola?", chunk)
    assert score >= 0.5
