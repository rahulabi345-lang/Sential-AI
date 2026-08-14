from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class SecurityEventCreate(BaseModel):
    """Schema for validating payload when creating a new Security Event."""
    timestamp: datetime
    event_type: str
    source: str
    hostname: str
    username: str
    process_name: str
    process_id: int
    severity: str
    description: str
    raw_data: Optional[dict[str, Any]] = Field(default_factory=dict)
    risk_score: Optional[int] = None
    risk_level: Optional[str] = None
    risk_reasons: Optional[List[str]] = None


class SecurityEventResponse(SecurityEventCreate):
    """Schema for returning a Security Event with database ID, risk details, and optional AI analysis."""
    id: int
    risk_score: Optional[int] = 0
    risk_level: Optional[str] = "LOW"
    risk_reasons: Optional[List[Any]] = Field(default_factory=list)
    ai_title: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_explanation: Optional[str] = None
    ai_indicators: Optional[List[str]] = Field(default_factory=list)
    ai_recommended_actions: Optional[List[str]] = Field(default_factory=list)
    ai_confidence: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class AIAnalysisResponse(BaseModel):
    """Schema for structured AI analysis response output."""
    title: str
    summary: str
    explanation: str
    indicators: List[str]
    recommended_actions: List[str]
    confidence: int


class AnalyzeRequest(BaseModel):
    """Schema for POST /analyze payload."""
    event_id: int


# Alias SecurityEvent to SecurityEventResponse for compatibility
SecurityEvent = SecurityEventResponse


class AlertResponse(BaseModel):
    """Schema for returning security alerts (HIGH or CRITICAL risk events)."""
    event_id: int
    timestamp: datetime
    event_type: str
    process_name: str
    risk_score: Optional[int] = 0
    risk_level: Optional[str] = "LOW"
    risk_reasons: Optional[List[Any]] = Field(default_factory=list)
    ai_summary: Optional[str] = None
    recommended_actions: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


class StatsResponse(BaseModel):
    """Schema for returning security event statistics from SQLite."""
    total_events: int = 0
    low: int = 0
    medium: int = 0
    high: int = 0
    critical: int = 0
    total_alerts: int = 0
    latest_event_timestamp: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)



