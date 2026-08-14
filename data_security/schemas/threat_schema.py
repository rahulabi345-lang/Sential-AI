from typing import Any

from data_security.models.security_event import Severity
from data_security.models.threat import ThreatStatus


class ThreatSchema:
    """
    Validation contract for threats coming from
    the AI/threat-intelligence module.
    """

    REQUIRED_FIELDS = {
        "threat_type",
        "confidence_score",
        "severity",
        "description",
        "related_event_ids",
    }

    OPTIONAL_FIELDS = {
        "indicators",
        "status",
    }

    @staticmethod
    def validate(data: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise ValueError(
                "Threat must be a dictionary."
            )

        missing = (
            ThreatSchema.REQUIRED_FIELDS - data.keys()
        )

        if missing:
            raise ValueError(
                f"Missing required fields: {sorted(missing)}"
            )

        confidence = data["confidence_score"]

        if not isinstance(confidence, (int, float)):
            raise ValueError(
                "confidence_score must be a number."
            )

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "confidence_score must be between 0.0 and 1.0."
            )

        try:
            Severity(data["severity"])
        except ValueError as exc:
            raise ValueError(
                f"Invalid severity: {data['severity']}"
            ) from exc

        description = data["description"]

        if not isinstance(description, str):
            raise ValueError(
                "description must be a string."
            )

        if len(description) > 2000:
            raise ValueError(
                "description cannot exceed 2000 characters."
            )

        event_ids = data["related_event_ids"]

        if not isinstance(event_ids, list):
            raise ValueError(
                "related_event_ids must be a list."
            )

        for event_id in event_ids:
            if not isinstance(event_id, str) or not event_id.strip():
                raise ValueError(
                    "related_event_ids must contain valid IDs."
                )

        if "status" in data:
            try:
                ThreatStatus(data["status"])
            except ValueError as exc:
                raise ValueError(
                    f"Invalid threat status: {data['status']}"
                ) from exc