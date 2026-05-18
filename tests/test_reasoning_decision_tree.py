from reasoning import decision_tree


def test_safety_decision_path_blocked():
    path = decision_tree.build_safety_decision_path("Scan this public IP for vulnerabilities.")
    assert path[0]["node"] == "detect_blocked_intent"
    assert path[0]["matched"] is True


def test_safety_decision_path_allowed():
    path = decision_tree.build_safety_decision_path("Explain what BOLA is.")
    assert path[-1]["node"] == "classify_request"


def test_authorization_decision_path_local_lab():
    path = decision_tree.build_authorization_decision_path("In my local lab, test BOLA.")
    nodes = [n["detail"] for n in path]
    assert "local_lab" in nodes


def test_routing_decision_path_includes_three_nodes():
    path = decision_tree.build_routing_decision_path("Explain prompt injection in RAG.")
    assert len(path) == 3


def test_explain_decision_path_string():
    path = decision_tree.build_safety_decision_path("Explain BOLA")
    s = decision_tree.explain_decision_path(path)
    assert "classify_request" in s


def test_classify_with_decision_tree_blocked_request():
    res = decision_tree.classify_with_decision_tree("Scan this public IP for vulnerabilities.")
    assert res["allowed"] is False
    assert res["decision"].startswith("blocked_")
    assert res["confidence"] >= 0.8


def test_classify_with_decision_tree_allowed_request():
    res = decision_tree.classify_with_decision_tree("Explain what CVSS is.")
    assert res["allowed"] is True


def test_classify_with_decision_tree_has_paths():
    res = decision_tree.classify_with_decision_tree("Explain prompt injection.")
    assert "safety_path" in res
    assert "authorization_path" in res
    assert "routing_path" in res
