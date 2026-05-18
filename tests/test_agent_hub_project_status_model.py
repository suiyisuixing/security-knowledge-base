from agent_hub import project_status_model as m


def test_project_status_construct():
    s = m.ProjectStatus(project_id="x", name="X")
    assert s.project_id == "x"


def test_project_skill_evidence_defaults():
    e = m.ProjectSkillEvidence(skill_id="s", project_id="p", evidence_type="t")
    assert e.confidence == 0.0
    assert e.status == "documented"


def test_validate_project_status_missing_project_id():
    issues = m.validate_project_status({"name": "x"})
    assert any("project_id" in i for i in issues)


def test_validate_project_status_missing_name():
    issues = m.validate_project_status({"project_id": "x"})
    assert any("name" in i for i in issues)


def test_validate_project_status_bad_level_type():
    issues = m.validate_project_status({"project_id": "x", "name": "n", "maturity_level": "high"})
    assert any("maturity_level" in i for i in issues)


def test_summarize_project_status_string():
    s = m.summarize_project_status({"project_id": "x", "maturity_level": 3, "focus": "y"})
    assert "x" in s
    assert "y" in s


def test_project_capability_construct():
    c = m.ProjectCapability(name="cap")
    assert c.name == "cap"


def test_project_maturity_score_construct():
    p = m.ProjectMaturityScore(project_id="x", level=1)
    assert p.level == 1
