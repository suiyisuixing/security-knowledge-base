# v6.0 — Future Local Model Integration (Out of Scope for v5.0)

This document captures the *intent* of v6.0 so reviewers know the
direction. **No code in v5.0 connects to a model.**

## Plan

- Add an *optional* local-model connector behind a feature flag.
- Default off in CI, default off in the bundled distribution, default off
  on first launch.
- The connector must be local-first (e.g. an `localhost`-bound process).
- The safety policy and authorized workflow planner remain authoritative —
  the connector cannot bypass them.
- The connector must respect the same forbidden-import rules.

## Constraints

- v5.x must keep passing all existing tests with the connector code
  removed.
- The connector module (if added) must live in a separate package and
  must not be imported by `backend/app`, `reasoning/`, `retrieval/`, or
  `agent_hub/` when the feature flag is off.
- The CI safety-boundary tests must continue to pass; new tests must be
  added to assert the feature flag is off by default.

## Why not now

The current value of the project is determinism, transparency, and the
ability to be reviewed cold. Adding a model would dilute that signal
without adding portfolio value — until it is built carefully behind a
flag.
