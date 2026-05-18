"""Template renderer — rule-based output formatting (v4.0)."""

from __future__ import annotations

from typing import Any


SAFETY_FOOTER = (
    "Safety boundary: this output is for local labs, defensive analysis, "
    "and explicitly authorized work. The system does not support unauthorized "
    "scanning or exploitation."
)


def render_grounded_answer_template(query: str, evidence: dict[str, Any]) -> str:
    docs = evidence.get("retrieved_docs", [])
    lines = [f"Answer to: {query.strip()}", "", "Based on local knowledge documents:"]
    if not docs:
        lines.append("- (no documents matched the query)")
    else:
        for d in docs:
            lines.append(f"- [{d['doc_id']}] {d['title']} ({d['domain']})")
    skills = evidence.get("related_skills", [])
    if skills:
        lines.append("")
        lines.append("Related skills: " + ", ".join(skills))
    projects = evidence.get("related_projects", [])
    if projects:
        lines.append("Related projects: " + ", ".join(projects))
    lines.append("")
    lines.append(SAFETY_FOOTER)
    return "\n".join(lines)


def render_safety_explanation_template(query: str, policy_decision: dict[str, Any]) -> str:
    return (
        f"Query: {query}\n"
        f"Classification: {policy_decision.get('classification')}\n"
        f"Allowed: {policy_decision.get('allowed')}\n"
        f"Reason: {policy_decision.get('reason')}\n"
        f"Safe redirect: {policy_decision.get('safe_redirect')}\n"
        f"{SAFETY_FOOTER}"
    )


def render_authorized_workflow_template(workflow: dict[str, Any]) -> str:
    lines = [
        f"Workflow: {workflow.get('workflow_id', '')}",
        f"Allowed: {workflow.get('allowed', False)}",
        f"Required scope: {workflow.get('required_scope', '')}",
        "Steps:",
    ]
    for s in workflow.get("steps", []):
        lines.append(f"  - {s}")
    lines.append("Blocked actions:")
    for s in workflow.get("blocked_actions", []):
        lines.append(f"  - {s}")
    lines.append("")
    lines.append(SAFETY_FOOTER)
    return "\n".join(lines)


def render_task_route_template(route: dict[str, Any]) -> str:
    return (
        f"Task routed to project: {route.get('project_id')}\n"
        f"Knowledge domain: {route.get('knowledge_domain')}\n"
        f"Skill: {route.get('skill_id')}\n"
        f"Explanation: {route.get('explanation')}\n"
        f"{SAFETY_FOOTER}"
    )


def render_portfolio_readiness_template(report: dict[str, Any]) -> str:
    lines = ["Portfolio readiness report:"]
    categories = report.get("categories", {})
    for k, v in categories.items():
        lines.append(f"- {k}: {v}")
    lines.append(f"Overall: {report.get('overall', 0)}")
    lines.append(SAFETY_FOOTER)
    return "\n".join(lines)


def render_skill_gap_template(gaps: list[dict[str, Any]]) -> str:
    lines = ["Skill gap report:"]
    if not gaps:
        lines.append("- No major gaps detected.")
    for g in gaps:
        lines.append(f"- {g.get('skill_id','?')}: {g.get('reason','')}")
    lines.append(SAFETY_FOOTER)
    return "\n".join(lines)
