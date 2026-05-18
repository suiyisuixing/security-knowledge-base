from retrieval import knowledge_conflict


def test_detect_duplicate_documents_none_in_bundled():
    dups = knowledge_conflict.detect_duplicate_documents()
    assert dups == []


def test_detect_stale_documents_none_in_bundled():
    stale = knowledge_conflict.detect_stale_documents()
    # bundled docs should all be > 200 chars
    assert stale == []


def test_detect_policy_conflicts_none_in_bundled():
    conflicts = knowledge_conflict.detect_policy_conflicts()
    assert conflicts == []


def test_detect_conflicting_guidance_returns_list():
    assert isinstance(knowledge_conflict.detect_conflicting_guidance(), list)


def test_build_conflict_report_keys():
    report = knowledge_conflict.build_conflict_report()
    assert set(report.keys()) >= {"duplicates", "stale", "conflicts", "policy_conflicts"}
