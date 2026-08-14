from data_security.api.public_interface import (
    get_event_by_id,
    get_latest_risk_assessment,
    get_threat_by_id,
    ingest_event,
    ingest_risk_assessment,
    ingest_threat,
)

from data_security.collectors.windows_event_collector import (
    collect_windows_event,
)

from data_security.detectors.basic_threat_detector import (
    detect_threats,
)


def test_event_api_flow():
    event_id = ingest_event(
        {
            "source": "api_test",
            "event_type": "login_attempt",
            "severity": "low",
            "host": "API-TEST-PC",
            "description": "API test security event.",
        }
    )

    event = get_event_by_id(event_id)

    assert event is not None
    assert event["event_id"] == event_id
    assert event["host"] == "API-TEST-PC"


def test_threat_api_flow():
    event_id = ingest_event(
        {
            "source": "api_test",
            "event_type": "process_start",
            "severity": "medium",
            "host": "API-TEST-PC",
            "description": "API test process event.",
        }
    )

    threat_id = ingest_threat(
        {
            "related_event_ids": [event_id],
            "threat_type": "api_test_threat",
            "confidence_score": 0.85,
            "severity": "medium",
            "description": "API test threat.",
            "status": "new",
        }
    )

    threat = get_threat_by_id(threat_id)

    assert threat is not None
    assert threat["threat_id"] == threat_id
    assert threat["related_event_ids"] == [event_id]


def test_risk_api_flow():
    event_id = ingest_event(
        {
            "source": "api_test",
            "event_type": "risk_test",
            "severity": "high",
            "host": "API-RISK-PC",
            "description": "API risk test event.",
        }
    )

    threat_id = ingest_threat(
        {
            "related_event_ids": [event_id],
            "threat_type": "api_risk_test",
            "confidence_score": 0.9,
            "severity": "high",
            "description": "API risk test threat.",
            "status": "confirmed",
        }
    )

    assessment_id = ingest_risk_assessment(
        {
            "scope": "API-RISK-PC",
            "risk_score": 75.0,
            "risk_level": "high",
            "related_threat_ids": [threat_id],
            "summary": "API risk assessment test.",
        }
    )

    assessment = get_latest_risk_assessment("API-RISK-PC")

    assert assessment is not None
    assert assessment["assessment_id"] == assessment_id
    assert assessment["risk_score"] == 75.0
    assert assessment["risk_level"] == "high"


def test_windows_event_collector():
    event_id = collect_windows_event(
        {
            "source": "windows_event_log",
            "event_type": "login_attempt",
            "severity": "low",
            "host": "COLLECTOR-TEST-PC",
            "description": "Windows event collector test.",
        }
    )

    assert event_id

    event = get_event_by_id(event_id)

    assert event is not None
    assert event["event_id"] == event_id
    assert event["host"] == "COLLECTOR-TEST-PC"
    assert event["source"] == "windows_event_log"


def test_basic_threat_detector_detects_high_severity_event():
    events = [
        {
            "event_id": "detector-test-event-001",
            "severity": "high",
            "description": "Suspicious high severity event.",
        }
    ]

    threats = detect_threats(events)

    assert len(threats) == 1

    threat = threats[0]

    assert threat["related_event_ids"] == [
        "detector-test-event-001"
    ]
    assert threat["threat_type"] == "high_severity_event"
    assert threat["confidence_score"] == 0.90
    assert threat["severity"] == "high"
    assert threat["status"] == "new"