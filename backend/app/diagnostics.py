"""Backend diagnostics (v3.2)."""

from __future__ import annotations

from typing import Any

from . import config
from . import integrity_checker
from . import schema_validator


def get_backend_status() -> dict[str, Any]:
    return {
        "status": "ok",
        "version": config.get_project_version(),
        "model_free": True,
        "fully_local": True,
        "deterministic": True,
    }


def get_data_status() -> dict[str, Any]:
    data_dir = config.DATA_DIR
    files: list[dict[str, Any]] = []
    if data_dir.exists():
        for path in sorted(data_dir.glob("*.json")):
            files.append({
                "name": path.name,
                "bytes": path.stat().st_size,
            })
    return {"count": len(files), "files": files}


def get_memory_status() -> dict[str, Any]:
    mem_dir = config.MEMORY_DIR
    files = []
    if mem_dir.exists():
        for path in sorted(mem_dir.glob("*.json")):
            files.append({"name": path.name, "bytes": path.stat().st_size})
    return {"count": len(files), "files": files}


def get_knowledge_status() -> dict[str, Any]:
    from . import knowledge_loader
    summary = knowledge_loader.summarize_knowledge_base()
    return summary


def get_frontend_expected_config() -> dict[str, Any]:
    return {
        "backend_url": "http://localhost:8000",
        "frontend_dev_url": "http://localhost:5173",
        "version": config.get_project_version(),
    }


def get_health_diagnostics() -> dict[str, Any]:
    return {
        "backend": get_backend_status(),
        "data": get_data_status(),
        "memory": get_memory_status(),
        "knowledge": get_knowledge_status(),
        "frontend": get_frontend_expected_config(),
    }


def build_diagnostics_report() -> dict[str, Any]:
    return {
        "health": get_health_diagnostics(),
        "integrity": integrity_checker.build_integrity_report(),
        "schema_validation": schema_validator.summarize_schema_validation(),
    }
