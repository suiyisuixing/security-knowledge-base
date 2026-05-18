from retrieval import retrieval_eval


def test_load_eval_cases_nonempty():
    cases = retrieval_eval.load_retrieval_eval_cases()
    assert len(cases) >= 10


def test_legacy_eval_pass_rate_reasonable():
    r = retrieval_eval.evaluate_legacy_retrieval()
    assert r["total"] == len(retrieval_eval.load_retrieval_eval_cases())
    assert 0.0 <= r["pass_rate"] <= 1.0


def test_hybrid_eval_pass_rate_reasonable():
    r = retrieval_eval.evaluate_hybrid_retrieval()
    assert r["total"] == len(retrieval_eval.load_retrieval_eval_cases())
    assert 0.0 <= r["pass_rate"] <= 1.0


def test_hybrid_pass_rate_at_least_half():
    r = retrieval_eval.evaluate_hybrid_retrieval()
    assert r["pass_rate"] >= 0.5


def test_compare_retrieval_methods_returns_both():
    cmp = retrieval_eval.compare_retrieval_methods()
    assert "legacy" in cmp and "hybrid" in cmp


def test_build_retrieval_eval_report_summary_keys():
    report = retrieval_eval.build_retrieval_eval_report()
    assert "summary" in report
    assert "details" in report
    assert "legacy_pass_rate" in report["summary"]
    assert "hybrid_pass_rate" in report["summary"]
