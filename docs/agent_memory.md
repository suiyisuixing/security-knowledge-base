# Agent Memory

## Files

- `memory/user_learning_profile.json` — display name, goals, preferences.
- `memory/skill_progress.json` — per-skill status and notes.
- `memory/completed_labs.json` — labs the user has completed.
- `memory/project_state.json` — portfolio project status snapshot.

## Operations

`memory_store.load_memory_profile` merges the files into a single profile
object. `update_skill_progress` updates a single skill in place; new skills
are appended. `add_completed_lab` is idempotent.

## What is not stored

- No passwords, tokens, API keys, or real targets.
- No third-party private data.
- No request bodies from external systems.
