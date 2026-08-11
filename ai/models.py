"""Data models for security events and threat analysis results."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Recommendation:
    """A safe defensive action suggested to the user."""

    title: str
    description: str
    priority: str


@dataclass
class SecurityEvent:
    """An event received from other Sentinel AI monitoring modules."""
    id: str
    event_type: str
    source: str
    timestamp: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ThreatAssessment:
    """The result of Sentinel AI's analysis of a security event."""

    threat_type: str
    risk_score: int
    risk_level: str
    confidence: float
    explanation: str
    recommendations: list[Recommendation] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 0 <= self.risk_score <= 100:
            raise ValueError("risk_score must be between 0 and 100")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
