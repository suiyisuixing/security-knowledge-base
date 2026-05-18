"""Uniform API error format (v3.2).

All API errors should serialize via :func:`make_error` so the frontend can
render a consistent shape, including a safe redirect when applicable.
"""

from __future__ import annotations

from typing import Any


VALID_CODES = {
    "not_found",
    "validation_error",
    "blocked_by_policy",
    "needs_confirmation",
    "schema_invalid",
    "integrity_failure",
    "internal_error",
}


def make_error(
    code: str,
    message: str,
    safe_redirect: str = "",
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if code not in VALID_CODES:
        code = "internal_error"
    return {
        "error": True,
        "code": code,
        "message": message,
        "safe_redirect": safe_redirect,
        "details": details or {},
    }


def not_found(resource: str) -> dict[str, Any]:
    return make_error(
        code="not_found",
        message=f"{resource} not found.",
        safe_redirect=f"Try listing available {resource}s.",
    )


def validation_error(field: str, reason: str) -> dict[str, Any]:
    return make_error(
        code="validation_error",
        message=f"Validation failed for '{field}': {reason}",
        safe_redirect="Adjust the request and retry.",
        details={"field": field, "reason": reason},
    )


def blocked_by_policy(classification: str, redirect: str) -> dict[str, Any]:
    return make_error(
        code="blocked_by_policy",
        message=f"Request blocked by safety policy: {classification}",
        safe_redirect=redirect or "Refer to safe boundary policy.",
        details={"classification": classification},
    )
