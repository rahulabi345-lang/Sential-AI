from __future__ import annotations

from data_security.models.risk_assessment import RiskLevel
from data_security.models.threat import Threat


def calculate_risk_score(threats: list[Threat]) -> float:
    """
    Calculate an overall risk score from detected threats.

    The score is based on threat severity and confidence.
    The final score is limited to the range 0-100.
    """

    severity_weights = {
        "low": 20.0,
        "medium": 40.0,
        "high": 70.0,
        "critical": 100.0,
    }

    if not threats:
        return 0.0

    total_score = 0.0

    for threat in threats:
        severity_score = severity_weights[threat.severity.value]

        threat_score = (
            severity_score
            * threat.confidence_score
        )

        total_score += threat_score

    # Average the threat scores so that the number
    # of threats does not automatically exceed 100.
    score = total_score / len(threats)

    return round(min(score, 100.0), 2)


def calculate_risk_level(
    risk_score: float,
) -> RiskLevel:
    """
    Convert a numerical risk score into a risk level.
    """

    if risk_score >= 80.0:
        return RiskLevel.CRITICAL

    if risk_score >= 60.0:
        return RiskLevel.HIGH

    if risk_score >= 30.0:
        return RiskLevel.MEDIUM

    return RiskLevel.LOW