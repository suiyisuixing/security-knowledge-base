"""Hybrid retrieval service — API-facing wrapper (v4.5)."""

from __future__ import annotations

from typing import Any

from retrieval import (
    hybrid,
    chunker,
    citation_grounding,
    faithfulness,
    source_trust,
    knowledge_conflict,
    retrieval_eval,
)

from . import knowledge_loader
from . import safety_policy
from . import retrieval as legacy_retrieval


def search_hybrid_knowledge(query: str, domain: str | None = None, top_k: int = 8) -> list[dict[str, Any]]:
    return hybrid.hybrid_search(query, domain=domain, top_k=top_k)


def build_hybrid_grounded_answer(query: str) -> dict[str, Any]:
    results = search_hybrid_knowledge(query, top_k=5)
    docs = knowledge_loader.get_index()["documents"]
    domain_filtered: list[dict[str, Any]] = []
    for r in results:
        for d in docs:
            if d["metadata"]["id"] == r["doc_id"]:
                domain_filtered.append({
                    "chunk_id": r["chunk_id"],
                    "doc_id": r["doc_id"],
                    "title": r["title"],
                    "domain": r["domain"],
                    "text": d["body"][:1200],
                })
                break
    lines = [f"Answer to: {query.strip()}", "", "Based on local knowledge chunks:"]
    for r in results:
        lines.append(f"- [{r['doc_id']}] {r['title']} ({r['domain']}) score={r['score']}")
    safety_note = (
        "Safety boundary: this answer is for local labs, defensive analysis, "
        "and explicitly authorized work. The system does not support unauthorized "
        "scanning or exploitation."
    )
    lines.append("")
    lines.append(safety_note)
    answer = "\n".join(lines)
    grounding = citation_grounding.build_grounding_report(answer, domain_filtered)
    faith = faithfulness.build_faithfulness_summary(answer, domain_filtered)
    classification = safety_policy.classify_request(query)
    return {
        "query": query,
        "answer": answer,
        "results": results,
        "grounding": grounding,
        "faithfulness": faith,
        "safety_classification": classification,
        "safety_note": safety_note,
    }


def evaluate_answer_grounding(answer: str, query: str) -> dict[str, Any]:
    results = search_hybrid_knowledge(query, top_k=5)
    docs = knowledge_loader.get_index()["documents"]
    chunks = []
    for r in results:
        for d in docs:
            if d["metadata"]["id"] == r["doc_id"]:
                chunks.append({
                    "chunk_id": r["chunk_id"],
                    "doc_id": r["doc_id"],
                    "title": r["title"],
                    "domain": r["domain"],
                    "text": d["body"][:1200],
                })
                break
    return {
        "grounding": citation_grounding.build_grounding_report(answer, chunks),
        "faithfulness": faithfulness.build_faithfulness_summary(answer, chunks),
    }


def compare_retrieval_modes(query: str) -> dict[str, Any]:
    return hybrid.compare_legacy_and_hybrid(query)


def build_retrieval_quality_report() -> dict[str, Any]:
    return {
        "evaluation": retrieval_eval.build_retrieval_eval_report(),
        "conflicts": knowledge_conflict.build_conflict_report(),
        "source_trust": source_trust.build_source_trust_report(knowledge_loader.get_index()["documents"]),
        "chunk_summary": chunker.summarize_chunks(
            chunker.chunk_all_documents(knowledge_loader.get_index()["documents"])
        ),
    }
