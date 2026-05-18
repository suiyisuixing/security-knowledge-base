from app import knowledge_loader, retrieval


def setup_module(module):
    knowledge_loader.build_knowledge_index()


def test_tokenize_basic():
    tokens = retrieval.tokenize("Prompt Injection in RAG systems")
    assert "prompt" in tokens
    assert "injection" in tokens


def test_tokenize_removes_stopwords():
    tokens = retrieval.tokenize("the and a")
    assert tokens == []


def test_tokenize_empty():
    assert retrieval.tokenize("") == []


def test_tokenize_drops_short_tokens():
    tokens = retrieval.tokenize("a bc def")
    assert "a" not in tokens


def test_search_returns_relevant_doc_for_prompt_injection():
    results = retrieval.search_knowledge("prompt injection", top_k=5)
    assert results
    assert any(r["doc_id"].startswith("ai-prompt-injection") for r in results)


def test_search_returns_relevant_doc_for_bola():
    results = retrieval.search_knowledge("bola authorization", top_k=5)
    assert results
    assert any(r["doc_id"].startswith("api-bola") for r in results)


def test_search_returns_relevant_doc_for_cvss():
    results = retrieval.search_knowledge("cvss", top_k=5)
    assert results
    assert any(r["doc_id"].startswith("vuln-cvss") for r in results)


def test_search_domain_filter():
    results = retrieval.search_knowledge("authorization", domain="api_security", top_k=10)
    for r in results:
        assert r["domain"] == "api_security"


def test_search_no_query_returns_empty():
    assert retrieval.search_knowledge("", top_k=5) == []


def test_search_unknown_term_returns_empty_or_low():
    results = retrieval.search_knowledge("zzzzznotaword12345", top_k=5)
    assert results == []


def test_search_top_k_limit():
    results = retrieval.search_knowledge("safety", top_k=2)
    assert len(results) <= 2


def test_search_by_tags_returns_matches():
    results = retrieval.search_by_tags(["BOLA"], top_k=5)
    assert any(r["doc_id"].startswith("api-bola") for r in results)


def test_search_by_tags_empty_input():
    assert retrieval.search_by_tags([], top_k=5) == []


def test_explain_search_shape():
    results = retrieval.search_knowledge("prompt injection", top_k=3)
    explanation = retrieval.explain_search("prompt injection", results)
    assert "tokens" in explanation
    assert "top_doc_ids" in explanation
    assert explanation["result_count"] == len(results)


def test_compute_idf_returns_floats():
    docs = knowledge_loader.load_all_knowledge_documents()
    idf = retrieval.compute_idf(docs)
    assert all(isinstance(v, float) for v in idf.values())
