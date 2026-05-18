"""Append-only audit log for agent decisions.

Logs go to logs/agent_audit.jsonl. Sensitive fields are redacted before write.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from . import config

AUDIT_FILE = "agent_audit.jsonl"

_SENSITIVE_PATTERNS = [
    (re.compile(r"(?i)(authorization\s*[:=]\s*)\S+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(token\s*[:=]\s*)\S+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(password\s*[:=]\s*)\S+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(api[_-]?key\s*[:=]\s*)\S+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]+"), "Bearer [REDACTED]"),
    (re.compile(r"(?i)sk-[A-Za-z0-9]{8,}"), "[REDACTED_API_KEY]"),
]


def _audit_path():
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    return config.LOGS_DIR / AUDIT_FILE


def _redact(value: str) -> str:
    out = value
    for pat, repl in _SENSITIVE_PATTERNS:
        out = pat.sub(repl, out)
    return out


def sanitize_event(details: dict[str, Any]) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}
    for k, v in (details or {}).items():
        if isinstance(v, str):
            cleaned[k] = _redact(v)
        elif isinstance(v, dict):
            cleaned[k] = sanitize_event(v)
        elif isinstance(v, list):
            cleaned[k] = [_redact(x) if isinstance(x, str) else x for x in v]
        else:
            cleaned[k] = v
    return cleaned


def log_event(event_type: str, details: dict[str, Any]) -> dict[str, Any]:
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "details": sanitize_event(details),
    }
    with _audit_path().open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def audit_allowed_decision(query: str, classification: dict[str, Any]) -> dict[str, Any]:
    return log_event("allowed_decision", {"query": query, "classification": classification})


def audit_blocked_decision(query: str, classification: dict[str, Any]) -> dict[str, Any]:
    return log_event("blocked_decision", {"query": query, "classification": classification})


def read_recent_events(limit: int = 20) -> list[dict[str, Any]]:
    path = _audit_path()
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[dict[str, Any]] = []
    for line in lines[-max(1, limit):]:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out
