"""Document chunker (v4.5)."""

from __future__ import annotations

from typing import Any


def build_chunk_id(doc_id: str, chunk_index: int) -> str:
    return f"{doc_id}#chunk-{chunk_index:03d}"


def chunk_document(doc: dict[str, Any], max_chars: int = 1200, overlap: int = 150) -> list[dict[str, Any]]:
    body = doc.get("body", "") or ""
    meta = doc.get("metadata", {}) or {}
    doc_id = meta.get("id", "unknown")
    if not body:
        return []
    chunks: list[dict[str, Any]] = []
    step = max(1, max_chars - overlap)
    idx = 0
    pos = 0
    while pos < len(body):
        end = min(len(body), pos + max_chars)
        text = body[pos:end].strip()
        if text:
            chunks.append({
                "chunk_id": build_chunk_id(doc_id, idx),
                "doc_id": doc_id,
                "domain": meta.get("domain", ""),
                "title": meta.get("title", ""),
                "tags": list(meta.get("tags", []) or []),
                "text": text,
                "start": pos,
                "end": end,
            })
            idx += 1
        if end == len(body):
            break
        pos += step
    return chunks


def chunk_all_documents(docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for d in docs:
        out.extend(chunk_document(d))
    return out


def extract_chunk_metadata(doc: dict[str, Any], chunk: dict[str, Any]) -> dict[str, Any]:
    meta = doc.get("metadata", {})
    return {
        "chunk_id": chunk.get("chunk_id"),
        "doc_id": meta.get("id"),
        "title": meta.get("title"),
        "domain": meta.get("domain"),
        "tags": meta.get("tags", []),
    }


def summarize_chunks(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    by_doc: dict[str, int] = {}
    by_domain: dict[str, int] = {}
    for c in chunks:
        by_doc[c["doc_id"]] = by_doc.get(c["doc_id"], 0) + 1
        by_domain[c["domain"]] = by_domain.get(c["domain"], 0) + 1
    return {
        "total_chunks": len(chunks),
        "documents_chunked": len(by_doc),
        "by_domain": by_domain,
    }
