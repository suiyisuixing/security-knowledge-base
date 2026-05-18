# Testing Strategy

## Coverage

| Area | Files |
|---|---|
| Knowledge loader | test_knowledge_loader.py |
| Metadata parser | test_metadata.py |
| Retrieval | test_retrieval.py |
| Answer builder | test_answer_builder.py |
| Safety policy | test_safety_policy.py |
| Evaluation harness | test_evaluation.py |
| Reporting | test_reporting.py |
| Memory store | test_memory_store.py |
| Skill mapper | test_skill_mapper.py |
| Learning path | test_learning_path.py |
| Project registry | test_project_registry.py |
| Context builder | test_context_builder.py |
| Audit | test_audit.py |
| Knowledge quality | test_knowledge_quality.py |
| Citation evaluator | test_citation_evaluator.py |
| Safety evaluator | test_safety_evaluator.py |
| Vuln reasoning templates | test_vuln_reasoning_templates.py |
| Authorized workflow | test_authorized_workflow.py |
| Task router | test_task_router.py |
| Benchmark builder | test_benchmark_builder.py |
| Agent report | test_agent_report.py |
| API (basic) | test_api.py |
| API (v2) | test_api_v2.py |
| API (v3) | test_api_v3.py |
| Security boundaries | test_security_boundaries.py |

## Hard rules

- All tests must pass.
- No skip, no xfail.
- Test files do not import `requests`, `subprocess`, or `urllib.request`.
- Security-boundary tests assert that the backend imports do not change.

## How to run

```cmd
cd /d C:\Users\27827\Desktop\Event\security-knowledge-base
C:\Users\27827\Desktop\Event\security-knowledge-base\.venv\Scripts\python.exe -m pytest
```
