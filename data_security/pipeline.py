from __future__ import annotations

from typing import Any

from data_security.api.public_interface import (
    ingest_event,
    ingest_risk_assessment,
    ingest_threat,
)
from data_security.collectors.windows_event_collector import (
    read_recent_windows_events,
)
from data_security.detectors.basic_threat_detector import (
    detect_threats,
)
from data_security.repository.threat_repository import ThreatRepository
from data_security.risk.risk_engine import (
    calculate_risk_level,
    calculate_risk_score,
)


def run_security_analysis(
    log_name: str = "System",
    limit: int = 10,
    scope: str | None = None,
) -> dict[str, Any]:
    """
    Run the complete Windows security analysis pipeline.

    Windows events
        -> security events
        -> threat detection
        -> threat persistence
        -> risk assessment
    """

    # 1. Collect Windows events.
    events = read_recent_windows_events(
        log_name=log_name,
        limit=limit,
    )

    # 2. Store the collected events and attach their database IDs.
    stored_events: list[dict[str, Any]] = []

    for event in events:
        event_id = ingest_event(event)

        stored_event = dict(event)
        stored_event["event_id"] = event_id
        stored_events.append(stored_event)

    # 3. Detect threats.
    detected_threats = detect_threats(stored_events)

    # 4. Store detected threats.
    threat_ids: list[str] = []

    for threat_data in detected_threats:
        threat_id = ingest_threat(threat_data)
        threat_ids.append(threat_id)

    # 5. Load stored Threat objects for risk calculation.
    threat_repository = ThreatRepository()

    stored_threats = []

    for threat_id in threat_ids:
        threat = threat_repository.get_threat(threat_id)

        if threat is not None:
            stored_threats.append(threat)

    # 6. Calculate risk.
    risk_score = calculate_risk_score(stored_threats)
    risk_level = calculate_risk_level(risk_score)

    # 7. Determine the assessment scope.
    assessment_scope = scope

    if not assessment_scope:
        if stored_events:
            assessment_scope = stored_events[0]["host"]
        else:
            assessment_scope = "unknown"

    # 8. Store the risk assessment.
    assessment_id = ingest_risk_assessment(
        {
            "scope": assessment_scope,
            "risk_score": risk_score,
            "risk_level": risk_level.value,
            "related_threat_ids": threat_ids,
            "summary": (
                f"Risk assessment for {assessment_scope} "
                f"based on {len(threat_ids)} detected threats."
            )
        }
    )

    return {
        "events_collected": len(stored_events),
        "threats_detected": len(threat_ids),
        "risk_score": risk_score,
        "risk_level": risk_level.value,
        "assessment_id": assessment_id,
    }