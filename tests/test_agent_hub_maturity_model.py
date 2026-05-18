from agent_hub import maturity_model


def test_load_maturity_model_has_five_levels():
    m = maturity_model.load_maturity_model()
    assert len(m["levels"]) == 5


def test_score_project_against_model():
    s = maturity_model.score_project_against_model("security-knowledge-base")
    assert s["level"] >= 4
    assert s["name"]


def test_score_all_projects_returns_four():
    scores = maturity_model.score_all_projects()
    assert len(scores) == 4


def test_summarize_maturity_scores_keys():
    s = maturity_model.summarize_maturity_scores()
    assert set(s.keys()) >= {"total", "by_level", "avg_level"}


def test_summarize_maturity_total_is_four():
    s = maturity_model.summarize_maturity_scores()
    assert s["total"] == 4


def test_recommend_maturity_improvements_returns_list():
    imps = maturity_model.recommend_maturity_improvements()
    assert isinstance(imps, list)
