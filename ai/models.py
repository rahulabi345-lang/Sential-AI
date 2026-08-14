"""Data models for security events and threat analysis results."""

from dataclasses import dataclass


@dataclass
class SecurityEvent:
    """An event received from other Sentinel AI monitoring modules."""

    id: str
    event_type: str
    source: str
    timestamp: str


@dataclass
class ThreatResult:
    """The result of analyzing a security event."""

    event_id: str
    classification: str
    risk_score: float
    explanation: str


@dataclass
class Recommendation:
    """A safe defensive action suggested to the user."""

    title: str
    description: str
    severity: str
