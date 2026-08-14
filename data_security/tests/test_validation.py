"""
Tests for Threat and RiskAssessment validation rules.
"""

import pytest
from pydantic import ValidationError

from data_security.models.risk_assessment import RiskAssessment, RiskLevel
from data_security.models.security_event import Severity
from data_security.models.threat import Threat, ThreatStatus


def _valid_threat_kwargs():
    return dict(
        threat_type="suspicious_process",
        confidence_score=0.75,
        severity=Severity.HIGH,
        description="Process exhibited suspicious behavior.",
    )


def _valid_risk_kwargs():
    return dict(
        scope="system",
        risk_score=42.0,
        risk_level=RiskLevel.MEDIUM,
        summary="Elevated risk due to recent suspicious activity.",
    )


def test_confidence_score_out_of_range_high_is_rejected():
    kwargs = _valid_threat_kwargs()
    kwargs["confidence_score"] = 1.5

    with pytest.raises(ValidationError):
        Threat(**kwargs)


def test_confidence_score_out_of_range_low_is_rejected():
    kwargs = _valid_threat_kwargs()
    kwargs["confidence_score"] = -0.1

    with pytest.raises(ValidationError):
        Threat(**kwargs)


def test_confidence_score_boundaries_are_accepted():
    assert Threat(
        **{**_valid_threat_kwargs(), "confidence_score": 0.0}
    )

    assert Threat(
        **{**_valid_threat_kwargs(), "confidence_score": 1.0}
    )


def test_risk_score_out_of_range_high_is_rejected():
    kwargs = _valid_risk_kwargs()
    kwargs["risk_score"] = 150.0

    with pytest.raises(ValidationError):
        RiskAssessment(**kwargs)


def test_risk_score_out_of_range_low_is_rejected():
    kwargs = _valid_risk_kwargs()
    kwargs["risk_score"] = -5.0

    with pytest.raises(ValidationError):
        RiskAssessment(**kwargs)


def test_risk_score_boundaries_are_accepted():
    assert RiskAssessment(
        **{**_valid_risk_kwargs(), "risk_score": 0.0}
    )

    assert RiskAssessment(
        **{**_valid_risk_kwargs(), "risk_score": 100.0}
    )


def test_invalid_threat_status_is_rejected():
    kwargs = _valid_threat_kwargs()
    kwargs["status"] = "resolved"

    with pytest.raises(ValidationError):
        Threat(**kwargs)


def test_valid_threat_status_is_accepted():
    kwargs = _valid_threat_kwargs()
    kwargs["status"] = ThreatStatus.INVESTIGATING

    threat = Threat(**kwargs)

    assert threat.status == ThreatStatus.INVESTIGATING


def test_non_json_serializable_indicators_is_rejected():
    kwargs = _valid_threat_kwargs()
    kwargs["indicators"] = {"bad": object()}

    with pytest.raises(ValidationError):
        Threat(**kwargs)