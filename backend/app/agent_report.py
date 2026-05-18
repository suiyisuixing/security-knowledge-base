"""Agent-level reports (coverage, safety, skill mapping, benchmark, readiness)."""

from __future__ import annotations

import json
from typing import Any

from . import benchmark_builder
from . import knowledge_loader
from . import project_registry
from . import reporting
from . import safety_policy
from . import skill_mapper


def build_knowledge_coverage_report() -> dict[str, Any]:
    summary = knowledge_loader.summarize_knowledge_base()
    sections = [
        {"heading": "Total documents", "body": str(summary["total_documents"])},
        {"heading": "Domains", "body": ", ".join(summary["domains"])},
        {"heading": "Documents per domain", "body": json.dumps(summary["documents_per_domain"], indent=2)},
        {"heading": "Development note", "body": reporting.AI_DISCLOSURE_EN},
    ]
    return {"title": "Knowledge Coverage Report", "sections": sections}


def build_safety_policy_report() -> dict[str, Any]:
    return reporting.build_safety_policy_report()


def build_skill_mapping_report() -> dict[str, Any]:
    skills = skill_mapper.list_skills()
    projects = project_registry.list_projects()
    mapping = {p["project_id"]: p["skills"] for p in projects}
    sections = [
        {"heading": "Skill count", "body": str(len(skills))},
        {"heading": "Skill IDs", "body": ", ".join(s["skill_id"] for s in skills)},
        {"heading": "Project → skills", "body": json.dumps(mapping, indent=2)},
        {"heading": "Development note", "body": reporting.AI_DISCLOSURE_EN},
    ]
    return {"title": "Skill Mapping Report", "sections": sections}


def build_benchmark_report() -> dict[str, Any]:
    summary = benchmark_builder.summarize_benchmark(benchmark_builder.run_benchmark())
    sections = [
        {"heading": "Benchmark summary", "body": json.dumps(summary, indent=2)},
        {"heading": "Development note", "body": reporting.AI_DISCLOSURE_EN},
    ]
    return {"title": "Benchmark Report", "sections": sections}


def build_agent_readiness_report() -> dict[str, Any]:
    return reporting.build_agent_readiness_report()
