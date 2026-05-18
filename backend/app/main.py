"""FastAPI application exposing the Security Knowledge Base & Agent Memory Lab API."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import (
    agent_report,
    answer_builder,
    audit,
    authorized_workflow,
    benchmark_builder,
    citation_evaluator,
    config,
    context_builder,
    evaluation,
    knowledge_loader,
    knowledge_quality,
    learning_path,
    memory_store,
    project_registry,
    reporting,
    retrieval,
    safety_evaluator,
    safety_policy,
    skill_mapper,
    task_router,
    vuln_reasoning_templates,
)
from .schemas import (
    AskRequest,
    AuthorizedWorkflowRequest,
    ContextBuildRequest,
    LearningPathRequest,
    SafetyClassificationRequest,
    SearchRequest,
    SkillUpdateRequest,
    TaskRouteRequest,
)

app = FastAPI(
    title="Security Knowledge Base & Agent Memory Lab",
    version=config.get_project_version(),
    description=(
        "Local cybersecurity knowledge base, retrieval, safety policy, agent memory, "
        "task routing, and benchmark platform for authorized security learning, "
        "defensive analysis, and safe vulnerability discovery reasoning."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


API_SURFACE: list[dict[str, str]] = []


def _route(method: str, path: str, summary: str):
    API_SURFACE.append({"method": method, "path": path, "summary": summary})


@app.get("/")
def root():
    return {
        "name": "Security Knowledge Base & Agent Memory Lab",
        "version": config.get_project_version(),
        "status": "ok",
    }


_route("GET", "/", "Project metadata")


@app.get("/health")
def health():
    return {"status": "ok", "version": config.get_project_version()}


_route("GET", "/health", "Liveness check")


@app.get("/knowledge/domains")
def knowledge_domains():
    summary = knowledge_loader.summarize_knowledge_base()
    return {"domains": summary["domains"], "counts": summary["documents_per_domain"]}


_route("GET", "/knowledge/domains", "List knowledge domains")


@app.get("/knowledge/docs")
def knowledge_docs(domain: str | None = None):
    docs = knowledge_loader.get_index()["documents"]
    if domain:
        docs = [d for d in docs if d["metadata"].get("domain") == domain]
    return {"count": len(docs), "documents": [
        {"doc_id": d["metadata"]["id"], "title": d["metadata"]["title"], "domain": d["metadata"]["domain"]}
        for d in docs
    ]}


_route("GET", "/knowledge/docs", "List knowledge documents")


@app.get("/knowledge/docs/{doc_id}")
def knowledge_doc(doc_id: str):
    doc = knowledge_loader.get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="document not found")
    return doc


_route("GET", "/knowledge/docs/{doc_id}", "Get a knowledge document")


@app.post("/knowledge/search")
def knowledge_search(req: SearchRequest):
    return {"results": retrieval.search_knowledge(req.query, req.domain, req.top_k)}


_route("POST", "/knowledge/search", "Search knowledge base")


@app.post("/knowledge/ask")
def knowledge_ask(req: AskRequest):
    results = retrieval.search_knowledge(req.query, req.domain, req.top_k)
    answer = answer_builder.build_grounded_answer(req.query, results)
    classification = safety_policy.classify_request(req.query)
    if classification["allowed"]:
        audit.audit_allowed_decision(req.query, classification)
    else:
        audit.audit_blocked_decision(req.query, classification)
    return answer


_route("POST", "/knowledge/ask", "Grounded answer for a query")


@app.post("/safety/classify")
def safety_classify(req: SafetyClassificationRequest):
    cls = safety_policy.classify_request(req.text)
    cls["explanation"] = safety_policy.explain_policy_decision(req.text, cls)
    if cls["allowed"]:
        audit.audit_allowed_decision(req.text, cls)
    else:
        audit.audit_blocked_decision(req.text, cls)
    return cls


_route("POST", "/safety/classify", "Classify a request against safety policy")


@app.get("/safety/policy")
def safety_policy_view():
    return safety_policy.load_safety_policy()


_route("GET", "/safety/policy", "Return loaded safety policy")


@app.get("/safety/evaluation")
def safety_evaluation_get():
    results = safety_evaluator.evaluate_safety_policy()
    return {"results": results, "summary": safety_evaluator.summarize_safety_evaluation(results)}


_route("GET", "/safety/evaluation", "Run safety policy evaluation")


@app.post("/safety/evaluate")
def safety_evaluation_post():
    results = safety_evaluator.evaluate_safety_policy()
    return {"results": results, "summary": safety_evaluator.summarize_safety_evaluation(results)}


_route("POST", "/safety/evaluate", "Run safety policy evaluation")


@app.get("/memory/profile")
def memory_profile():
    return memory_store.load_memory_profile()


_route("GET", "/memory/profile", "Load agent memory profile")


@app.post("/memory/update-skill")
def memory_update_skill(req: SkillUpdateRequest):
    skills = memory_store.update_skill_progress(req.skill_id, req.status, req.notes)
    return {"skills": skills}


_route("POST", "/memory/update-skill", "Update skill progress in memory")


@app.get("/memory/skill-progress")
def memory_skill_progress():
    return {"skills": memory_store.get_skill_progress()}


_route("GET", "/memory/skill-progress", "List skill progress entries")


@app.get("/memory/audit")
def memory_audit(limit: int = 20):
    return {"events": audit.read_recent_events(limit)}


_route("GET", "/memory/audit", "Read recent audit events")


@app.get("/projects")
def projects_list():
    return {"projects": project_registry.list_projects()}


_route("GET", "/projects", "List portfolio projects")


@app.get("/projects/{project_id}")
def projects_get(project_id: str):
    p = project_registry.get_project(project_id)
    if not p:
        raise HTTPException(status_code=404, detail="project not found")
    return p


_route("GET", "/projects/{project_id}", "Get a portfolio project")


@app.get("/skills")
def skills_list():
    return {"skills": skill_mapper.list_skills()}


_route("GET", "/skills", "List skills")


@app.get("/skills/{skill_id}")
def skills_get(skill_id: str):
    s = skill_mapper.get_skill(skill_id)
    if not s:
        raise HTTPException(status_code=404, detail="skill not found")
    return s


_route("GET", "/skills/{skill_id}", "Get a skill")


@app.post("/skills/recommend")
def skills_recommend(payload: dict):
    goal = payload.get("goal", "")
    return {"recommended_skills": skill_mapper.recommend_skills_for_goal(goal)}


_route("POST", "/skills/recommend", "Recommend skills for a goal")


@app.post("/learning-path/generate")
def learning_path_generate(req: LearningPathRequest):
    return learning_path.generate_learning_path(req.goal, req.current_skills)


_route("POST", "/learning-path/generate", "Generate learning path")


@app.post("/context/build")
def context_build(req: ContextBuildRequest):
    return context_builder.build_context_for_query(req.query, req.top_k)


_route("POST", "/context/build", "Build agent context for a query")


@app.get("/quality/knowledge")
def quality_knowledge():
    results = knowledge_quality.score_all_documents()
    return {"results": results, "summary": knowledge_quality.summarize_quality_scores(results)}


_route("GET", "/quality/knowledge", "Score all knowledge documents")


@app.get("/quality/knowledge/{doc_id}")
def quality_knowledge_doc(doc_id: str):
    doc = knowledge_loader.get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="document not found")
    return knowledge_quality.score_document_quality(doc)


_route("GET", "/quality/knowledge/{doc_id}", "Score a knowledge document")


@app.post("/quality/citations/evaluate")
def quality_citations_evaluate(payload: dict):
    return citation_evaluator.evaluate_answer_citations(payload)


_route("POST", "/quality/citations/evaluate", "Evaluate citation quality of an answer")


@app.get("/reasoning/templates")
def reasoning_templates_list():
    return {"templates": vuln_reasoning_templates.list_templates()}


_route("GET", "/reasoning/templates", "List vulnerability reasoning templates")


@app.get("/reasoning/templates/{template_id}")
def reasoning_template_get(template_id: str):
    t = vuln_reasoning_templates.get_template(template_id)
    if not t:
        raise HTTPException(status_code=404, detail="template not found")
    return t


_route("GET", "/reasoning/templates/{template_id}", "Get a reasoning template")


@app.post("/workflow/authorized-plan")
def workflow_authorized_plan(req: AuthorizedWorkflowRequest):
    return authorized_workflow.build_authorized_workflow(req.model_dump())


_route("POST", "/workflow/authorized-plan", "Plan an authorized workflow")


@app.post("/router/route-task")
def router_route_task(req: TaskRouteRequest):
    return task_router.route_task(req.query)


_route("POST", "/router/route-task", "Route a task to a portfolio project")


@app.get("/benchmark/tasks")
def benchmark_tasks():
    return {"tasks": benchmark_builder.load_benchmark_tasks()}


_route("GET", "/benchmark/tasks", "List benchmark tasks")


@app.post("/benchmark/run")
def benchmark_run():
    results = benchmark_builder.run_benchmark()
    return {"results": results, "summary": benchmark_builder.summarize_benchmark(results)}


_route("POST", "/benchmark/run", "Run all benchmark tasks")


@app.get("/benchmark/export-jsonl")
def benchmark_export_jsonl():
    return {"jsonl": benchmark_builder.export_benchmark_jsonl()}


_route("GET", "/benchmark/export-jsonl", "Export benchmark tasks as JSONL string")


@app.post("/report/knowledge-coverage")
def report_knowledge_coverage():
    report = agent_report.build_knowledge_coverage_report()
    report["markdown"] = reporting.build_markdown_report(report)
    return report


_route("POST", "/report/knowledge-coverage", "Generate knowledge coverage report")


@app.post("/report/safety-policy")
def report_safety_policy():
    report = agent_report.build_safety_policy_report()
    report["markdown"] = reporting.build_markdown_report(report)
    return report


_route("POST", "/report/safety-policy", "Generate safety policy report")


@app.post("/report/agent-readiness")
def report_agent_readiness():
    report = agent_report.build_agent_readiness_report()
    report["markdown"] = reporting.build_markdown_report(report)
    return report


_route("POST", "/report/agent-readiness", "Generate agent readiness report")


@app.get("/evaluation/scenarios")
def evaluation_scenarios():
    return evaluation.load_evaluation_scenarios()


_route("GET", "/evaluation/scenarios", "List evaluation scenarios")


@app.post("/evaluation/run")
def evaluation_run():
    results = evaluation.run_all_scenarios()
    return {"results": results, "summary": evaluation.summarize_evaluation(results)}


_route("POST", "/evaluation/run", "Run all evaluation scenarios")


@app.get("/api/surface")
def api_surface():
    return {"endpoints": API_SURFACE}


_route("GET", "/api/surface", "Inventory of API endpoints")
