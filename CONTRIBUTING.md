# Contributing

This is a portfolio project. External contributions are not solicited, but the
following rules apply to any local changes the author makes.

## Hard constraints

- No real secrets, tokens, or API keys committed to the repo.
- No real third-party target data, hostnames, IPs, or sample telemetry.
- No unauthorized scanning content (commands, payloads).
- No exploit weaponization (working RCE chains, shell payloads).
- No credential attacks (brute-force scripts, stuffing).
- No persistence, evasion, exfiltration, or malware content.

## Testing rules

- Any change to knowledge, safety policy, retrieval, router, or workflow
  planning must come with tests.
- New blocked safety classes must include at least one positive (blocked)
  test case.
- New benchmark tasks must include a deterministic expected output.

## Commit hygiene

- All commits are managed by the author.
- Commit messages do not name AI tools.
- No `Co-authored-by` trailer.

## Local validation

```cmd
cd /d C:\Users\27827\Desktop\Event\security-knowledge-base
C:\Users\27827\Desktop\Event\security-knowledge-base\.venv\Scripts\python.exe tools\run_checks.py
```
