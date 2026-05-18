from app import knowledge_loader
from retrieval import source_trust


def test_score_source_safety_for_real_doc():
    doc = knowledge_loader.get_index()["documents"][0]
    s = source_trust.score_source_safety(doc)
    assert 0.0 <= s <= 1.0


def test_score_source_domain_relevance_for_real_doc():
    doc = knowledge_loader.get_index()["documents"][0]
    s = source_trust.score_source_domain_relevance(doc)
    assert s >= 0.2


def test_score_source_freshness_default():
    s = source_trust.score_source_freshness({"metadata": {}})
    assert 0.0 <= s <= 1.0


def test_score_source_trust_empty_doc_zero():
    assert source_trust.score_source_trust({}) == 0.0


def test_score_source_trust_real_doc_positive():
    doc = knowledge_loader.get_index()["documents"][0]
    assert source_trust.score_source_trust(doc) > 0


def test_build_source_trust_report_for_all_docs():
    docs = knowledge_loader.get_index()["documents"]
    report = source_trust.build_source_trust_report(docs)
    assert report["count"] == len(docs)
    for item in report["items"]:
        assert "trust" in item
