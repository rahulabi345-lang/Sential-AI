from data_security.detectors.basic_threat_detector import detect_threats


def test_detects_high_severity_event():
    events = [
        {
            "event_id": "test-high-001",
            "severity": "high",
            "event_type": "system_event",
            "description": "High severity event",
        }
    ]

    threats = detect_threats(events)

    assert len(threats) == 1
    assert threats[0]["threat_type"] == "high_severity_event"
    assert threats[0]["confidence_score"] == 0.90


def test_detects_suspicious_process():
    events = [
        {
            "event_id": "test-process-001",
            "severity": "medium",
            "event_type": "process_start",
            "process_name": "test.exe",
            "description": "Process start test",
        }
    ]

    threats = detect_threats(events)

    assert len(threats) == 1
    assert threats[0]["threat_type"] == "suspicious_process_activity"
    assert threats[0]["confidence_score"] == 0.80
    assert threats[0]["indicators"]["rule"] == "suspicious_process"


def test_detects_suspicious_login():
    events = [
        {
            "event_id": "test-login-001",
            "severity": "medium",
            "event_type": "failed_login",
            "description": "Failed login test",
        }
    ]

    threats = detect_threats(events)

    assert len(threats) == 1
    assert threats[0]["threat_type"] == "suspicious_login_attempt"
    assert threats[0]["confidence_score"] == 0.85
    assert threats[0]["indicators"]["rule"] == "suspicious_login"


def test_normal_event_produces_no_threat():
    events = [
        {
            "event_id": "test-normal-001",
            "severity": "low",
            "event_type": "normal_activity",
            "description": "Normal event",
        }
    ]

    threats = detect_threats(events)

    assert threats == []