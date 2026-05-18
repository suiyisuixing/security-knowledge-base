from app import skill_mapper


def test_list_skills_minimum_count():
    skills = skill_mapper.list_skills()
    assert len(skills) >= 16


def test_skills_have_required_fields():
    for s in skill_mapper.list_skills():
        assert s["skill_id"]
        assert s["name"]
        assert s["domain"]
        assert "description" in s


def test_get_skill_existing():
    s = skill_mapper.get_skill("prompt_injection_reasoning")
    assert s is not None
    assert s["domain"] == "ai_security"


def test_get_skill_missing():
    assert skill_mapper.get_skill("not-a-skill") is None


def test_map_query_to_skills_returns_list():
    assert isinstance(skill_mapper.map_query_to_skills("prompt injection"), list)


def test_map_query_prompt_injection():
    out = skill_mapper.map_query_to_skills("prompt injection in RAG")
    assert "prompt_injection_reasoning" in out


def test_map_query_logs():
    out = skill_mapper.map_query_to_skills("review my logs")
    assert "log_analysis" in out


def test_map_query_cve():
    out = skill_mapper.map_query_to_skills("prioritize this cve list")
    assert "vulnerability_prioritization" in out


def test_map_query_bola():
    out = skill_mapper.map_query_to_skills("bola in api")
    assert "api_authorization_reasoning" in out


def test_map_query_returns_empty_for_unrelated():
    assert skill_mapper.map_query_to_skills("totally unrelated topic xyz") == []


def test_map_document_to_skills_uses_meta():
    doc = {"metadata": {"related_skills": ["a", "b"]}}
    assert skill_mapper.map_document_to_skills(doc) == ["a", "b"]


def test_map_document_to_skills_empty_for_none():
    assert skill_mapper.map_document_to_skills({}) == []


def test_map_project_to_skills_llm():
    skills = skill_mapper.map_project_to_skills("llm-security-lab")
    assert "prompt_injection_reasoning" in skills


def test_map_project_to_skills_unknown():
    assert skill_mapper.map_project_to_skills("no-such-project") == []


def test_recommend_skills_for_goal_ai():
    recs = skill_mapper.recommend_skills_for_goal("learn ai security")
    assert "prompt_injection_reasoning" in recs


def test_recommend_skills_for_goal_detection():
    recs = skill_mapper.recommend_skills_for_goal("improve detection")
    assert "mitre_mapping" in recs


def test_recommend_skills_for_goal_dedup():
    recs = skill_mapper.recommend_skills_for_goal("ai security and ai security")
    assert len(recs) == len(set(recs))
