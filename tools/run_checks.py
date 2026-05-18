"""Local-development check runner.

Runs: pytest, compileall, and npm run build (if frontend is installed).
Subprocess is used here intentionally; backend/app code never imports it.
"""

from __future__ import annotations

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


def main() -> int:
    python = sys.executable
    failures: list[str] = []

    code = run("pytest", [python, "-m", "pytest", "-q"], cwd=ROOT)
    if code != 0:
        failures.append("pytest")

    code = run("compileall", [python, "-m", "compileall",
                              "backend/app", "tests", "tools"], cwd=ROOT)
    if code != 0:
        failures.append("compileall")

    npm = shutil.which("npm")
    if npm:
        code = run("npm run build", [npm, "run", "build"], cwd=ROOT / "frontend")
        if code != 0:
            failures.append("npm run build")
    else:
        print("\n=== npm run build ===")
        print("npm not found on PATH; skipping frontend build check.")

    print("\n=== summary ===")
    if failures:
        print("FAILED:", ", ".join(failures))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
