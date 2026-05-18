# Demo Walkthrough

A short narrative for a five-minute review.

1. **Open the dashboard.** Backend status shows online, version v3.0-rc.
2. **Search.** Type `BOLA authorization` and run search. Top result is
   `api-bola-001` from `api_security`.
3. **Ask.** Ask "Explain what BOLA is." The grounded answer includes
   citations and a safety note.
4. **Classify.** Paste "Scan this public IP for vulnerabilities." The
   classifier returns `blocked_unauthorized_public_scan` with a redirect to
   local lab or authorized assessment.
5. **Memory.** The memory panel shows skill progress for the 16 skills.
6. **Learning path.** Set goal to "detection engineering" and generate.
7. **Workflow plan.** Plan limited recon inside a bug bounty scope; the
   planner returns an allowed plan with five steps and a list of blocked
   actions.
8. **Task router.** Route "Help me triage these SOC alerts." — destination is
   `security-log-ai-assistant`.
9. **Benchmark.** Run the benchmark. Summary shows total/passed/pass-rate and
   the per-type breakdown.
10. **Report.** Generate the agent readiness report. The Markdown ends with
    the AI-assisted development disclosure.
