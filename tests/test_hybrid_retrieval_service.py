from app import hybrid_retrieval_service


def test_search_hybrid_knowledge_returns_list():
    res = hybrid_retrieval_service.search_hybrid_knowledge("Explain BOLA", top_k=5)
    assert isinstance(res, list)


def test_build_hybrid_grounded_answer_includes_safety_note():
    r = hybrid_retrieval_service.build_hybrid_grounded_answer("Explain BOLA")
    assert "Safety boundary" in r["safety_note"]


def test_build_hybrid_grounded_answer_classification():
    r = hybrid_retrieval_service.build_hybrid_grounded_answer("Explain BOLA")
    assert r["safety_classification"]["allowed"] is True


def test_compare_retrieval_modes_returns_diff():
    cmp = hybrid_retrieval_service.compare_retrieval_modes("Explain BOLA")
    assert "legacy" in cmp and "hybrid" in cmp


def test_evaluate_answer_grounding_keys():
    g = hybrid_retrieval_service.evaluate_answer_grounding("BOLA is an API flaw.", "Explain BOLA")
    assert "grounding" in g and "faithfulness" in g


def test_retrieval_quality_report_keys():
    r = hybrid_retrieval_service.build_retrieval_quality_report()
    assert set(r.keys()) >= {"evaluation", "conflicts", "source_trust", "chunk_summary"}
