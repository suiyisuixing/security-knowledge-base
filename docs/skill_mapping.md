# Skill Mapping

The skill taxonomy in `data/skill_taxonomy.json` lists 16 skills. Each skill
has a `skill_id`, `name`, `domain`, `description`, and `related_projects`.

## Mapping

- `map_query_to_skills(query)` — keyword rules map text to candidate skills.
- `map_document_to_skills(doc)` — reads `related_skills` from front matter.
- `map_project_to_skills(project_id)` — reads skills from project registry.
- `recommend_skills_for_goal(goal)` — keyword rules for goal-style strings.

## Cross-project map

| Project | Primary skills |
|---|---|
| llm-security-lab | prompt_injection_reasoning, rag_access_control, secure_retrieval_design |
| security-log-ai-assistant | log_analysis, mitre_mapping, alert_triage, detection_engineering |
| vulnerability-intelligence-lab | vulnerability_prioritization, api_authorization_reasoning, secure_code_review, configuration_review, dependency_risk_reasoning, safe_verification_planning |
| security-knowledge-base | safety_boundary_classification, authorized_recon_planning, task_routing |
