from app import integrity_checker


def test_project_structure_ok():
    assert integrity_checker.check_project_structure()["ok"]


def test_required_files_ok():
    assert integrity_checker.check_required_files()["ok"]


def test_knowledge_docs_ok():
    res = integrity_checker.check_knowledge_docs()
    assert res["ok"], res
    assert res["total_docs"] >= 32


def test_data_files_ok():
    assert integrity_checker.check_data_files()["ok"]


def test_memory_files_ok():
    assert integrity_checker.check_memory_files()["ok"]


def test_sample_outputs_ok():
    assert integrity_checker.check_sample_outputs()["ok"]


def test_docs_consistency_ok():
    assert integrity_checker.check_docs_consistency()["ok"]


def test_no_forbidden_imports():
    res = integrity_checker.check_no_forbidden_imports()
    assert res["ok"], res["offenders"]


def test_no_external_api_usage():
    res = integrity_checker.check_no_external_api_usage()
    assert res["ok"], res["offenders"]


def test_no_real_scanning_tools():
    res = integrity_checker.check_no_real_scanning_tools()
    assert res["ok"], res["offenders"]


def test_no_model_integration():
    res = integrity_checker.check_no_model_integration()
    assert res["ok"], res["offenders"]


def test_build_integrity_report_ok():
    report = integrity_checker.build_integrity_report()
    assert report["ok"], report["checks"]
    assert len(report["checks"]) == 10
