"""v5-specific security boundary checks."""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _py_files(*dirs: str) -> list[Path]:
    out: list[Path] = []
    for d in dirs:
        p = PROJECT_ROOT / d
        if not p.exists():
            continue
        out.extend(x for x in p.rglob("*.py") if "__pycache__" not in x.parts)
    return out


_NEW_DIRS = ("backend/app", "reasoning", "retrieval", "agent_hub")


def test_no_requests_import_in_new_dirs():
    for p in _py_files(*_NEW_DIRS):
        if p.name == "integrity_checker.py":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        assert "import requests" not in text


def test_no_urllib_request_in_new_dirs():
    for p in _py_files(*_NEW_DIRS):
        if p.name == "integrity_checker.py":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        assert "urllib.request" not in text


def test_no_subprocess_in_new_dirs():
    for p in _py_files(*_NEW_DIRS):
        if p.name == "integrity_checker.py":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        assert "import subprocess" not in text


def test_no_os_system_in_new_dirs():
    for p in _py_files(*_NEW_DIRS):
        if p.name == "integrity_checker.py":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        assert "os.system(" not in text


def test_no_shell_true_in_new_dirs():
    for p in _py_files(*_NEW_DIRS):
        if p.name == "integrity_checker.py":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        assert "shell=True" not in text


def test_no_llm_provider_imports_in_new_dirs():
    forbidden = ("import openai", "from openai", "import anthropic", "from anthropic",
                 "import google.generativeai", "import ollama", "llama_cpp", "lmstudio")
    for p in _py_files(*_NEW_DIRS):
        if p.name == "integrity_checker.py":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        for needle in forbidden:
            assert needle not in text, f"{p.name} contains forbidden {needle}"


def test_no_llm_directory_present():
    assert not (PROJECT_ROOT / "llm").exists()


def test_no_model_config_file_present():
    assert not (PROJECT_ROOT / "model_config.json").exists()


def test_no_external_url_in_new_dirs():
    pat = re.compile(r"https?://(?!localhost|127\.0\.0\.1|github\.com)")
    for p in _py_files(*_NEW_DIRS):
        if p.name == "integrity_checker.py":
            continue
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            stripped = line.lstrip()
            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                continue
            if pat.search(line):
                raise AssertionError(f"external URL in {p.name}: {line[:80]}")


def test_no_real_target_in_new_dirs():
    forbidden = ("example.com", "google.com", "facebook.com")
    for p in _py_files(*_NEW_DIRS):
        if p.name == "integrity_checker.py":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
        for d in forbidden:
            assert d not in text


def test_ai_disclosure_no_claude_in_new_docs():
    for name in ("v3_1_reviewer_experience.md", "v3_2_stability_model.md",
                 "v4_rule_based_reasoning.md", "v4_5_hybrid_retrieval.md"):
        path = PROJECT_ROOT / "docs" / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            assert "Claude" not in text
            assert "Anthropic" not in text


def test_data_synonyms_no_external_url():
    syn = PROJECT_ROOT / "data" / "security_synonyms.json"
    if syn.exists():
        text = syn.read_text(encoding="utf-8")
        assert "https://" not in text


def test_agent_hub_does_not_open_outside_files(tmp_path):
    """agent_hub should only read bundled data, never outside paths."""
    from agent_hub import project_adapter
    summary = project_adapter.build_project_adapter_summary("llm-security-lab")
    assert summary["project_id"] == "llm-security-lab"


def test_orchestrator_blocked_request_returns_blocked_classification():
    from agent_hub import agent_orchestrator
    r = agent_orchestrator.produce_orchestration_result("Brute force this login.")
    assert r["classification"]["allowed"] is False
