from __future__ import annotations

from data_security.models.risk_assessment import RiskAssessment
from data_security.repository.risk_repository import RiskRepository
from data_security.repository.threat_repository import ThreatRepository

from data_security.risk.risk_engine import (
    calculate_risk_level,
    calculate_risk_score,
)


def assess_risk(
    scope: str,
    limit: int = 50,
) -> str:
    """
    Calculate and store a risk assessment for a scope.

    Args:
        scope:
            The scope being assessed, usually a host name.

        limit:
            Maximum number of recent threats to consider.

    Returns:
        The newly created risk assessment ID.
    """

    threat_repository = ThreatRepository()
    risk_repository = RiskRepository()

    # Only analyze threats associated with this host/scope.
    threats = threat_repository.query_threats(
        host=scope,
        limit=limit,
    )

    risk_score = calculate_risk_score(threats)
    risk_level = calculate_risk_level(risk_score)

    related_threat_ids = [
        threat.threat_id
        for threat in threats
    ]

    if threats:
        summary = (
            f"Risk assessment for {scope}: "
            f"{len(threats)} threat(s) analyzed. "
            f"Risk score {risk_score}/100, "
            f"risk level {risk_level.value}."
        )
    else:
        summary = (
            f"Risk assessment for {scope}: "
            "No threats detected. "
            "Risk score 0/100, risk level low."
        )

    assessment = RiskAssessment(
        scope=scope,
        risk_score=risk_score,
        risk_level=risk_level,
        related_threat_ids=related_threat_ids,
        summary=summary,
    )

    return risk_repository.add_assessment(assessment)