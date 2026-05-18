from retrieval import hybrid


def test_hybrid_search_returns_results_for_bola():
    results = hybrid.hybrid_search("broken object level authorization", top_k=5)
    assert len(results) >= 1
    assert any(r["doc_id"].startswith("api-bola") for r in results)


def test_hybrid_search_returns_results_for_prompt_injection():
    results = hybrid.hybrid_search("prompt injection", top_k=5)
    assert any(r["doc_id"].startswith("ai-prompt-injection") for r in results)


def test_hybrid_search_with_domain_filter():
    results = hybrid.hybrid_search("authorization", domain="api_security", top_k=5)
    for r in results:
        assert r["domain"] == "api_security"


def test_hybrid_search_empty_query():
    assert hybrid.hybrid_search("", top_k=5) == []


def test_combine_scores_weights():
    assert hybrid.combine_scores(1, 1, 1, 1) == 1.0


def test_explain_hybrid_score_string():
    res = hybrid.hybrid_search("BOLA", top_k=1)
    if res:
        s = hybrid.explain_hybrid_score(res[0])
        assert "lex=" in s


def test_compare_legacy_and_hybrid_returns_both():
    cmp = hybrid.compare_legacy_and_hybrid("Explain BOLA")
    assert "legacy" in cmp
    assert "hybrid" in cmp


def test_rerank_results_sorts_descending():
    results = [{"score": 1.0}, {"score": 3.0}, {"score": 2.0}]
    reranked = hybrid.rerank_results("q", results)
    scores = [r["score"] for r in reranked]
    assert scores == sorted(scores, reverse=True)
