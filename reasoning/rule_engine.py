"""Rule engine — load and apply rule sets (v4.0)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app import config


@lru_cache(maxsize=1)
def load_reasoning_rules() -> dict[str, Any]:
    path: Path = config.DATA_DIR / "reasoning_rules.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _matches_rule(rule: dict[str, Any], query: str) -> bool:
    q = (query or "").lower()
    requires_all = rule.get("all_of") or []
    requires_any = rule.get("any_of") or []
    excludes = rule.get("none_of") or []
    if requires_all and not all(k.lower() in q for k in requires_all):
        return False
    if requires_any and not any(k.lower() in q for k in requires_any):
        return False
    if excludes and any(k.lower() in q for k in excludes):
        return False
    return True


def match_rules(query: str, context: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    rules = load_reasoning_rules().get("rules", [])
    matched: list[dict[str, Any]] = []
    for rule in rules:
        if _matches_rule(rule, query):
            matched.append(dict(rule))
    return matched


def rank_matched_rules(rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    priority_order = {"blocked": 0, "needs_confirmation": 1, "allowed": 2, "informational": 3}

    def key(r: dict[str, Any]) -> tuple[int, int]:
        cat = r.get("category", "informational")
        return (priority_order.get(cat, 4), -int(r.get("priority", 0)))

    return sorted(rules, key=key)


def explain_rule_match(query: str, matched_rules: list[dict[str, Any]]) -> str:
    if not matched_rules:
        return f"No rule matched for query: {query!r}."
    parts = [f"Matched {len(matched_rules)} rule(s) for {query!r}:"]
    for r in matched_rules:
        parts.append(f"- {r.get('rule_id','?')}: {r.get('description','')}")
    return "\n".join(parts)


def apply_rule_set(query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    matched = match_rules(query, context)
    ranked = rank_matched_rules(matched)
    return {
        "query": query,
        "matched_count": len(ranked),
        "ranked_rules": ranked,
        "top_rule": ranked[0] if ranked else None,
        "explanation": explain_rule_match(query, ranked),
    }
