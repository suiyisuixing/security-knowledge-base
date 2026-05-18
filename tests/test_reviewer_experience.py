from pathlib import Path

from app import demo_assets

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_sample_outputs_dir_exists():
    assert (PROJECT_ROOT / "sample_outputs").is_dir()


def test_all_required_subdirs_present():
    base = PROJECT_ROOT / "sample_outputs"
    for sub in ("api_responses", "reports", "benchmark", "agent_readiness",
                "router_examples", "authorized_workflows"):
        assert (base / sub).is_dir(), f"missing sample_outputs/{sub}"


def test_at_least_15_sample_outputs():
    base = PROJECT_ROOT / "sample_outputs"
    total = sum(1 for _ in base.rglob("*.json"))
    assert total >= 15


def test_each_sample_has_sample_id_or_filename():
    samples = demo_assets.list_demo_samples()
    for s in samples:
        assert s.get("sample_id")


def test_router_examples_cover_a_b_c_d():
    samples = demo_assets.list_demo_samples()
    ids = {s["sample_id"] for s in samples}
    assert "route_rag_to_A" in ids
    assert "route_logs_to_B" in ids
    assert "route_cve_to_C" in ids
    assert "route_safety_to_D" in ids


def test_reviewer_docs_exist():
    docs = PROJECT_ROOT / "docs"
    assert (docs / "reviewer_quick_path.md").exists()
    assert (docs / "example_outputs.md").exists()
    assert (docs / "v3_1_reviewer_experience.md").exists()


def test_reviewer_path_step_actions_present():
    path = demo_assets.build_reviewer_path()
    actions = [s["action"] for s in path["steps"]]
    assert "Load knowledge domains" in actions
    assert "Run benchmark" in actions
    assert "Review portfolio value summary" in actions
