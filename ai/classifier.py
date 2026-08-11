"""Simple defensive threat classification."""

from typing import Any


def classify(event: dict[str, Any]) -> str:
    """Classify a security event using simple deterministic rules."""

    if not event:
        return "unknown"

    event_type = str(event.get("event_type", "")).lower()
    source = str(event.get("source", "")).lower()
    details = event.get("details", {})

    if not event_type and not source and not details:
        return "unknown"

    suspicious_terms = {
        "failed_login",
        "unexpected_process",
        "suspicious_connection",
        "unknown_process",
    }

    malicious_terms = {
        "malware",
        "ransomware",
        "trojan",
        "virus",
    }

    event_text = f"{event_type} {source} {details}".lower()

    if any(term in event_text for term in malicious_terms):
        return "malicious"

    if any(term in event_text for term in suspicious_terms):
        return "suspicious"

    if event_type in {"login", "file_access", "system_event"}:
        return "benign"

    return "unknown"