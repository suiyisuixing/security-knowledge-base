from app import knowledge_loader


def test_load_all_documents_returns_list():
    docs = knowledge_loader.load_all_knowledge_documents()
    assert isinstance(docs, list)


def test_load_all_documents_minimum_count():
    docs = knowledge_loader.load_all_knowledge_documents()
    assert len(docs) >= 32


def test_documents_have_metadata():
    docs = knowledge_loader.load_all_knowledge_documents()
    for d in docs:
        assert "metadata" in d
        assert "body" in d


def test_documents_have_id_and_title():
    docs = knowledge_loader.load_all_knowledge_documents()
    for d in docs:
        assert d["metadata"].get("id")
        assert d["metadata"].get("title")


def test_documents_have_domain():
    docs = knowledge_loader.load_all_knowledge_documents()
    for d in docs:
        assert d["metadata"].get("domain")


def test_documents_have_related_skills():
    docs = knowledge_loader.load_all_knowledge_documents()
    for d in docs:
        assert isinstance(d["metadata"].get("related_skills", []), list)
        assert len(d["metadata"].get("related_skills", [])) >= 1


def test_documents_have_safe_use():
    docs = knowledge_loader.load_all_knowledge_documents()
    for d in docs:
        assert isinstance(d["metadata"].get("safe_use", []), list)
        assert len(d["metadata"].get("safe_use", [])) >= 1


def test_documents_have_forbidden_use():
    docs = knowledge_loader.load_all_knowledge_documents()
    for d in docs:
        assert isinstance(d["metadata"].get("forbidden_use", []), list)
        assert len(d["metadata"].get("forbidden_use", [])) >= 1


def test_documents_have_unique_ids():
    docs = knowledge_loader.load_all_knowledge_documents()
    ids = [d["metadata"]["id"] for d in docs]
    assert len(set(ids)) == len(ids)


def test_index_is_cached():
    a = knowledge_loader.get_index()
    b = knowledge_loader.get_index()
    assert a is b


def test_group_documents_by_domain():
    docs = knowledge_loader.load_all_knowledge_documents()
    groups = knowledge_loader.group_documents_by_domain(docs)
    expected = {"ai_security", "api_security", "detection_engineering",
                "vulnerability_intelligence", "secure_coding", "safe_boundaries"}
    assert expected.issubset(set(groups.keys()))


def test_get_document_by_id_existing():
    doc = knowledge_loader.get_document_by_id("api-bola-001")
    assert doc is not None
    assert doc["metadata"]["title"].lower().startswith("broken object")


def test_get_document_by_id_missing():
    assert knowledge_loader.get_document_by_id("does-not-exist") is None


def test_summarize_knowledge_base():
    summary = knowledge_loader.summarize_knowledge_base()
    assert summary["total_documents"] >= 32
    assert "ai_security" in summary["domains"]


def test_documents_path_field_relative():
    docs = knowledge_loader.load_all_knowledge_documents()
    for d in docs:
        assert d["path"].startswith("knowledge/")


def test_build_knowledge_index_resets_cache():
    idx1 = knowledge_loader.get_index()
    idx2 = knowledge_loader.build_knowledge_index()
    assert idx2["count"] == idx1["count"]
