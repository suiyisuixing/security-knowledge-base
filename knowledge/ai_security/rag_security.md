---
id: ai-rag-security-001
title: RAG Security Fundamentals
domain: ai_security
difficulty: medium
related_projects:
  - llm-security-lab
  - security-knowledge-base
related_skills:
  - rag_access_control
  - secure_retrieval_design
  - prompt_injection_reasoning
tags:
  - RAG
  - Retrieval
  - AI Security
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

Retrieval-augmented generation (RAG) combines a search step with a generation step. Security concerns span both halves: who can see which documents, what content reaches the model, and whether the model treats retrieved text as trusted instructions or as untrusted data.

## Why it matters

A misconfigured RAG layer can leak documents the user is not entitled to, expose sensitive metadata, or carry hostile instructions into the model. Because retrieval happens before generation, access-control failures cannot be fixed by prompt engineering alone.

## Common indicators

- Single shared index across users with different entitlements
- Retrieval scores returned to clients in ways that leak document existence
- No provenance markers on retrieved chunks
- No tests for cross-tenant retrieval leakage

## Safe local example

In a local lab, build a small index with documents tagged for two simulated users. Query as one user and verify that no chunks from the other user appear. Add canary chunks and check whether they leak into unrelated answers.

## Defensive verification approach

- Run cross-tenant retrieval tests as part of CI
- Maintain provenance metadata on every chunk
- Log which chunks contributed to each answer
- Compare responses against an allow-list of expected sources per role

## Remediation guidance

- Enforce access control at retrieval time, not at prompt time
- Keep separate indexes when entitlements differ
- Mark untrusted chunks during prompt assembly
- Surface citations to end users

## Safety boundary

The document is a defensive reference. It does not include techniques for attacking third-party RAG providers. Use ideas only in local labs or authorized systems.

## Related project connection

Hands-on labs are in `llm-security-lab`. The reasoning templates and safety policy used by the agent reference this concept.
