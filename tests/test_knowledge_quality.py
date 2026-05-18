from app import knowledge_loader, knowledge_quality


def setup_module(module):
    knowledge_loader.build_knowledge_index()


def test_score_all_documents_returns_one_per_doc():
    results = knowledge_quality.score_all_documents()
    docs = knowledge_loader.get_index()["documents"]
    assert len(results) == len(docs)


def test_score_in_range():
    for r in knowledge_quality.score_all_documents():
        assert 0.0 <= r["score"] <= 1.0


def test_score_components_present():
    for r in knowledge_quality.score_all_documents():
        for key in ("metadata_completeness", "domain_clarity",
                    "related_skills", "safe_use_forbidden_use",
                    "remediation_guidance", "citation_readiness"):
            assert key in r["components"]


def test_summary_shape():
    results = knowledge_quality.score_all_documents()
    summary = knowledge_quality.summarize_quality_scores(results)
    for key in ("count", "average", "min", "max"):
        assert key in summary


def test_summary_empty():
    s = knowledge_quality.summarize_quality_scores([])
    assert s["count"] == 0


def test_missing_metadata_lowers_score():
    bad_doc = {
        "metadata": {"id": "x"},
        "body": "no remediation no safety",
    }
    score = knowledge_quality.score_document_quality(bad_doc)["score"]
    good = knowledge_quality.score_all_documents()[0]["score"]
    assert score < good


def test_safe_use_forbidden_present_for_all():
    for r in knowledge_quality.score_all_documents():
        assert r["components"]["safe_use_forbidden_use"] == 1.0


def test_remediation_component_high_for_most():
    results = knowledge_quality.score_all_documents()
    high = sum(1 for r in results if r["components"]["remediation_guidance"] == 1.0)
    assert high >= 20


def test_citation_readiness_high_for_most():
    results = knowledge_quality.score_all_documents()
    high = sum(1 for r in results if r["components"]["citation_readiness"] == 1.0)
    assert high >= 20


def test_average_score_reasonable():
    summary = knowledge_quality.summarize_quality_scores(knowledge_quality.score_all_documents())
    assert summary["average"] >= 0.85
