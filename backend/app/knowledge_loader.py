"""Load Markdown knowledge documents from KNOWLEDGE_DIR."""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

from . import config
from . import metadata as meta_mod


def load_markdown_document(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    raw_meta = meta_mod.parse_front_matter(text)
    norm = meta_mod.normalize_metadata(raw_meta)
    body = meta_mod.extract_body(text)
    doc_id = meta_mod.build_document_id(path, norm)
    norm["id"] = doc_id
    return {
        "metadata": norm,
        "body": body,
        "path": str(path.relative_to(config.PROJECT_ROOT)).replace("\\", "/"),
    }


def load_all_knowledge_documents() -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []
    for md_path in sorted(config.KNOWLEDGE_DIR.rglob("*.md")):
        docs.append(load_markdown_document(md_path))
    return docs


@lru_cache(maxsize=1)
def _cached_index() -> dict[str, Any]:
    docs = load_all_knowledge_documents()
    by_id = {d["metadata"]["id"]: d for d in docs}
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for d in docs:
        by_domain[d["metadata"]["domain"]].append(d)
    return {
        "documents": docs,
        "by_id": by_id,
        "by_domain": dict(by_domain),
        "count": len(docs),
    }


def build_knowledge_index() -> dict[str, Any]:
    _cached_index.cache_clear()
    return _cached_index()


def get_index() -> dict[str, Any]:
    return _cached_index()


def group_documents_by_domain(docs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for d in docs:
        grouped[d["metadata"]["domain"]].append(d)
    return dict(grouped)


def get_document_by_id(doc_id: str) -> dict[str, Any] | None:
    return get_index()["by_id"].get(doc_id)


def summarize_knowledge_base() -> dict[str, Any]:
    index = get_index()
    counts = {domain: len(items) for domain, items in index["by_domain"].items()}
    return {
        "total_documents": index["count"],
        "domains": sorted(counts.keys()),
        "documents_per_domain": counts,
    }
