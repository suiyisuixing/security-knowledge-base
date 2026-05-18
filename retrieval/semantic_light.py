"""Light-weight semantic-style expansion (v4.5).

No embeddings, no vector store. A bundled security-term synonym map plus
domain-name normalisation give a deterministic semantic-style boost.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from typing import Any

from app import config


_SYNONYM_FALLBACK = {
    "idor": ["bola", "broken object level authorization"],
    "bola": ["idor", "broken object level authorization"],
    "broken object level authorization": ["bola", "idor"],
    "prompt injection": ["instruction override", "jailbreak", "indirect injection"],
    "instruction override": ["prompt injection"],
    "rag security": ["retrieval security", "rag access control"],
    "retrieval security": ["rag security"],
    "mitre": ["attack technique", "att&ck"],
    "attack technique": ["mitre"],
    "cve": ["vulnerability identifier"],
    "cvss": ["severity score"],
    "epss": ["exploitation probability"],
    "kev": ["known exploited vulnerability"],
    "secrets": ["credentials", "api key"],
    "credentials": ["secrets"],
    "authz": ["authorization"],
    "authn": ["authentication"],
    "safe verification": ["authorized validation"],
    "defensive review": ["security assessment"],
}


@lru_cache(maxsize=1)
def _load_synonyms() -> dict[str, list[str]]:
    path = config.DATA_DIR / "security_synonyms.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return {k.lower(): [s.lower() for s in v] for k, v in (data.get("map") or {}).items()}
        except json.JSONDecodeError:
            pass
    return dict(_SYNONYM_FALLBACK)


def normalize_security_terms(text: str) -> str:
    t = (text or "").lower()
    t = re.sub(r"att&ck", "mitre", t)
    t = re.sub(r"\bauthz\b", "authorization", t)
    t = re.sub(r"\bauthn\b", "authentication", t)
    return t


def map_synonyms(query: str) -> list[str]:
    norm = normalize_security_terms(query)
    syn = _load_synonyms()
    expansions: list[str] = []
    for key, values in syn.items():
        if key in norm:
            expansions.extend(values)
    return expansions


def expand_security_query(query: str) -> str:
    base = normalize_security_terms(query)
    expansions = map_synonyms(query)
    if not expansions:
        return base
    return base + " " + " ".join(expansions)


def concept_overlap_score(query: str, chunk: dict[str, Any]) -> float:
    expanded = expand_security_query(query)
    chunk_text = (chunk.get("text") or "").lower()
    score = 0.0
    for token in set(expanded.split()):
        if len(token) > 2 and token in chunk_text:
            score += 1.0
    return score / max(1.0, len(set(expanded.split())))


def related_skill_score(query: str, chunk: dict[str, Any]) -> float:
    q = (query or "").lower()
    tags = [str(t).lower() for t in chunk.get("tags", []) or []]
    score = 0.0
    for t in tags:
        if any(token in q for token in t.split()):
            score += 0.5
    return score
