"""Project paths and safe path resolution.

All file access in this project is constrained to PROJECT_ROOT.
Path-traversal attempts (e.g. ``..``, absolute escapes, symlinks pointing
outside the project tree) are rejected before any I/O happens.
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR: Path = PROJECT_ROOT / "knowledge"
DATA_DIR: Path = PROJECT_ROOT / "data"
MEMORY_DIR: Path = PROJECT_ROOT / "memory"
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
LOGS_DIR: Path = PROJECT_ROOT / "logs"

PROJECT_VERSION: str = "5.0"
SCHEMAS_DIR: Path = PROJECT_ROOT / "schemas"
SAMPLE_OUTPUTS_DIR: Path = PROJECT_ROOT / "sample_outputs"
REASONING_DIR: Path = PROJECT_ROOT / "reasoning"
RETRIEVAL_DIR: Path = PROJECT_ROOT / "retrieval"
AGENT_HUB_DIR: Path = PROJECT_ROOT / "agent_hub"


def get_project_version() -> str:
    return PROJECT_VERSION


def _safe_resolve(base: Path, relative_path: str) -> Path:
    rel = (relative_path or "").strip().replace("\\", "/").lstrip("/")
    if not rel:
        raise ValueError("relative_path must not be empty")
    if ".." in rel.split("/"):
        raise ValueError("path traversal not allowed")
    candidate = (base / rel).resolve()
    base_resolved = base.resolve()
    try:
        candidate.relative_to(base_resolved)
    except ValueError as exc:
        raise ValueError(f"path escapes base directory: {relative_path}") from exc
    return candidate


def safe_resolve_project_path(relative_path: str) -> Path:
    return _safe_resolve(PROJECT_ROOT, relative_path)


def safe_resolve_knowledge_path(relative_path: str) -> Path:
    return _safe_resolve(KNOWLEDGE_DIR, relative_path)


def safe_resolve_data_path(relative_path: str) -> Path:
    return _safe_resolve(DATA_DIR, relative_path)


def safe_resolve_memory_path(relative_path: str) -> Path:
    return _safe_resolve(MEMORY_DIR, relative_path)


def list_project_files() -> list[str]:
    skip_dirs = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache",
                 "dist", ".vite", "logs"}
    out: list[str] = []
    for path in PROJECT_ROOT.rglob("*"):
        if path.is_dir():
            continue
        parts = set(path.relative_to(PROJECT_ROOT).parts)
        if parts & skip_dirs:
            continue
        out.append(str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"))
    return sorted(out)
