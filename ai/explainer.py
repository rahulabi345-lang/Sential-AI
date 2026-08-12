"""Generate human-readable explanations for analysis results."""

from typing import Any


def explain(
    event: dict[str, Any],
    category: str,
    risk_score: float,
) -> str:
    """Generate a plain-language explanation of a security event."""

    category = category.lower().strip()

    event_type = str(event.get("event_type", "security event"))
    source = str(event.get("source", "unknown source"))

    if category == "benign":
        return (
            f"The {event_type} from {source} appears to be normal activity. "
            f"The current risk score is {risk_score:.0f}/100, indicating low risk."
        )

    if category == "suspicious":
        return (
            f"The {event_type} from {source} shows suspicious activity. "
            f"The current risk score is {risk_score:.0f}/100, "
            "so this event should be investigated."
        )

    if category == "malicious":
        return (
            f"The {event_type} from {source} appears to be malicious activity. "
            f"The current risk score is {risk_score:.0f}/100, "
            "indicating a high-risk event that requires immediate investigation."
        )

    return (
        f"The {event_type} from {source} could not be confidently classified. "
        f"The current risk score is {risk_score:.0f}/100, "
        "so additional investigation may be required."
    )