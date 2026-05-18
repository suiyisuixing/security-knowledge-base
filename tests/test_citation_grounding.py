from retrieval import citation_grounding


_CHUNKS = [
    {"chunk_id": "c1", "doc_id": "api-bola-001", "title": "BOLA", "domain": "api_security",
     "text": "Broken object level authorization is a common API authorization flaw."},
    {"chunk_id": "c2", "doc_id": "api-bfla-001", "title": "BFLA", "domain": "api_security",
     "text": "Broken function level authorization affects function-level capabilities."},
]


def test_check_claim_supported():
    res = citation_grounding.check_claim_supported_by_chunks(
        "Broken object level authorization is an API flaw.", _CHUNKS,
    )
    assert res["supported"] is True


def test_check_claim_unsupported_for_unrelated():
    res = citation_grounding.check_claim_supported_by_chunks(
        "Cooking pasta is a fine art.", _CHUNKS,
    )
    assert res["supported"] is False


def test_build_grounded_citations_dedups_doc_ids():
    citations = citation_grounding.build_grounded_citations("some answer", _CHUNKS + _CHUNKS)
    ids = [c["doc_id"] for c in citations]
    assert len(ids) == len(set(ids))


def test_estimate_claim_support_score_in_range():
    score = citation_grounding.estimate_claim_support_score(
        "Broken object level authorization is an API flaw. Cooking pasta is fun.", _CHUNKS,
    )
    assert 0.0 <= score <= 1.0


def test_detect_uncited_claims_returns_list():
    answer = "Broken object level authorization is an API flaw. Cooking pasta is fun."
    uncited = citation_grounding.detect_uncited_claims(answer, _CHUNKS)
    assert isinstance(uncited, list)


def test_build_grounding_report_keys():
    report = citation_grounding.build_grounding_report("BOLA is an API flaw.", _CHUNKS)
    assert set(report.keys()) >= {"citations", "support_score", "uncited_claims"}
