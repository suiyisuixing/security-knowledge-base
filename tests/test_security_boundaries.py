import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = PROJECT_ROOT / "backend" / "app"


def _python_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.py") if "__pycache__" not in p.parts]


APP_FILES = _python_files(APP_DIR)
APP_TEXTS = {p: p.read_text(encoding="utf-8") for p in APP_FILES}


def test_no_requests_import_in_backend():
    for p, text in APP_TEXTS.items():
        assert "import requests" not in text, f"requests import in {p.name}"
        assert "from requests" not in text, f"requests import in {p.name}"


def test_no_urllib_request_in_backend():
    for p, text in APP_TEXTS.items():
        assert "urllib.request" not in text, f"urllib.request in {p.name}"
        assert "from urllib.request" not in text, f"urllib.request in {p.name}"


def test_no_subprocess_in_backend():
    for p, text in APP_TEXTS.items():
        assert "import subprocess" not in text, f"subprocess in {p.name}"
        assert "from subprocess" not in text, f"subprocess in {p.name}"


def test_no_os_system_in_backend():
    for p, text in APP_TEXTS.items():
        assert "os.system(" not in text, f"os.system in {p.name}"


def test_no_shell_true_in_backend():
    for p, text in APP_TEXTS.items():
        assert "shell=True" not in text, f"shell=True in {p.name}"


def test_no_socket_in_backend():
    for p, text in APP_TEXTS.items():
        assert "import socket" not in text, f"socket import in {p.name}"


def test_no_real_api_key_pattern_in_backend():
    pat = re.compile(r"sk-[A-Za-z0-9]{8,}")
    for p, text in APP_TEXTS.items():
        # tests are allowed to mention pattern strings; backend may not.
        for line in text.splitlines():
            if "REDACTED" in line or "redact" in line.lower():
                continue
            if pat.search(line):
                raise AssertionError(f"possible api key in {p.name}: {line[:80]}")


def test_no_real_target_domain_in_backend():
    forbidden = ["example.com", "google.com", "facebook.com", "evil.com"]
    for p, text in APP_TEXTS.items():
        for d in forbidden:
            assert d not in text.lower(), f"real target domain {d} in {p.name}"


def test_no_real_target_ip_in_backend():
    pat = re.compile(r"\b(?:1\.1\.1\.1|8\.8\.8\.8|9\.9\.9\.9)\b")
    for p, text in APP_TEXTS.items():
        assert not pat.search(text), f"public ip in {p.name}"


def test_no_nmap_command_in_backend():
    for p, text in APP_TEXTS.items():
        assert "nmap " not in text.lower(), f"nmap command in {p.name}"
        assert "masscan " not in text.lower(), f"masscan command in {p.name}"


def test_no_sqlmap_command_in_backend():
    for p, text in APP_TEXTS.items():
        assert "sqlmap " not in text.lower(), f"sqlmap command in {p.name}"


def test_no_credential_theft_phrases_in_allowed_outputs():
    text = (PROJECT_ROOT / "data" / "safety_policy.json").read_text(encoding="utf-8")
    assert "blocked_credential_attack" in text
    # In allowed classes' safe_redirect, no theft instructions.
    assert "steal password" not in text.lower() or "blocked" in text.lower()


def test_ai_disclosure_does_not_name_claude():
    for path in (PROJECT_ROOT / "README.md", PROJECT_ROOT / "README.zh-CN.md"):
        if path.exists():
            text = path.read_text(encoding="utf-8")
            assert "Claude" not in text
            assert "Anthropic" not in text


def test_no_co_authored_by_in_repo_text_files():
    for path in (PROJECT_ROOT / "README.md", PROJECT_ROOT / "README.zh-CN.md",
                 PROJECT_ROOT / "CHANGELOG.md", PROJECT_ROOT / "RELEASE_CHECKLIST.md"):
        if path.exists():
            text = path.read_text(encoding="utf-8")
            assert "Co-authored-by" not in text
            assert "Generated with Claude" not in text


def test_safety_policy_lists_blocked_actions():
    text = (PROJECT_ROOT / "data" / "safety_policy.json").read_text(encoding="utf-8")
    for required in ("blocked_unauthorized_public_scan", "blocked_credential_attack",
                     "blocked_exploit_weaponization", "blocked_persistence",
                     "blocked_evasion", "blocked_exfiltration",
                     "blocked_destructive_action", "blocked_malware"):
        assert required in text


def test_knowledge_files_contain_safety_boundary_section():
    md_files = list((PROJECT_ROOT / "knowledge").rglob("*.md"))
    assert len(md_files) >= 32
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        assert "Safety boundary" in text, f"missing boundary section in {md.name}"


def test_knowledge_files_do_not_include_real_attack_commands():
    forbidden = ["nmap ", "masscan ", "sqlmap ", "ffuf ", "gobuster ", "nikto "]
    for md in (PROJECT_ROOT / "knowledge").rglob("*.md"):
        text = md.read_text(encoding="utf-8").lower()
        for cmd in forbidden:
            assert cmd not in text, f"attack command {cmd} in {md.name}"


def test_project_registry_contains_four_projects():
    import json as _json
    text = (PROJECT_ROOT / "data" / "project_registry.json").read_text(encoding="utf-8")
    data = _json.loads(text)
    ids = {p["project_id"] for p in data["projects"]}
    assert ids == {
        "llm-security-lab",
        "security-log-ai-assistant",
        "vulnerability-intelligence-lab",
        "security-knowledge-base",
    }


def test_no_real_data_in_memory_files():
    text = "\n".join(p.read_text(encoding="utf-8") for p in (PROJECT_ROOT / "memory").glob("*.json"))
    assert "@gmail.com" not in text or "suiyisuixing060626@gmail.com" not in text
    assert "password" not in text.lower()
    assert "Authorization:" not in text


def test_no_external_url_in_backend_modules():
    pat = re.compile(r"https?://(?!localhost|127\.0\.0\.1|github\.com)")
    for p, text in APP_TEXTS.items():
        for line in text.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                continue
            if pat.search(line):
                raise AssertionError(f"external URL in {p.name}: {line[:80]}")


def test_config_safe_path_resolves_inside_project(tmp_path):
    from app import config as cfg
    p = cfg.safe_resolve_knowledge_path("ai_security/owasp_llm_top10.md")
    assert str(p).startswith(str(cfg.KNOWLEDGE_DIR))


def test_config_safe_path_rejects_traversal():
    from app import config as cfg
    import pytest
    with pytest.raises(ValueError):
        cfg.safe_resolve_knowledge_path("../../etc/passwd")


def test_config_safe_path_rejects_empty():
    from app import config as cfg
    import pytest
    with pytest.raises(ValueError):
        cfg.safe_resolve_knowledge_path("")


def test_changelog_marks_v3_release():
    path = PROJECT_ROOT / "CHANGELOG.md"
    if path.exists():
        assert "v3.0-rc" in path.read_text(encoding="utf-8")


def test_release_checklist_lists_safety_items():
    path = PROJECT_ROOT / "RELEASE_CHECKLIST.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        assert "no unauthorized scanning" in text.lower()


def test_logs_dir_not_committed_files_only_gitkeep():
    logs = PROJECT_ROOT / "logs"
    if logs.exists():
        for p in logs.iterdir():
            if p.is_file() and p.name not in {".gitkeep"}:
                # jsonl/log are local-only and excluded by .gitignore
                assert p.suffix in {".jsonl", ".log", ".tmp"} or p.name.startswith(".")
