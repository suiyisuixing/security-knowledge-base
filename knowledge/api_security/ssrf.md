---
id: api-ssrf-001
title: Server-Side Request Forgery (SSRF) Risk Reasoning
domain: api_security
difficulty: hard
related_projects:
  - vulnerability-intelligence-lab
  - security-knowledge-base
related_skills:
  - api_authorization_reasoning
  - secure_code_review
  - configuration_review
tags:
  - OWASP API
  - SSRF
  - Network Security
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

Server-Side Request Forgery (SSRF) is when an application makes outbound requests on behalf of a user, and the user can influence the destination. Because the request originates from the server, it may reach internal services that are not exposed to the public network.

## Why it matters

In cloud environments, SSRF has historically been the path to metadata services, credential theft, and lateral movement. Even without cloud metadata, SSRF can be used to map internal networks or trigger internal admin endpoints.

## Common indicators

- Endpoints that accept URLs or hostnames from clients
- Image proxies, webhook fetchers, link previewers without allow-lists
- HTTP clients without explicit network policy
- Logs showing outbound requests to private address ranges

## Safe local example

Inside a local lab, run a small HTTP fetcher endpoint and call it with localhost URLs. Observe whether internal services respond. Implement an allow-list of permitted destinations and reject everything else. Confirm internal calls now fail safely.

## Defensive verification approach

- Maintain an allow-list of permitted outbound destinations
- Reject responses from disallowed address ranges
- Require explicit network policy at the HTTP-client layer
- Monitor for outbound requests to internal ranges

## Remediation guidance

- Resolve and validate hostnames before connecting
- Disable redirects or restrict their targets
- Run fetchers in a constrained network namespace
- Apply egress firewalls where possible

## Safety boundary

This is defensive analysis only. It does not include payloads aimed at production cloud metadata or third-party services. Practice in local labs that you own.

## Related project connection

CVE catalog and reasoning exercises live in `vulnerability-intelligence-lab`. This knowledge base supplies the concept and template.
