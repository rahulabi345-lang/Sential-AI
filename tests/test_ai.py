"""Tests for the Sentinel AI threat intelligence module."""

from ai.analyzer import analyze
from ai.classifier import classify
from ai.models import Recommendation, SecurityEvent, ThreatResult
from ai.risk_scoring import calculate_risk_score, get_risk_level
from ai.explainer import explain


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
    assert recommendation.description == (
        "Turn on multi-factor authentication for this account."
    )
    assert recommendation.severity == "high"


def test_classify_benign_event():
    event = {
        "event_type": "login",
        "source": "test",
    }

    assert classify(event) == "benign"


def test_classify_suspicious_event():
    event = {
        "event_type": "failed_login",
        "source": "test",
    }

    assert classify(event) == "suspicious"


def test_classify_unknown_event():
    event = {}

    assert classify(event) == "unknown"


def test_benign_risk_score():
    assert calculate_risk_score("benign") == 10


def test_suspicious_risk_score():
    assert calculate_risk_score("suspicious") == 60


def test_malicious_risk_score():
    assert calculate_risk_score("malicious") == 90


def test_unknown_risk_score():
    assert calculate_risk_score("unknown") == 20


def test_risk_levels():
    assert get_risk_level(10) == "low"
    assert get_risk_level(50) == "medium"
    assert get_risk_level(90) == "high"


def test_explain_benign_event():
    event = {
        "event_type": "login",
        "source": "auth_monitor",
    }

    explanation = explain(event, "benign", 10)

    assert "normal activity" in explanation
    assert "10/100" in explanation
    assert "low risk" in explanation


def test_explain_suspicious_event():
    event = {
        "event_type": "failed_login",
        "source": "auth_monitor",
    }

    explanation = explain(event, "suspicious", 70)

    assert "suspicious activity" in explanation
    assert "70/100" in explanation
    assert "investigated" in explanation


def test_explain_malicious_event():
    event = {
        "event_type": "ransomware",
        "source": "endpoint_monitor",
    }

    explanation = explain(event, "malicious", 100)

    assert "malicious activity" in explanation
    assert "100/100" in explanation
    assert "immediate investigation" in explanation


def test_explain_unknown_event():
    event = {
        "event_type": "unknown_event",
        "source": "test",
    }

    explanation = explain(event, "unknown", 20)

    assert "could not be confidently classified" in explanation
    assert "20/100" in explanation