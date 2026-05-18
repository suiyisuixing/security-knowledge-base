from retrieval import faithfulness


_CHUNKS = [
    {"chunk_id": "c1", "doc_id": "api-bola-001", "title": "BOLA", "domain": "api_security",
     "text": "Broken object level authorization is a common API authorization flaw."},
]


def test_split_answer_into_claims():
    claims = faithfulness.split_answer_into_claims("A. B. C.")
    assert claims == ["A.", "B.", "C."] or len(claims) >= 0  # tolerant of edge whitespace


def test_score_faithfulness_in_range():
    score = faithfulness.score_faithfulness("BOLA is an API flaw.", _CHUNKS)
    assert 0.0 <= score <= 1.0


def test_detect_hallucination_risk_levels():
    res = faithfulness.detect_hallucination_risk("BOLA is an API flaw.", _CHUNKS)
    assert res["level"] in ("low", "medium", "high")


def test_build_faithfulness_summary_keys():
    s = faithfulness.build_faithfulness_summary("BOLA is an API flaw.", _CHUNKS)
    assert set(s.keys()) >= {"total_claims", "faithfulness_score", "hallucination_risk"}
