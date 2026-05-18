from app import diagnostics


def test_backend_status_ok():
    s = diagnostics.get_backend_status()
    assert s["status"] == "ok"
    assert s["model_free"] is True
    assert s["fully_local"] is True


def test_data_status_lists_files():
    s = diagnostics.get_data_status()
    assert s["count"] >= 8


def test_memory_status_lists_files():
    s = diagnostics.get_memory_status()
    assert s["count"] >= 4


def test_knowledge_status_summary():
    s = diagnostics.get_knowledge_status()
    assert s["total_documents"] >= 32
    assert len(s["domains"]) >= 6


def test_frontend_expected_config():
    s = diagnostics.get_frontend_expected_config()
    assert s["backend_url"].startswith("http://localhost")


def test_health_diagnostics_keys():
    s = diagnostics.get_health_diagnostics()
    assert set(s.keys()) >= {"backend", "data", "memory", "knowledge", "frontend"}


def test_build_diagnostics_report_ok():
    r = diagnostics.build_diagnostics_report()
    assert r["integrity"]["ok"]
    assert r["schema_validation"]["all_valid"]
