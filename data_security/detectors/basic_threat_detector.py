from __future__ import annotations

from typing import Any


def _high_severity_rule(event: dict[str, Any]) -> dict[str, Any] | None:
    severity = str(event.get("severity", "")).lower()

    if severity in {"high", "critical"}:
        return {
            "threat_type": "high_severity_event",
            "description": (
                f"High-severity Windows security event detected: "
                f"{event.get('description', 'Unknown event')}."
            ),
            "confidence_score": 0.90,
            "severity": severity,
            "status": "new",
            "related_event_ids": [event["event_id"]],
            "indicators": {
                "rule": "high_severity",
            },
        }

    return None


def _suspicious_login_rule(event: dict[str, Any]) -> dict[str, Any] | None:
    event_type = str(event.get("event_type", "")).lower()

    login_types = {
        "login_attempt",
        "failed_login",
        "authentication_failure",
        "login_failure",
    }

    if event_type in login_types:
        return {
            "threat_type": "suspicious_login_attempt",
            "description": (
                f"Suspicious login activity detected: "
                f"{event.get('description', 'Unknown event')}."
            ),
            "confidence_score": 0.85,
            "severity": "medium",
            "status": "new",
            "related_event_ids": [event["event_id"]],
            "indicators": {
                "rule": "suspicious_login",
            },
        }

    return None


def _suspicious_process_rule(event: dict[str, Any]) -> dict[str, Any] | None:
    event_type = str(event.get("event_type", "")).lower()

    process_types = {
        "process_start",
        "process_creation",
        "suspicious_process",
    }

    if event_type in process_types:
        return {
            "threat_type": "suspicious_process_activity",
            "description": (
                f"Suspicious process activity detected: "
                f"{event.get('description', 'Unknown event')}."
            ),
            "confidence_score": 0.80,
            "severity": "medium",
            "status": "new",
            "related_event_ids": [event["event_id"]],
            "indicators": {
                "rule": "suspicious_process",
            },
        }

    return None


def _windows_application_error_rule(
    event: dict[str, Any],
) -> dict[str, Any] | None:
    """
    Detect Windows Application Error events.

    Event ID 1000 represents an application error/crash.
    This is treated as a medium-severity security-relevant event,
    but is not classified as malicious activity by itself.
    """

    event_type = str(event.get("event_type", "")).strip()
    source = str(event.get("source", "")).lower()

    if event_type == "1000" and source == "windows_event_log":
        return {
            "threat_type": "application_error",
            "description": (
                f"Windows Application Error detected: "
                f"{event.get('description', 'Unknown application error')}."
            ),
            "confidence_score": 0.70,
            "severity": "medium",
            "status": "new",
            "related_event_ids": [event["event_id"]],
            "indicators": {
                "rule": "windows_application_error",
            },
        }

    return None


def detect_threats(
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Apply all threat detection rules to normalized security events.
    """

    threats: list[dict[str, Any]] = []

    for event in events:
        if not event.get("event_id"):
            continue

        rules = (
            _high_severity_rule,
            _suspicious_login_rule,
            _suspicious_process_rule,
            _windows_application_error_rule,
        )

        for rule in rules:
            threat = rule(event)

            if threat is not None:
                threats.append(threat)

    return threats