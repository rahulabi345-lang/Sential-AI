from __future__ import annotations

from data_security.detectors.basic_threat_detector import detect_threats
from data_security.models.threat import Threat
from data_security.repository.event_repository import EventRepository
from data_security.repository.threat_repository import ThreatRepository


def detect_and_store_threats(
    limit: int = 50,
) -> list[str]:
    """
    Read recent security events, detect threats,
    validate them, and store only newly detected threats.

    Returns:
        A list of newly stored threat IDs.
    """

    event_repository = EventRepository()
    threat_repository = ThreatRepository()

    # 1. Read recent security events.
    events = event_repository.query_events(limit=limit)

    # 2. Convert Pydantic models to dictionaries.
    event_data = [
        event.model_dump(mode="json")
        for event in events
    ]

    # 3. Run the threat detector.
    detected_threats = detect_threats(event_data)

    threat_ids: list[str] = []

    # 4. Process each detected threat.
    for threat_data in detected_threats:
        threat = Threat(**threat_data)

        # 5. Check whether this event/threat was already stored.
        existing_threats = threat_repository.query_threats(
            threat_type=threat.threat_type,
            limit=100,
        )

        already_exists = any(
            set(existing.related_event_ids)
            == set(threat.related_event_ids)
            for existing in existing_threats
        )

        # 6. Skip duplicate threats.
        if already_exists:
            continue

        # 7. Store the new threat.
        threat_id = threat_repository.add_threat(threat)
        threat_ids.append(threat_id)

    return threat_ids