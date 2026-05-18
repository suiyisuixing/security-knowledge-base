# Reviewer Quick Path (v5.0)

A 12-step walkthrough that exercises every major capability without any
external network call.

1. Load knowledge domains — `GET /knowledge/domains`.
2. Search for a security concept — `POST /knowledge/search`.
3. Ask a knowledge-grounded question — `POST /knowledge/ask`.
4. Classify an *allowed* request — `POST /safety/classify` with
   `"Explain what BOLA is."`.
5. Classify a *needs-confirmation* request — `POST /safety/classify` with
   `"Help me check this domain for issues."`.
6. Classify a *blocked* request — `POST /safety/classify` with
   `"Scan this public IP for vulnerabilities."`.
7. Generate a learning path — `POST /learning-path/generate`.
8. Build an authorized workflow plan — `POST /workflow/authorized-plan`.
9. Route a task to A/B/C/D — `POST /router/route-task`.
10. Run benchmark — `POST /benchmark/run`.
11. Generate agent readiness report — `POST /report/agent-readiness`.
12. Review portfolio value summary — `GET /demo/portfolio-summary`.

Every sample output is also bundled under `sample_outputs/` so the path can
be reviewed without starting the backend.
