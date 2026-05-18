import os

from app import audit


def test_log_event_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr(audit.config, "LOGS_DIR", tmp_path)
    event = audit.log_event("test", {"foo": "bar"})
    assert event["type"] == "test"
    assert (tmp_path / audit.AUDIT_FILE).exists()


def test_log_event_redacts_authorization(tmp_path, monkeypatch):
    monkeypatch.setattr(audit.config, "LOGS_DIR", tmp_path)
    event = audit.log_event("test", {"headers": "Authorization: Bearer abc.def.ghi"})
    assert "[REDACTED]" in event["details"]["headers"]


def test_log_event_redacts_password(tmp_path, monkeypatch):
    monkeypatch.setattr(audit.config, "LOGS_DIR", tmp_path)
    event = audit.log_event("test", {"body": "password=hunter2"})
    assert "[REDACTED]" in event["details"]["body"]


def test_log_event_redacts_token(tmp_path, monkeypatch):
    monkeypatch.setattr(audit.config, "LOGS_DIR", tmp_path)
    event = audit.log_event("test", {"body": "token=abcdef"})
    assert "[REDACTED]" in event["details"]["body"]


def test_log_event_redacts_api_key_pattern(tmp_path, monkeypatch):
    monkeypatch.setattr(audit.config, "LOGS_DIR", tmp_path)
    event = audit.log_event("test", {"body": "sk-ABCDEFGHIJKL"})
    assert "[REDACTED" in event["details"]["body"]


def test_audit_allowed_decision(tmp_path, monkeypatch):
    monkeypatch.setattr(audit.config, "LOGS_DIR", tmp_path)
    e = audit.audit_allowed_decision("Explain BOLA.", {"classification": "allowed_learning"})
    assert e["type"] == "allowed_decision"


def test_audit_blocked_decision(tmp_path, monkeypatch):
    monkeypatch.setattr(audit.config, "LOGS_DIR", tmp_path)
    e = audit.audit_blocked_decision("nmap target", {"classification": "blocked_unauthorized_public_scan"})
    assert e["type"] == "blocked_decision"


def test_read_recent_events(tmp_path, monkeypatch):
    monkeypatch.setattr(audit.config, "LOGS_DIR", tmp_path)
    audit.log_event("a", {"x": 1})
    audit.log_event("b", {"x": 2})
    events = audit.read_recent_events(limit=5)
    assert len(events) >= 2


def test_read_recent_events_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(audit.config, "LOGS_DIR", tmp_path)
    assert audit.read_recent_events() == []


def test_sanitize_event_recursive():
    sanitized = audit.sanitize_event({"nested": {"password=foo": "x", "field": "Bearer abc"}})
    assert "[REDACTED]" in sanitized["nested"]["field"] or "Bearer [REDACTED]" in sanitized["nested"]["field"]
