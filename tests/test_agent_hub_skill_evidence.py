from agent_hub import skill_evidence


def test_load_skill_evidence_map():
    data = skill_evidence.load_skill_evidence_map()
    assert "records" in data
    assert len(data["records"]) >= 10


def test_get_evidence_for_skill_safety():
    recs = skill_evidence.get_evidence_for_skill("safety_boundary_classification")
    assert len(recs) >= 1


def test_get_evidence_for_skill_missing():
    assert skill_evidence.get_evidence_for_skill("nonexistent_skill_zzz") == []


def test_get_evidence_for_project_knowledge_base():
    recs = skill_evidence.get_evidence_for_project("security-knowledge-base")
    assert len(recs) >= 1


def test_add_evidence_record_returns_record():
    r = skill_evidence.add_evidence_record("test_skill_x", "security-knowledge-base", "x.py", "code", 0.9)
    assert r["skill_id"] == "test_skill_x"
    assert r["status"] == "implemented"


def test_score_skill_evidence_for_known_skill():
    s = skill_evidence.score_skill_evidence("safety_boundary_classification")
    assert s > 0


def test_score_project_evidence_for_known_project():
    s = skill_evidence.score_project_evidence("security-knowledge-base")
    assert s > 0


def test_build_skill_evidence_report_keys():
    report = skill_evidence.build_skill_evidence_report()
    assert "count" in report and "items" in report


def test_build_missing_evidence_report_returns_list():
    report = skill_evidence.build_missing_evidence_report()
    assert "missing_skills" in report
