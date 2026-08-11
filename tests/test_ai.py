"""Tests for the Sentinel AI threat intelligence module."""

from ai.analyzer import analyze
from ai.classifier import classify
from ai.models import SecurityEvent


def test_analyze_returns_placeholder():
    event = {"id": "test-001", "source": "test"}
    result = analyze(event)
    assert result["status"] == "not_implemented"
    assert result["event_id"] == "test-001"


def test_classify_returns_unknown():
    assert classify({}) == "unknown"


def test_security_event_dataclass():
    event = SecurityEvent(
        id="1", 
        event_type="test",
        source="test",
        timestamp="2026-01-01T00:00:00Z"
         )
    assert event.id == "1"
