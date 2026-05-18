from pathlib import Path

from app import metadata as meta_mod


SAMPLE = """---
id: api-bola-001
title: Broken Object Level Authorization
domain: api_security
difficulty: medium
related_projects:
  - vulnerability-intelligence-lab
related_skills:
  - api_authorization_reasoning
tags:
  - OWASP API
  - BOLA
safe_use:
  - local_lab
forbidden_use:
  - unauthorized_scanning
---

## Concept

body text here.
"""


def test_parse_front_matter_returns_dict():
    meta = meta_mod.parse_front_matter(SAMPLE)
    assert meta["id"] == "api-bola-001"


def test_parse_front_matter_title():
    meta = meta_mod.parse_front_matter(SAMPLE)
    assert meta["title"] == "Broken Object Level Authorization"


def test_parse_front_matter_lists():
    meta = meta_mod.parse_front_matter(SAMPLE)
    assert meta["related_projects"] == ["vulnerability-intelligence-lab"]
    assert "BOLA" in meta["tags"]


def test_extract_body():
    body = meta_mod.extract_body(SAMPLE)
    assert body.lstrip().startswith("## Concept")


def test_extract_body_no_front_matter_returns_text():
    text = "no front matter here"
    assert meta_mod.extract_body(text) == text


def test_parse_empty_front_matter_returns_empty_dict():
    assert meta_mod.parse_front_matter("no front matter") == {}


def test_validate_metadata_complete():
    meta = meta_mod.parse_front_matter(SAMPLE)
    missing = meta_mod.validate_metadata(meta)
    assert missing == []


def test_validate_metadata_missing_fields():
    incomplete = {"id": "x", "title": "y"}
    missing = meta_mod.validate_metadata(incomplete)
    assert "domain" in missing
    assert "safe_use" in missing


def test_normalize_metadata_lists_remain_lists():
    meta = meta_mod.parse_front_matter(SAMPLE)
    norm = meta_mod.normalize_metadata(meta)
    assert isinstance(norm["related_skills"], list)


def test_normalize_metadata_string_to_list():
    norm = meta_mod.normalize_metadata({"tags": "single"})
    assert norm["tags"] == ["single"]


def test_normalize_metadata_none_to_empty_list():
    norm = meta_mod.normalize_metadata({"tags": None})
    assert norm["tags"] == []


def test_normalize_metadata_strips_strings():
    norm = meta_mod.normalize_metadata({"id": " x ", "title": " y "})
    assert norm["id"] == "x"
    assert norm["title"] == "y"


def test_build_document_id_from_meta():
    assert meta_mod.build_document_id(Path("foo.md"), {"id": "abc"}) == "abc"


def test_build_document_id_fallback_to_stem():
    assert meta_mod.build_document_id(Path("foo.md"), {}) == "foo"


def test_metadata_to_tags_includes_tags():
    tags = meta_mod.metadata_to_tags({"tags": ["a", "b"], "domain": "x"})
    assert "a" in tags and "b" in tags and "x" in tags
