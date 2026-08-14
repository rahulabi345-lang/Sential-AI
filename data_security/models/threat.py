from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator

from data_security.models.security_event import DESCRIPTION_MAX_LENGTH, Severity


class ThreatStatus(str, Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    CONFIRMED = "confirmed"
    DISMISSED = "dismissed"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _new_uuid() -> str:
    return str(uuid.uuid4())


class Threat(BaseModel):
    threat_id: str = Field(default_factory=_new_uuid)
    related_event_ids: list[str] = Field(default_factory=list)
    threat_type: str = Field(..., min_length=1, max_length=200)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    severity: Severity
    description: str = Field(..., max_length=DESCRIPTION_MAX_LENGTH)
    indicators: dict[str, Any] = Field(default_factory=dict)
    status: ThreatStatus = Field(default=ThreatStatus.NEW)
    detected_at: datetime = Field(default_factory=_utc_now)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("detected_at", "created_at")
    @classmethod
    def _ensure_timezone_aware_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @field_validator("indicators")
    @classmethod
    def _ensure_json_serializable(cls, value: dict[str, Any]) -> dict[str, Any]:
        try:
            json.dumps(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"indicators must be JSON-serializable: {exc}"
            ) from exc
        return value

    @field_validator("related_event_ids")
    @classmethod
    def _ensure_non_empty_ids(cls, value: list[str]) -> list[str]:
        for event_id in value:
            if not event_id or not event_id.strip():
                raise ValueError(
                    "related_event_ids must not contain empty values"
                )
        return value

    @field_validator("description")
    @classmethod
    def _strip_description(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("description must not be empty")
        return value