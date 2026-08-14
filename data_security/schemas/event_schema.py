from typing import Any, Optional

from data_security.models.security_event import Severity


class EventSchema:
    """
    Validation contract for events coming from
    the Windows monitoring module.
    """

    REQUIRED_FIELDS = {
        "source",
        "event_type",
        "severity",
        "host",
        "description",
    }

    OPTIONAL_FIELDS = {
        "timestamp",
        "user",
        "process_name",
        "raw_data",
    }

    @staticmethod
    def validate(data: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise ValueError("Event must be a dictionary.")

        missing = EventSchema.REQUIRED_FIELDS - data.keys()

        if missing:
            raise ValueError(
                f"Missing required fields: {sorted(missing)}"
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

        raw_data: Optional[Any] = data.get("raw_data")

        if raw_data is not None and not isinstance(raw_data, dict):
            raise ValueError(
                "raw_data must be a JSON object."
            )