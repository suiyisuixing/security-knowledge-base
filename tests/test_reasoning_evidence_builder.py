from reasoning import evidence_builder


def test_select_supporting_documents_uses_retrieval():
    docs = evidence_builder.select_supporting_documents("Explain BOLA")
    assert isinstance(docs, list)


def test_select_relevant_skills_returns_list():
    s = evidence_builder.select_relevant_skills("Explain prompt injection")
    assert isinstance(s, list)


def test_select_related_projects_one_or_more():
    p = evidence_builder.select_related_projects("Explain prompt injection")
    assert len(p) >= 1


def test_build_evidence_chain_has_required_keys():
    chain = evidence_builder.build_evidence_chain("Explain BOLA")
    for k in ("retrieved_docs", "cited_doc_ids", "related_skills",
              "related_projects", "safety_policy_decision",
              "limitations", "recommended_next_step", "summary"):
        assert k in chain


def test_build_evidence_summary_string():
    chain = evidence_builder.build_evidence_chain("Explain BOLA")
    s = evidence_builder.build_evidence_summary(chain)
    assert isinstance(s, str)
    assert "docs=" in s


def test_evidence_chain_limitations_mention_local_only():
    chain = evidence_builder.build_evidence_chain("Explain BOLA")
    text = " ".join(chain["limitations"])
    assert "Local" in text or "local" in text


def test_evidence_chain_no_model_inference_claim():
    chain = evidence_builder.build_evidence_chain("Explain BOLA")
    text = " ".join(chain["limitations"])
    assert "no model" in text.lower() or "rule-based" in text.lower()
