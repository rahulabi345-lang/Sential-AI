"""Risk scoring for Sentinel AI security events."""

from typing import Any


def calculate_risk_score(
    classification: str,
    event: dict[str, Any] | None = None,
) -> int:
    """Return a risk score from 0 to 100."""

    classification = classification.lower().strip()

    base_scores = {
        "benign": 10,
        "unknown": 20,
        "suspicious": 60,
        "malicious": 90,
    }

    score = base_scores.get(classification, 20)

    if event:
        event_text = str(event).lower()

        if "failed_login" in event_text:
            score += 10

        if "malware" in event_text:
            score += 10

        if "ransomware" in event_text:
            score += 10

    return min(score, 100)


def get_risk_level(score: int) -> str:
    """Convert a numerical score into a risk level."""

    if score <= 30:
        return "low"

    if score <= 70:
        return "medium"

    return "high"