# v5.0 — Security Boundaries

This page is the authoritative list of what v5.0 does and does *not* do.

## v5.0 does:

- Local knowledge retrieval over bundled Markdown.
- Hybrid retrieval (chunk + lexical + light semantic + trust + quality).
- Rule-based safety policy classification (20 categories).
- Authorized workflow *planning* (local lab, self-owned asset, authorized
  engagement only). Planning artifacts only — never executes.
- Agent memory tracking via local JSON.
- Task routing across A / B / C / D.
- Cross-project context, skill evidence, portfolio readiness, maturity.
- Citation grounding, faithfulness, source-trust scoring.

## v5.0 does **not**:

- Call any external model-provider API of any kind.
- Call any local LLM connector. No `llm/`, no `model_config.json`.
- Run real port scans (nmap / masscan), web fuzzers (ffuf / gobuster) or
  exploit tools (sqlmap / Hydra) — those strings cannot appear in
  `backend/app`, `reasoning/`, `retrieval/`, or `agent_hub/` (enforced by
  `tests/test_v5_security_boundaries.py`).
- Import `requests`, `urllib.request`, `subprocess` from backend code.
- Use `os.system(` or `shell=True`.
- Read or modify A/B/C project files.

## Future v6.0

v6.0 may introduce an *optional* local-model connector behind a feature
flag (off by default). Until then, v5.x stays fully model-free.

## Public-version boundary statement

The system does not support unauthorized scanning or exploitation. It
supports local labs, self-owned assets, and explicitly authorized
reconnaissance planning, low-risk security check planning, and safe
verification workflows.

本系统不支持未授权扫描或漏洞利用。它支持本地实验、自有资产和明确授权范围内的信息
收集规划、低风险安全检查规划与安全验证流程。
