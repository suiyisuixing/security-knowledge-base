from app import answer_builder, knowledge_loader, retrieval


def setup_module(module):
    knowledge_loader.build_knowledge_index()


def test_grounded_answer_includes_citations():
    results = retrieval.search_knowledge("prompt injection", top_k=3)
    a = answer_builder.build_grounded_answer("prompt injection", results)
    assert a["citations"]


def test_grounded_answer_contains_safety_note():
    results = retrieval.search_knowledge("bola", top_k=3)
    a = answer_builder.build_grounded_answer("bola", results)
    assert "safety boundary" in a["answer"].lower()


def test_grounded_answer_safety_note_field():
    results = retrieval.search_knowledge("bola", top_k=3)
    a = answer_builder.build_grounded_answer("bola", results)
    assert a["safety_note"]


def test_grounded_answer_related_skills():
    results = retrieval.search_knowledge("bola", top_k=3)
    a = answer_builder.build_grounded_answer("bola", results)
    assert isinstance(a["related_skills"], list)
    assert "api_authorization_reasoning" in a["related_skills"]


def test_grounded_answer_related_projects():
    results = retrieval.search_knowledge("bola", top_k=3)
    a = answer_builder.build_grounded_answer("bola", results)
    assert "vulnerability-intelligence-lab" in a["related_projects"]


def test_grounded_answer_no_results():
    a = answer_builder.build_grounded_answer("zzzznosuchterm", [])
    assert a["citations"] == []
    assert a["safety_note"]


def test_build_citations_dedupes():
    fake = [
        {"doc_id": "a", "title": "A", "domain": "x", "score": 1.0, "snippet": ""},
        {"doc_id": "a", "title": "A", "domain": "x", "score": 0.9, "snippet": ""},
    ]
    citations = answer_builder.build_citations(fake)
    assert len(citations) == 1


def test_build_citations_preserves_order():
    fake = [
        {"doc_id": "a", "title": "A", "domain": "x", "score": 1.0, "snippet": ""},
        {"doc_id": "b", "title": "B", "domain": "x", "score": 0.5, "snippet": ""},
    ]
    citations = answer_builder.build_citations(fake)
    assert [c["doc_id"] for c in citations] == ["a", "b"]


def test_build_safety_note_constant():
    note = answer_builder.build_safety_note([])
    assert "unauthorized scanning" in note.lower()


def test_answer_does_not_include_real_scanning_commands():
    results = retrieval.search_knowledge("ssrf", top_k=3)
    a = answer_builder.build_grounded_answer("ssrf", results)
    text = a["answer"].lower()
    for bad in ("nmap ", "masscan ", "sqlmap ", "ffuf ", "gobuster ", "nikto "):
        assert bad not in text


def test_answer_does_not_include_curl_attack_examples():
    results = retrieval.search_knowledge("bola", top_k=3)
    a = answer_builder.build_grounded_answer("bola", results)
    assert "curl -X POST https://" not in a["answer"]


def test_related_skills_unique():
    results = retrieval.search_knowledge("rag", top_k=5)
    a = answer_builder.build_grounded_answer("rag", results)
    assert len(a["related_skills"]) == len(set(a["related_skills"]))


def test_related_projects_unique():
    results = retrieval.search_knowledge("rag", top_k=5)
    a = answer_builder.build_grounded_answer("rag", results)
    assert len(a["related_projects"]) == len(set(a["related_projects"]))


def test_answer_field_contains_query():
    results = retrieval.search_knowledge("epss", top_k=2)
    a = answer_builder.build_grounded_answer("epss", results)
    assert "epss" in a["answer"].lower()


def test_answer_lists_doc_ids():
    results = retrieval.search_knowledge("epss", top_k=2)
    a = answer_builder.build_grounded_answer("epss", results)
    for r in results:
        assert r["doc_id"] in a["answer"]
