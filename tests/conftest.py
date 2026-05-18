"""pytest configuration for backend tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(scope="session")
def project_root() -> Path:
    return PROJECT_ROOT


@pytest.fixture
def fresh_index():
    from app import knowledge_loader
    return knowledge_loader.build_knowledge_index()


@pytest.fixture
def api_client():
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app) as client:
        yield client
