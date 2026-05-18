# Reviewer Guide

A 10-step path that exercises every major capability.

1. `GET /knowledge/domains` — confirm six domains and >=32 documents.
2. `POST /knowledge/search` with `{"query": "prompt injection"}` — expect
   `ai-prompt-injection-001` at the top.
3. `POST /knowledge/ask` with `{"query": "Explain what BOLA is."}` — expect
   citations and a safety note.
4. `POST /safety/classify` with `{"text": "Scan this public IP for
   vulnerabilities."}` — expect `blocked_unauthorized_public_scan`.
5. `GET /skills` and `GET /projects` — confirm 16 skills and four projects.
6. `POST /learning-path/generate` with `{"goal": "detection engineering"}` —
   expect `log_analysis`, `mitre_mapping`, `alert_triage`, `detection_engineering`.
7. `POST /workflow/authorized-plan` with `{"request": "Plan limited
   authorized recon inside my bug bounty scope."}` — expect allowed plan
   with `authorized_engagement` scope.
8. `POST /router/route-task` with `{"query": "Help me triage these SOC
   alerts."}` — expect `security-log-ai-assistant`.
9. `POST /benchmark/run` — expect pass rate >= 0.8.
10. `POST /report/agent-readiness` — expect Markdown report with the
    AI-assisted development disclosure (and no mention of any specific AI
    vendor).

Look for:

- Safety note present in every grounded answer.
- Blocked safety classes return `allowed: false`.
- Workflow planner refuses requests without explicit scope.
- Router does not invent endpoints — it only returns IDs.
