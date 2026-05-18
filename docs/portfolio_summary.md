# Portfolio Summary

This project is the fourth in a four-project security portfolio.

| # | Project | Focus |
|---|---|---|
| A | llm-security-lab | AI / RAG security evaluation |
| B | security-log-ai-assistant | Detection engineering / SOC workflow |
| C | vulnerability-intelligence-lab | Vulnerability intelligence and skill data |
| D | security-knowledge-base | Knowledge, safety policy, agent memory, routing |

## How D ties them together

- Provides the canonical knowledge documents the other projects reference.
- Provides a single safety policy classifier the other projects can call
  conceptually.
- Provides a router that suggests which project should handle a task.
- Provides the agent memory and learning-path layer.

## What reviewers should take away

- The portfolio prefers transparent, file-based design over heavy dependencies.
- Every feature is exercised by tests.
- Safety boundaries are first-class artifacts, not afterthoughts.
- The AI-assisted development disclosure is included consistently.
