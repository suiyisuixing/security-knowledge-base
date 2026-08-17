from agent_hub import roadmap_planner


def test_build_v5_roadmap_marks_completed_milestones():
    r = roadmap_planner.build_v5_roadmap()
    assert all(m["done"] for m in r["milestones"])
    ids = [m["id"] for m in r["milestones"]]
    assert "reviewer-experience" in ids and "agent-hub" in ids
    assert r["version"] == "v5.0"


def test_build_v5_to_v6_roadmap_mentions_feature_flag():
    r = roadmap_planner.build_v5_to_v6_roadmap()
    assert "feature flag" in r["key_decision"].lower()


def test_build_release_checklist_for_v5():
    c = roadmap_planner.build_release_checklist("v5.0")
    assert "pytest pass" in c["items"]
    assert c["version"] == "v5.0"


def test_release_checklist_includes_author_check():
    c = roadmap_planner.build_release_checklist("v5.0")
    text = " ".join(c["items"])
    assert "suiyisuixing" in text


def test_release_notes_string_mentions_local_only():
    n = roadmap_planner.build_github_release_notes("v5.0")
    assert "Local-only" in n or "model-free" in n.lower()
