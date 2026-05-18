from app import learning_path


def test_generate_ai_security_path_steps():
    steps = learning_path.generate_ai_security_path()
    assert len(steps) >= 3
    assert steps[0]["step"] == 1


def test_generate_detection_path_steps():
    steps = learning_path.generate_detection_engineering_path()
    ids = [s["skill_id"] for s in steps]
    assert "log_analysis" in ids
    assert "mitre_mapping" in ids


def test_generate_vuln_intelligence_path():
    steps = learning_path.generate_vulnerability_intelligence_path()
    ids = [s["skill_id"] for s in steps]
    assert "vulnerability_prioritization" in ids


def test_generate_secure_code_review_path():
    steps = learning_path.generate_secure_code_review_path()
    ids = [s["skill_id"] for s in steps]
    assert "secure_code_review" in ids


def test_generate_learning_path_ai_goal():
    path = learning_path.generate_learning_path("learn ai security")
    assert path["steps"]
    assert path["goal"] == "learn ai security"


def test_generate_learning_path_detection_goal():
    path = learning_path.generate_learning_path("improve detection in our soc")
    ids = [s["skill_id"] for s in path["steps"]]
    assert "log_analysis" in ids


def test_generate_learning_path_generic_falls_back():
    path = learning_path.generate_learning_path("general security")
    assert path["steps"]


def test_generate_learning_path_current_skills_marked():
    path = learning_path.generate_learning_path("ai security", current_skills=["prompt_injection_reasoning"])
    step = next(s for s in path["steps"] if s["skill_id"] == "prompt_injection_reasoning")
    assert "Already in progress" in step["notes"]


def test_summarize_learning_path_returns_string():
    path = learning_path.generate_learning_path("ai security")
    assert isinstance(learning_path.summarize_learning_path(path), str)


def test_learning_path_summary_field():
    path = learning_path.generate_learning_path("ai security")
    assert "steps" in path["summary"]
