"""Data models for security events and analysis results."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SecurityEvent:
    """Placeholder model representing a single security event."""

    id: str
    source: str
    timestamp: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    """Placeholder model representing the output of threat analysis."""

    event_id: str
    category: str
    risk_score: float
    explanation: str
    recommendations: list[str] = field(default_factory=list)
