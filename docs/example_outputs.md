# Example Outputs

Bundled in `sample_outputs/`. These are deterministic JSON snapshots; they
are not generated at request time. They show the shape of each API surface.

| Group | Files |
|---|---|
| `api_responses/` | knowledge_search_bola, grounded_answer_prompt_injection, safety_allowed_learning, safety_needs_confirmation, safety_blocked_public_scan, learning_path_ai_security |
| `authorized_workflows/` | local_lab_workflow, blocked_public_scan_workflow |
| `router_examples/` | route_rag_to_A, route_logs_to_B, route_cve_to_C, route_safety_to_D |
| `benchmark/` | benchmark_summary |
| `reports/` | knowledge_coverage_report, safety_policy_report |
| `agent_readiness/` | agent_readiness_report |

Reviewer Mode in the frontend loads any of these on click. The backend
exposes them at `/demo/sample-outputs` and `/demo/sample-output/{sample_id}`.
