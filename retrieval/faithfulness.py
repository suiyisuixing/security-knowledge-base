"""Faithfulness scoring (v4.5)."""

from __future__ import annotations

import re
from typing import Any

from . import citation_grounding


def split_answer_into_claims(answer: str) -> list[str]:
    sentences = re.split(r"(?<=[\.!?])\s+", answer or "")
    return [s.strip() for s in sentences if len(s.strip()) > 8]


def score_faithfulness(answer: str, chunks: list[dict[str, Any]]) -> float:
    return citation_grounding.estimate_claim_support_score(answer, chunks)


def detect_hallucination_risk(answer: str, chunks: list[dict[str, Any]]) -> dict[str, Any]:
    score = score_faithfulness(answer, chunks)
    if score >= 0.8:
        level = "low"
    elif score >= 0.5:
        level = "medium"
    else:
        level = "high"
    uncited = citation_grounding.detect_uncited_claims(answer, chunks)
    return {
        "score": score,
        "level": level,
        "uncited_count": len(uncited),
        "uncited_samples": uncited[:5],
    }


def build_faithfulness_summary(answer: str, chunks: list[dict[str, Any]]) -> dict[str, Any]:
    claims = split_answer_into_claims(answer)
    return {
        "total_claims": len(claims),
        "faithfulness_score": score_faithfulness(answer, chunks),
        "hallucination_risk": detect_hallucination_risk(answer, chunks),
    }
