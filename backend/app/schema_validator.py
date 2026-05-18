"""Lightweight JSON-schema-like validator (v3.2).

Implemented with the Python standard library; no third-party jsonschema
package. Supports a small but sufficient subset for the bundled schemas:

- required fields
- type check (string / number / object / dict / list / boolean)
- list item type / list item object schema
- enum check
- nested dict/object schema
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from . import config


_PRIMITIVES = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
}


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    path = config.SCHEMAS_DIR / f"{schema_name}.schema.json"
    if not path.exists():
        raise FileNotFoundError(f"schema not found: {schema_name}")
    return json.loads(path.read_text(encoding="utf-8"))


def _check_type(value: Any, type_name: str) -> bool:
    if type_name in _PRIMITIVES:
        return isinstance(value, _PRIMITIVES[type_name])
    if type_name in ("object", "dict"):
        return isinstance(value, dict)
    if type_name == "list":
        return isinstance(value, list)
    return True


def _validate_value(value: Any, schema: dict[str, Any], path: str) -> list[str]:
    errs: list[str] = []
    expected_type = schema.get("type")
    if expected_type and not _check_type(value, expected_type):
        errs.append(f"{path}: expected {expected_type}, got {type(value).__name__}")
        return errs
    enum_values = schema.get("enum")
    if enum_values is not None and value not in enum_values:
        errs.append(f"{path}: value '{value}' not in enum {enum_values}")
    if expected_type == "list" and isinstance(value, list):
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(value):
                errs.extend(_validate_value(item, item_schema, f"{path}[{idx}]"))
    if expected_type in ("object", "dict", None) and isinstance(value, dict):
        for req in schema.get("required", []) or []:
            if req not in value:
                errs.append(f"{path}: missing required field '{req}'")
        props = schema.get("properties") or {}
        for key, sub_schema in props.items():
            if key in value:
                errs.extend(_validate_value(value[key], sub_schema, f"{path}.{key}"))
    return errs


def validate_json_against_schema(data: Any, schema_name: str) -> dict[str, Any]:
    schema = load_schema(schema_name)
    errors = _validate_value(data, schema, "$")
    return {"schema": schema_name, "valid": not errors, "errors": errors}


def _load_json(rel: str) -> Any:
    return json.loads((config.PROJECT_ROOT / rel).read_text(encoding="utf-8"))


def validate_knowledge_metadata_schema() -> dict[str, Any]:
    from . import knowledge_loader
    docs = knowledge_loader.get_index()["documents"]
    aggregate_errors: list[str] = []
    for d in docs:
        result = validate_json_against_schema(d["metadata"], "knowledge_metadata")
        if not result["valid"]:
            for e in result["errors"]:
                aggregate_errors.append(f"{d['metadata'].get('id','?')}: {e}")
    return {
        "schema": "knowledge_metadata",
        "checked": len(docs),
        "valid": not aggregate_errors,
        "errors": aggregate_errors[:30],
    }


def validate_safety_policy_schema() -> dict[str, Any]:
    return validate_json_against_schema(_load_json("data/safety_policy.json"), "safety_policy")


def validate_skill_taxonomy_schema() -> dict[str, Any]:
    return validate_json_against_schema(_load_json("data/skill_taxonomy.json"), "skill_taxonomy")


def validate_project_registry_schema() -> dict[str, Any]:
    return validate_json_against_schema(_load_json("data/project_registry.json"), "project_registry")


def validate_benchmark_tasks_schema() -> dict[str, Any]:
    return validate_json_against_schema(_load_json("data/benchmark_tasks.json"), "benchmark_task")


def validate_memory_schema() -> dict[str, Any]:
    profile = _load_json("memory/user_learning_profile.json")
    return validate_json_against_schema(profile, "memory_profile")


def summarize_schema_validation() -> dict[str, Any]:
    checks = [
        validate_knowledge_metadata_schema(),
        validate_safety_policy_schema(),
        validate_skill_taxonomy_schema(),
        validate_project_registry_schema(),
        validate_benchmark_tasks_schema(),
        validate_memory_schema(),
    ]
    passed = sum(1 for c in checks if c["valid"])
    return {
        "total": len(checks),
        "passed": passed,
        "all_valid": passed == len(checks),
        "results": checks,
    }
