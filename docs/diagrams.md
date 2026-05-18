# Diagrams

## Knowledge ask flow

```
client ──▶ POST /knowledge/ask
            │
            ▼
     safety_policy.classify_request
            │
            ▼
        audit.log_event
            │
            ▼
   retrieval.search_knowledge
            │
            ▼
 answer_builder.build_grounded_answer
            │
            ▼
       JSON response (answer + citations + safety_note)
```

## Authorized workflow plan flow

```
client ──▶ POST /workflow/authorized-plan
            │
            ▼
   authorized_workflow.validate_scope
            │
       ┌────┴────┐
   in scope?     │
       │         ▼
       ▼     blocked plan + redirect
   allowed plan
```

## Router

```
client ──▶ POST /router/route-task
            │
            ▼
   task_router.route_task
            │
            ▼
  {project_id, knowledge_domain, skill_id}
```
