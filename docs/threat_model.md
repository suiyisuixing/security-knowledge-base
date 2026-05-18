# Threat Model

## Scope

This project is a local, file-based educational service. It exposes a FastAPI
surface on localhost, a React frontend, and no outbound network calls.

## Trust boundaries

- Filesystem: the project trusts files under its own `PROJECT_ROOT`.
  All path resolution is constrained via `config.safe_resolve_*`.
- Client → API: the API is intended for localhost use.
- API → external: there is no external network call from `backend/app/`.

## Assumptions

- The user runs the service in a personal environment.
- No multi-tenant deployment is intended.
- Audit logs may be inspected by the user only.

## Threats and mitigations

- Path traversal in knowledge resolution → blocked by `safe_resolve_*`.
- Sensitive data leakage in audit logs → redacted via `audit.sanitize_event`.
- Untrusted user intent (scan/exploit) → safety policy blocks and redirects.
- Misuse as a planner for unauthorized activity → workflow planner refuses
  without an explicit local/self/authorized scope claim.

## Out of scope

- Production deployment.
- Multi-user authentication.
- Encryption at rest of memory files (they contain no sensitive data).
