"""Lightweight YAML front-matter parsing (no external YAML dependency)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "id", "title", "domain", "difficulty",
    "related_projects", "related_skills", "tags",
    "safe_use", "forbidden_use",
}

_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def parse_front_matter(markdown_text: str) -> dict[str, Any]:
    match = _FRONT_MATTER_RE.match(markdown_text or "")
    if not match:
        return {}
    block = match.group(1)
    result: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") or line.startswith("- "):
            if current_list is None:
                current_list = []
                if current_key is not None:
                    result[current_key] = current_list
            item = line.split("-", 1)[1].strip()
            current_list.append(_parse_scalar(item))
            continue
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            current_key = key
            if value == "":
                current_list = []
                result[key] = current_list
            else:
                current_list = None
                result[key] = _parse_scalar(value)
    return result


def extract_body(markdown_text: str) -> str:
    match = _FRONT_MATTER_RE.match(markdown_text or "")
    if not match:
        return markdown_text or ""
    return markdown_text[match.end():]


def validate_metadata(meta: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in meta:
            missing.append(field)
    return missing


def normalize_metadata(meta: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(meta)
    for list_field in ("related_projects", "related_skills", "tags", "safe_use", "forbidden_use"):
        value = normalized.get(list_field)
        if value is None:
            normalized[list_field] = []
        elif isinstance(value, str):
            normalized[list_field] = [value]
    for str_field in ("id", "title", "domain", "difficulty"):
        if str_field in normalized and normalized[str_field] is not None:
            normalized[str_field] = str(normalized[str_field]).strip()
    return normalized


def build_document_id(path: Path | str, meta: dict[str, Any]) -> str:
    doc_id = meta.get("id")
    if isinstance(doc_id, str) and doc_id.strip():
        return doc_id.strip()
    return Path(str(path)).stem


def metadata_to_tags(meta: dict[str, Any]) -> list[str]:
    tags: list[str] = []
    for field in ("tags", "related_skills", "domain"):
        value = meta.get(field)
        if isinstance(value, list):
            tags.extend(str(v) for v in value)
        elif isinstance(value, str):
            tags.append(value)
    return tags
