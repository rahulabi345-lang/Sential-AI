"""Tests for the Sentinel AI threat intelligence module."""

from ai.analyzer import analyze
from ai.classifier import classify
from ai.models import Recommendation, SecurityEvent, ThreatResult
from ai.risk_scoring import calculate_risk_score, get_risk_level
from ai.explainer import explain
from ai.recommender import recommend
def test_analyze_combines_ai_pipeline():
    event = {
        "id": "event-001",
        "event_type": "failed_login",
        "source": "auth_monitor",
    }

    result = analyze(event)

    assert result["event_id"] == "event-001"
    assert result["classification"] == "suspicious"
    assert result["risk_score"] == 70
    assert "suspicious activity" in result["explanation"]
    assert len(result["recommendations"]) > 0


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
def test_recommend_benign_event():
    recommendations = recommend("benign", 10)

    assert "Continue monitoring the activity." in recommendations


def test_recommend_suspicious_event():
    recommendations = recommend("suspicious", 60)

    assert "Investigate the event and review related security logs." in recommendations
    assert (
        "Check the affected account or system for additional suspicious activity."
        in recommendations
    )


def test_recommend_high_risk_suspicious_event():
    recommendations = recommend("suspicious", 70)

    assert (
        "Consider enabling stronger authentication controls such as MFA."
        in recommendations
    )


def test_recommend_malicious_event():
    recommendations = recommend("malicious", 90)

    assert "Isolate the affected system if possible." in recommendations
    assert "Reset potentially compromised credentials." in recommendations
    assert "Escalate the incident for immediate security response." in recommendations


def test_recommend_unknown_event():
    recommendations = recommend("unknown", 20)

    assert "Collect additional information about the event." in recommendations