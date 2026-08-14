from __future__ import annotations

from typing import Any, Optional

from pydantic import ValidationError as PydanticValidationError

from data_security.db.connection import initialize_database
from data_security.models.risk_assessment import RiskAssessment
from data_security.models.security_event import SecurityEvent, Severity
from data_security.models.threat import Threat, ThreatStatus
from data_security.repository.event_repository import EventRepository
from data_security.repository.risk_repository import RiskRepository
from data_security.repository.threat_repository import ThreatRepository


_events = EventRepository()
_threats = ThreatRepository()
_risks = RiskRepository()

_initialized = False


class ValidationError(ValueError):
    """Raised when supplied data fails validation."""


class ReferenceError(ValueError):
    """Raised when a record references an ID that does not exist."""


def _ensure_initialized() -> None:
    global _initialized

    if not _initialized:
        initialize_database()
        _initialized = True


# ---------------------------------------------------------
# EVENT FUNCTIONS
# ---------------------------------------------------------

def ingest_event(event_dict: dict[str, Any]) -> str:
    """
    Validate and store a security event.

    Used by the monitoring module.
    """

    _ensure_initialized()

    try:
        event = SecurityEvent(**event_dict)
    except PydanticValidationError as exc:
        raise ValidationError(
            f"Invalid event data: {exc}"
        ) from exc

    return _events.add_event(event)


def get_recent_events(
    limit: int = 50,
    severity: Optional[str] = None,
    host: Optional[str] = None,
    source: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Return recent security events."""

    _ensure_initialized()

    severity_enum = (
        Severity(severity)
        if severity
        else None
    )

    events = _events.query_events(
        severity=severity_enum,
        host=host,
        source=source,
        limit=limit,
    )

    return [
        event.model_dump(mode="json")
        for event in events
    ]


def get_event_by_id(
    event_id: str,
) -> Optional[dict[str, Any]]:
    """Return one security event by ID."""

    _ensure_initialized()

    event = _events.get_event(event_id)

    if event is None:
        return None

    return event.model_dump(mode="json")


# ---------------------------------------------------------
# THREAT FUNCTIONS
# ---------------------------------------------------------

def ingest_threat(
    threat_dict: dict[str, Any],
) -> str:
    """
    Validate and store a threat.

    Used by the AI/threat intelligence module.
    """

    _ensure_initialized()

    try:
        threat = Threat(**threat_dict)
    except PydanticValidationError as exc:
        raise ValidationError(
            f"Invalid threat data: {exc}"
        ) from exc

    # Make sure referenced events actually exist.
    for event_id in threat.related_event_ids:

        if _events.get_event(event_id) is None:
            raise ReferenceError(
                f"Unknown event_id: {event_id}"
            )

    return _threats.add_threat(threat)


def get_recent_threats(
    limit: int = 50,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    threat_type: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Return recent threats."""

    _ensure_initialized()

    severity_enum = (
        Severity(severity)
        if severity
        else None
    )

    status_enum = (
        ThreatStatus(status)
        if status
        else None
    )

    threats = _threats.query_threats(
        severity=severity_enum,
        status=status_enum,
        threat_type=threat_type,
        limit=limit,
    )

    return [
        threat.model_dump(mode="json")
        for threat in threats
    ]


def get_threat_by_id(
    threat_id: str,
) -> Optional[dict[str, Any]]:
    """Return one threat by ID."""

    _ensure_initialized()

    threat = _threats.get_threat(threat_id)

    if threat is None:
        return None

    return threat.model_dump(mode="json")


def update_threat_status(
    threat_id: str,
    status: str,
) -> bool:
    """
    Update the status of an existing threat.
    """

    _ensure_initialized()

    try:
        status_enum = ThreatStatus(status)
    except ValueError as exc:
        raise ValidationError(
            f"Invalid threat status: {status}"
        ) from exc

    if _threats.get_threat(threat_id) is None:
        raise ReferenceError(
            f"Unknown threat_id: {threat_id}"
        )

    return _threats.update_status(
        threat_id,
        status_enum,
    )


# ---------------------------------------------------------
# RISK FUNCTIONS
# ---------------------------------------------------------

def ingest_risk_assessment(
    assessment_dict: dict[str, Any],
) -> str:
    """
    Validate and store a risk assessment.
    """

    _ensure_initialized()

    try:
        assessment = RiskAssessment(**assessment_dict)
    except PydanticValidationError as exc:
        raise ValidationError(
            f"Invalid risk assessment: {exc}"
        ) from exc

    # Make sure referenced threats exist.
    for threat_id in assessment.related_threat_ids:

        if _threats.get_threat(threat_id) is None:
            raise ReferenceError(
                f"Unknown threat_id: {threat_id}"
            )

    return _risks.add_assessment(assessment)


def get_latest_risk_assessment(
    scope: str,
) -> Optional[dict[str, Any]]:
    """Return the latest risk assessment for a scope."""

    _ensure_initialized()

    assessment = _risks.get_latest_assessment(scope)

    if assessment is None:
        return None

    return assessment.model_dump(mode="json")


def get_risk_history(
    scope: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Return historical risk assessments."""

    _ensure_initialized()

    assessments = _risks.query_assessments(
        scope=scope,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )

    return [
        assessment.model_dump(mode="json")
        for assessment in assessments
    ]