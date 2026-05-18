from app import answer_builder, citation_evaluator, knowledge_loader, retrieval


def setup_module(module):
    knowledge_loader.build_knowledge_index()


def _answer(query="prompt injection"):
    results = retrieval.search_knowledge(query, top_k=3)
    return answer_builder.build_grounded_answer(query, results)


def test_cited_docs_exist_true_for_real_answer():
    a = _answer()
    assert citation_evaluator.check_cited_docs_exist(a) is True


def test_cited_docs_exist_false_for_unknown():
    fake = {"citations": [{"doc_id": "no-such", "title": "x", "domain": "x"}],
            "answer": "x", "safety_note": "x"}
    assert citation_evaluator.check_cited_docs_exist(fake) is False


def test_safety_note_present_true():
    a = _answer()
    assert citation_evaluator.check_safety_note_present(a) is True


def test_safety_note_present_false():
    a = {"citations": [], "answer": "", "safety_note": ""}
    assert citation_evaluator.check_safety_note_present(a) is False


def test_unsupported_claims_when_no_citations():
    a = {"citations": [], "answer": "long answer with claims", "safety_note": "n"}
    assert citation_evaluator.check_unsupported_claims(a)


def test_no_unsupported_claims_for_grounded():
    a = _answer()
    assert citation_evaluator.check_unsupported_claims(a) == []


def test_evaluate_answer_citations_shape():
    a = _answer()
    result = citation_evaluator.evaluate_answer_citations(a)
    for key in ("cited_docs_exist", "safety_note_present", "unsupported_claims", "notes"):
        assert key in result


def test_summarize_citation_quality_shape():
    rs = [citation_evaluator.evaluate_answer_citations(_answer(q)) for q in ("bola", "cvss", "ssrf")]
    summary = citation_evaluator.summarize_citation_quality(rs)
    for key in ("total", "ok", "ok_rate"):
        assert key in summary


def test_summarize_empty():
    s = citation_evaluator.summarize_citation_quality([])
    assert s["total"] == 0


def test_evaluate_answer_notes_review_required_for_bad():
    bad = {"citations": [], "answer": "claim", "safety_note": ""}
    result = citation_evaluator.evaluate_answer_citations(bad)
    assert result["notes"] == "review required"
