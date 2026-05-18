import pytest

from app import schema_validator


def test_load_schema_knowledge_metadata():
    s = schema_validator.load_schema("knowledge_metadata")
    assert s["$schema_name"] == "knowledge_metadata"


def test_load_schema_missing_raises():
    with pytest.raises(FileNotFoundError):
        schema_validator.load_schema("nonexistent_schema")


def test_validate_knowledge_metadata_all_valid():
    result = schema_validator.validate_knowledge_metadata_schema()
    assert result["valid"], result["errors"]
    assert result["checked"] >= 32


def test_validate_safety_policy_schema_valid():
    result = schema_validator.validate_safety_policy_schema()
    assert result["valid"], result["errors"]


def test_validate_skill_taxonomy_schema_valid():
    result = schema_validator.validate_skill_taxonomy_schema()
    assert result["valid"], result["errors"]


def test_validate_project_registry_schema_valid():
    result = schema_validator.validate_project_registry_schema()
    assert result["valid"], result["errors"]


def test_validate_benchmark_tasks_schema_valid():
    result = schema_validator.validate_benchmark_tasks_schema()
    assert result["valid"], result["errors"]


def test_validate_memory_schema_valid():
    result = schema_validator.validate_memory_schema()
    assert result["valid"], result["errors"]


def test_summarize_schema_validation_all_valid():
    summary = schema_validator.summarize_schema_validation()
    assert summary["all_valid"], summary


def test_validate_rejects_missing_required():
    bad = {"title": "Foo"}  # missing id, domain
    res = schema_validator.validate_json_against_schema(bad, "knowledge_metadata")
    assert not res["valid"]
    assert any("id" in e for e in res["errors"])


def test_validate_rejects_bad_enum():
    bad = {"id": "x", "title": "y", "domain": "not_a_domain"}
    res = schema_validator.validate_json_against_schema(bad, "knowledge_metadata")
    assert not res["valid"]


def test_validate_rejects_wrong_list_type():
    bad = {"id": "x", "title": "y", "domain": "ai_security", "tags": "should-be-list"}
    res = schema_validator.validate_json_against_schema(bad, "knowledge_metadata")
    assert not res["valid"]
