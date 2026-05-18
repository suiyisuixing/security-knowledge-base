---
id: api-owasp-api-top10-001
title: OWASP API Top 10 Overview
domain: api_security
difficulty: easy
related_projects:
  - vulnerability-intelligence-lab
  - security-knowledge-base
related_skills:
  - api_authorization_reasoning
  - secure_code_review
  - safe_verification_planning
tags:
  - OWASP
  - API
  - Risk Catalog
safe_use:
  - local_lab
  - authorized_testing
  - defensive_learning
forbidden_use:
  - unauthorized_scanning
  - credential_theft
  - exploit_weaponization
---

## Concept

The OWASP API Security Top 10 is a curated list of the most impactful API risks, including broken object level authorization (BOLA), broken authentication, broken object property level authorization (BOPLA), unrestricted resource consumption, broken function level authorization (BFLA), unrestricted access to sensitive business flows, server-side request forgery (SSRF), security misconfiguration, improper inventory management, and unsafe consumption of APIs.

## Why it matters

APIs are now the dominant attack surface for web applications. Authorization bugs in particular are easy to introduce, hard to detect with generic scanners, and severe in impact. A shared vocabulary helps reviewers, developers, and AI agents reason about the same risks.

## Common indicators

- Endpoints that accept object IDs without ownership checks
- Admin functionality exposed under the same path prefix as user functionality
- Endpoints that return unfiltered object fields
- Outbound requests built from user-supplied URLs
- Inconsistent inventory between production and staging

## Safe local example

In a local lab, run a deliberately vulnerable API such as one you build yourself with two users, two objects, and an endpoint that accepts an object ID. Confirm whether user A can read user B's object by changing the ID. Add an ownership check and re-run.

## Defensive verification approach

- Map each Top 10 category to your endpoints
- Add automated tests for authorization across roles
- Maintain an API inventory and review it on every release
- Surface logs that capture authorization decisions

## Remediation guidance

- Centralize authorization checks at a single layer
- Validate input types and shapes at the boundary
- Apply rate limits per principal and per resource
- Treat outbound requests built from user input as SSRF risks

## Safety boundary

This is a defensive reference. It does not include payloads aimed at third-party APIs. Use only in local labs or authorized environments.

## Related project connection

CVE-style intelligence and dependency reasoning live in `vulnerability-intelligence-lab`. This knowledge base provides concepts and policy that the agent uses to reason about API risks.
