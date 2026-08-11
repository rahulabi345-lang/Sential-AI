"""Tests for the Sentinel AI threat intelligence module."""

from ai.analyzer import analyze
from ai.classifier import classify
from ai.models import Recommendation, SecurityEvent, ThreatResult


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
        event_type="login_attempt",
        source="auth_monitor",
        timestamp="2026-01-01T00:00:00Z",
    )
    assert event.id == "1"
    assert event.event_type == "login_attempt"
    assert event.source == "auth_monitor"
    assert event.timestamp == "2026-01-01T00:00:00Z"


def test_threat_result_dataclass():
    result = ThreatResult(
        event_id="1",
        classification="suspicious_login",
        risk_score=72.5,
        explanation="Multiple failed login attempts detected.",
    )
    assert result.event_id == "1"
    assert result.classification == "suspicious_login"
    assert result.risk_score == 72.5
    assert result.explanation == "Multiple failed login attempts detected."


def test_recommendation_dataclass():
    recommendation = Recommendation(
        title="Enable MFA",
        description="Turn on multi-factor authentication for this account.",
        severity="high",
    )
    assert recommendation.title == "Enable MFA"
    assert recommendation.description == "Turn on multi-factor authentication for this account."
    assert recommendation.severity == "high"
