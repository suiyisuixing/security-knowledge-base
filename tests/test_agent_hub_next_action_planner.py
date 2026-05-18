from agent_hub import next_action_planner


def test_recommend_next_project_actions_returns_list():
    actions = next_action_planner.recommend_next_project_actions()
    assert isinstance(actions, list)


def test_recommend_next_skill_actions_returns_list():
    actions = next_action_planner.recommend_next_skill_actions()
    assert isinstance(actions, list)


def test_recommend_next_documentation_actions_min_two():
    actions = next_action_planner.recommend_next_documentation_actions()
    assert len(actions) >= 2


def test_recommend_next_testing_actions_min_two():
    actions = next_action_planner.recommend_next_testing_actions()
    assert len(actions) >= 2


def test_recommend_next_demo_actions_nonempty():
    actions = next_action_planner.recommend_next_demo_actions()
    assert len(actions) >= 1


def test_build_30_day_plan_has_safety_boundary():
    p = next_action_planner.build_30_day_plan()
    assert "safety_boundary" in p
    assert "local" in p["safety_boundary"].lower()


def test_build_version_roadmap_from_v5_mentions_v6():
    r = next_action_planner.build_version_roadmap_from_v5()
    versions = [item["version"] for item in r["next"]]
    assert any(v.startswith("v6") for v in versions)
