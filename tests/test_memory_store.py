import json

from app import config, memory_store


def _backup(filename):
    path = config.MEMORY_DIR / filename
    return path.read_text(encoding="utf-8") if path.exists() else None


def _restore(filename, content):
    path = config.MEMORY_DIR / filename
    if content is not None:
        path.write_text(content, encoding="utf-8")


def test_load_profile_shape():
    profile = memory_store.load_memory_profile()
    assert "profile_id" in profile
    assert "skill_progress" in profile
    assert "completed_labs" in profile


def test_get_skill_progress_returns_list():
    progress = memory_store.get_skill_progress()
    assert isinstance(progress, list)
    assert progress


def test_update_skill_progress_existing():
    backup = _backup(memory_store.SKILL_PROGRESS_FILE)
    try:
        skills = memory_store.update_skill_progress("prompt_injection_reasoning", "completed", "done")
        found = [s for s in skills if s["skill_id"] == "prompt_injection_reasoning"]
        assert found
        assert found[0]["status"] == "completed"
        assert found[0]["notes"] == "done"
    finally:
        _restore(memory_store.SKILL_PROGRESS_FILE, backup)


def test_update_skill_progress_adds_new():
    backup = _backup(memory_store.SKILL_PROGRESS_FILE)
    try:
        skills = memory_store.update_skill_progress("brand_new_skill_x", "planned", "note")
        found = [s for s in skills if s["skill_id"] == "brand_new_skill_x"]
        assert found
    finally:
        _restore(memory_store.SKILL_PROGRESS_FILE, backup)


def test_add_completed_lab_appends():
    backup = _backup(memory_store.COMPLETED_LABS_FILE)
    try:
        labs = memory_store.add_completed_lab("test-lab-x", "llm-security-lab")
        ids = [l["lab_id"] for l in labs]
        assert "test-lab-x" in ids
    finally:
        _restore(memory_store.COMPLETED_LABS_FILE, backup)


def test_add_completed_lab_idempotent():
    backup = _backup(memory_store.COMPLETED_LABS_FILE)
    try:
        before = len(memory_store.add_completed_lab("test-lab-y", "llm-security-lab"))
        after = len(memory_store.add_completed_lab("test-lab-y", "llm-security-lab"))
        assert before == after
    finally:
        _restore(memory_store.COMPLETED_LABS_FILE, backup)


def test_recommend_next_skills_returns_planned():
    backup = _backup(memory_store.SKILL_PROGRESS_FILE)
    try:
        recs = memory_store.recommend_next_skills()
        assert isinstance(recs, list)
    finally:
        _restore(memory_store.SKILL_PROGRESS_FILE, backup)


def test_summarize_memory_shape():
    summary = memory_store.summarize_memory()
    assert "skill_count" in summary
    assert "by_status" in summary
    assert "completed_lab_count" in summary


def test_no_sensitive_storage_in_profile():
    profile = memory_store.load_memory_profile()
    blob = json.dumps(profile)
    for bad in ("password", "secret", "api_key", "token"):
        assert bad not in blob.lower() or bad == "secrets_management"


def test_save_memory_profile_roundtrip():
    backup = _backup(memory_store.PROFILE_FILE)
    try:
        original = memory_store.load_memory_profile()
        copy = dict(original)
        copy["goals"] = list(copy["goals"]) + ["temp-goal"]
        memory_store.save_memory_profile(copy)
        reloaded = memory_store.load_memory_profile()
        assert "temp-goal" in reloaded["goals"]
    finally:
        _restore(memory_store.PROFILE_FILE, backup)


def test_load_profile_contains_default_id():
    profile = memory_store.load_memory_profile()
    assert profile["profile_id"]


def test_skill_progress_entries_have_status():
    progress = memory_store.get_skill_progress()
    for s in progress:
        assert "status" in s
