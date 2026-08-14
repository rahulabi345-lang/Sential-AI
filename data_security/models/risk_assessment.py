from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from data_security.models.security_event import DESCRIPTION_MAX_LENGTH


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _new_uuid() -> str:
    return str(uuid.uuid4())


class RiskAssessment(BaseModel):
    assessment_id: str = Field(default_factory=_new_uuid)
    scope: str = Field(..., min_length=1, max_length=255)
    risk_score: float = Field(..., ge=0.0, le=100.0)
    risk_level: RiskLevel
    related_threat_ids: list[str] = Field(default_factory=list)
    summary: str = Field(..., max_length=DESCRIPTION_MAX_LENGTH)
    assessed_at: datetime = Field(default_factory=_utc_now)
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("assessed_at", "created_at")
    @classmethod
    def _ensure_timezone_aware_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @field_validator("related_threat_ids")
    @classmethod
    def _ensure_non_empty_ids(cls, value: list[str]) -> list[str]:
        for threat_id in value:
            if not threat_id or not threat_id.strip():
                raise ValueError(
                    "related_threat_ids must not contain empty values"
                )
        return value

    @field_validator("summary")
    @classmethod
    def _strip_summary(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("summary must not be empty")
        return value