"""Report generation (knowledge, safety, agent readiness)."""

from __future__ import annotations

import json
from typing import Any

from . import knowledge_loader
from . import safety_policy
from . import skill_mapper
from . import project_registry
from . import benchmark_builder


AI_DISCLOSURE_EN = (
    "This project was developed as an AI-assisted learning and engineering project. "
    "The architecture, security knowledge model, safety policy design, testing goals, "
    "validation process, and final review were directed by the author. AI tools were used "
    "for planning, documentation support, debugging guidance, and review assistance, while "
    "all repository commits and project decisions were managed by the author."
)


def build_knowledge_report() -> dict[str, Any]:
    summary = knowledge_loader.summarize_knowledge_base()
    sections = [
        {"heading": "Total documents", "body": str(summary["total_documents"])},
        {"heading": "Domains", "body": ", ".join(summary["domains"])},
        {"heading": "Documents per domain", "body": json.dumps(summary["documents_per_domain"], indent=2)},
        {"heading": "Development note", "body": AI_DISCLOSURE_EN},
    ]
    return {"title": "Knowledge Coverage Report", "sections": sections}


def build_safety_policy_report() -> dict[str, Any]:
    policy = safety_policy.load_safety_policy()
    classes = policy.get("classes", {})
    counts = {
        "allowed": sum(1 for v in classes.values() if v.get("allowed") and v.get("description", "").startswith(("Conceptual", "Defensive", "Request applies", "Code", "Generate", "Plan"))),
        "needs_confirmation": sum(1 for k in classes if k.startswith("needs_")),
        "blocked": sum(1 for k in classes if k.startswith("blocked_")),
        "total": len(classes),
    }
    sections = [
        {"heading": "Policy version", "body": policy.get("policy_version", "")},
        {"heading": "Class counts", "body": json.dumps(counts, indent=2)},
        {"heading": "Classes", "body": ", ".join(sorted(classes.keys()))},
        {"heading": "Development note", "body": AI_DISCLOSURE_EN},
    ]
    return {"title": "Safety Policy Report", "sections": sections}


def build_agent_readiness_report() -> dict[str, Any]:
    kb = knowledge_loader.summarize_knowledge_base()
    skills = skill_mapper.list_skills()
    projects = project_registry.list_projects()
    bench = benchmark_builder.summarize_benchmark(benchmark_builder.run_benchmark())
    sections = [
        {"heading": "Knowledge documents", "body": str(kb["total_documents"])},
        {"heading": "Domains", "body": ", ".join(kb["domains"])},
        {"heading": "Skills", "body": str(len(skills))},
        {"heading": "Portfolio projects", "body": ", ".join(p["project_id"] for p in projects)},
        {"heading": "Benchmark summary", "body": json.dumps(bench, indent=2)},
        {"heading": "Development note", "body": AI_DISCLOSURE_EN},
    ]
    return {"title": "Agent Readiness Report", "sections": sections}


def build_markdown_report(report: dict[str, Any]) -> str:
    lines = [f"# {report.get('title', 'Report')}", ""]
    for s in report.get("sections", []):
        lines.append(f"## {s.get('heading', '')}")
        lines.append("")
        lines.append(s.get("body", ""))
        lines.append("")
    return "\n".join(lines)


def build_json_report(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False)
