"""Rule-based risk scoring (v4.0).

Risk levels: informational / low / medium / high / blocked.
Scoring is deterministic and keyword/structure-based — no model.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from app import config
from app import safety_policy


_HIGH_RISK_TERMS = (
    "exploit", "weaponize", "exfiltrate", "ransomware", "backdoor",
    "evade", "credential", "shell payload", "keylogger",
)

_MEDIUM_RISK_TERMS = (
    "scan", "recon", "test login", "fuzz", "stress test",
)

_LOW_RISK_TERMS = (
    "code review", "configuration review", "header review",
    "verify", "explain", "describe",
)


@lru_cache(maxsize=1)
def _scoring_rules() -> dict[str, Any]:
    path = config.DATA_DIR / "risk_scoring_rules.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _lower(text: str) -> str:
    return (text or "").lower()


def score_request_risk(query: str) -> dict[str, Any]:
    cls = safety_policy.classify_request(query)
    if not cls["allowed"] and cls["classification"].startswith("blocked_"):
        return {"level": "blocked", "score": 1.0, "reasons": [cls["classification"]]}
    q = _lower(query)
    reasons: list[str] = []
    if any(t in q for t in _HIGH_RISK_TERMS):
        reasons.extend(t for t in _HIGH_RISK_TERMS if t in q)
        return {"level": "high", "score": 0.8, "reasons": reasons}
    if any(t in q for t in _MEDIUM_RISK_TERMS):
        reasons.extend(t for t in _MEDIUM_RISK_TERMS if t in q)
        return {"level": "medium", "score": 0.5, "reasons": reasons}
    if any(t in q for t in _LOW_RISK_TERMS):
        reasons.extend(t for t in _LOW_RISK_TERMS if t in q)
        return {"level": "low", "score": 0.2, "reasons": reasons}
    return {"level": "informational", "score": 0.05, "reasons": ["no risk keywords"]}


def score_workflow_risk(workflow: dict[str, Any]) -> dict[str, Any]:
    if not workflow.get("allowed", False):
        return {"level": "blocked", "score": 1.0, "reasons": ["workflow not allowed"]}
    scope = workflow.get("required_scope", "")
    if scope == "local_lab":
        return {"level": "low", "score": 0.1, "reasons": ["local lab scope"]}
    if scope in ("self_owned_asset", "authorized_engagement"):
        return {"level": "medium", "score": 0.4, "reasons": [f"{scope} scope"]}
    return {"level": "informational", "score": 0.05, "reasons": ["planning artifact only"]}


def score_content_risk(text: str) -> dict[str, Any]:
    return score_request_risk(text)


def explain_risk_score(score: dict[str, Any]) -> str:
    return f"level={score.get('level')} score={score.get('score')} reasons={score.get('reasons')}"


def build_risk_breakdown(query: str) -> dict[str, Any]:
    base = score_request_risk(query)
    return {
        "query": query,
        "overall": base,
        "explanation": explain_risk_score(base),
    }
