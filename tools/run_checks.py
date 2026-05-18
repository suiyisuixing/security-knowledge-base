"""Local-development check runner.

Runs: pytest, compileall (backend/app + reasoning/ + retrieval/ + agent_hub/
+ tests + tools), npm run build, and a few integrity-style sanity checks.

Subprocess is used here intentionally; backend/app code never imports it.
"""

from __future__ import annotations

import json
import shutil
import subprocess  # noqa: S404 (allowed in tools only)
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(label: str, args: list[str], cwd: Path | None = None) -> int:
    print(f"\n=== {label} ===")
    print("$", " ".join(args))
    try:
        proc = subprocess.run(args, cwd=str(cwd) if cwd else None, check=False)
        return proc.returncode
    except FileNotFoundError as exc:
        print(f"missing tool: {exc}")
        return 127


def check_readme_required_sections() -> int:
    print("\n=== README required sections ===")
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    required = (
        "Reviewer Quick Path",
        "Development Note",
        "Safety",  # any safety-related header
        "v5.0",
    )
    missing = [r for r in required if r not in text]
    if missing:
        print("MISSING:", missing)
        return 1
    print("OK")
    return 0


def check_ai_disclosure_no_named_provider() -> int:
    print("\n=== AI disclosure must not name a provider ===")
    forbidden = ("Claude", "Anthropic")
    fail = 0
    for fname in ("README.md", "README.zh-CN.md", "reports/SECURITY_REPORT.md"):
        path = ROOT / fname
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in text:
                print(f"FAIL: {fname} contains {needle!r}")
                fail = 1
    if not fail:
        print("OK")
    return fail


def check_no_llm_directory_present() -> int:
    print("\n=== No LLM directory present ===")
    if (ROOT / "llm").exists() or (ROOT / "model_config.json").exists():
        print("FAIL: llm/ or model_config.json found")
        return 1
    print("OK")
    return 0


def check_integrity_report() -> int:
    print("\n=== Backend integrity report ===")
    try:
        sys.path.insert(0, str(ROOT / "backend"))
        sys.path.insert(0, str(ROOT))
        from app import integrity_checker, schema_validator
        report = integrity_checker.build_integrity_report()
        if not report["ok"]:
            print("FAIL:", json.dumps(report["checks"], default=str)[:600])
            return 1
        schema_summary = schema_validator.summarize_schema_validation()
        if not schema_summary["all_valid"]:
            print("FAIL schemas:", schema_summary)
            return 1
        print("OK integrity + schema validation")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {exc}")
        return 1


def main() -> int:
    python = sys.executable
    failures: list[str] = []

    code = run("pytest", [python, "-m", "pytest", "-q"], cwd=ROOT)
    if code != 0:
        failures.append("pytest")

    code = run("compileall", [python, "-m", "compileall",
                              "backend/app", "tests", "tools",
                              "reasoning", "retrieval", "agent_hub"], cwd=ROOT)
    if code != 0:
        failures.append("compileall")

    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if npm:
        code = run("npm run build", [npm, "run", "build"], cwd=ROOT / "frontend")
        if code != 0:
            failures.append("npm run build")
    else:
        print("\n=== npm run build ===")
        print("npm not found on PATH; skipping frontend build check.")

    if check_readme_required_sections() != 0:
        failures.append("README required sections")
    if check_ai_disclosure_no_named_provider() != 0:
        failures.append("AI disclosure")
    if check_no_llm_directory_present() != 0:
        failures.append("no LLM directory")
    if check_integrity_report() != 0:
        failures.append("integrity report")

    print("\n=== summary ===")
    if failures:
        print("FAILED:", ", ".join(failures))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
