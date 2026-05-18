---
id: ai-owasp-llm-top10-001
title: OWASP LLM Top 10 Overview
domain: ai_security
difficulty: easy
related_projects:
  - llm-security-lab
  - security-knowledge-base
related_skills:
  - prompt_injection_reasoning
  - rag_access_control
  - secure_retrieval_design
tags:
  - OWASP
  - LLM
  - AI Security
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

The OWASP LLM Top 10 is a community-maintained catalog of the most critical security risks for applications that integrate large language models. It includes prompt injection, insecure output handling, training-data poisoning, model denial of service, supply-chain risks, sensitive-information disclosure, insecure plugin design, excessive agency, overreliance, and model theft.

## Why it matters

LLM-backed applications now sit between users, internal data sources, and downstream automation. A single insecure pattern (for example, treating model output as trusted code) can expose backend systems, leak private context, or trigger unsafe actions on behalf of the user. The Top 10 gives engineering teams a shared vocabulary for prioritizing defenses.

## Common indicators

- Prompts that mix untrusted content with system instructions
- Tools or plugins that execute model output without validation
- RAG pipelines that retrieve documents without access-control checks
- Logs showing model output flowing directly into shells, SQL, or HTTP requests
- Lack of allow-lists for tool invocation

## Safe local example

In a local lab, build a small RAG application that retrieves from a folder of plain Markdown files. Try to enforce per-user access lists at the retrieval boundary, then observe whether your prompt assembly leaks documents the user is not allowed to see. Repeat the exercise with documents that contain hostile instructions to study indirect prompt injection.

## Defensive verification approach

- Map every category in the Top 10 to your application's components
- Add automated tests for prompt-injection canary strings
- Capture which documents and tools were used in each response
- Review logs to confirm sensitive data is not echoed back

## Remediation guidance

- Separate trusted system prompts from untrusted user or document content
- Validate and constrain model-driven actions through allow-lists
- Apply least-privilege access control at the retrieval layer
- Treat model output as untrusted input for downstream systems

## Safety boundary

This document is a defensive learning reference. It does not provide weaponized prompts or instructions for attacking third-party systems. Use it only inside local labs or systems you are explicitly authorized to test.

## Related project connection

Hands-on labs for these risks live in the `llm-security-lab` project, while this knowledge base supplies the concepts, citations, and safety policy used by the agent layer.
