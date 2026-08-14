from data_security.models.risk_assessment import RiskLevel
from data_security.models.security_event import Severity
from data_security.models.threat import Threat, ThreatStatus
from data_security.risk.risk_engine import (
    calculate_risk_level,
    calculate_risk_score,
)


def make_threat(
    severity: Severity,
    confidence: float,
) -> Threat:
    return Threat(
        related_event_ids=["test-event"],
        threat_type="test_threat",
        confidence_score=confidence,
        severity=severity,
        description="Risk engine test threat.",
        status=ThreatStatus.NEW,
    )


def test_no_threats_produce_zero_risk():
    score = calculate_risk_score([])

    assert score == 0.0


def test_high_severity_threat_produces_high_risk():
    threats = [
        make_threat(
            Severity.HIGH,
            1.0,
        )
    ]

    score = calculate_risk_score(threats)

    assert score == 70.0


def test_critical_threat_produces_critical_score():
    threats = [
        make_threat(
            Severity.CRITICAL,
            1.0,
        )
    ]

    score = calculate_risk_score(threats)

    assert score == 100.0


def test_confidence_reduces_risk_score():
    threats = [
        make_threat(
            Severity.HIGH,
            0.5,
        )
    ]

    score = calculate_risk_score(threats)

    assert score == 35.0


def test_multiple_threats_are_averaged():
    threats = [
        make_threat(
            Severity.HIGH,
            1.0,
        ),
        make_threat(
            Severity.LOW,
            1.0,
        ),
    ]

    score = calculate_risk_score(threats)

    assert score == 45.0


def test_risk_level_low():
    assert calculate_risk_level(10.0) == RiskLevel.LOW


def test_risk_level_medium():
    assert calculate_risk_level(30.0) == RiskLevel.MEDIUM


def test_risk_level_high():
    assert calculate_risk_level(60.0) == RiskLevel.HIGH


def test_risk_level_critical():
    assert calculate_risk_level(80.0) == RiskLevel.CRITICAL