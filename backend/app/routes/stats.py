from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
import models
import schemas

router = APIRouter(
    tags=["Statistics"]
)


@router.get("/stats", response_model=schemas.StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """
    GET /stats
    Calculates dynamic statistics for security events stored in SQLite:
    - total_events
    - count per risk level (low, medium, high, critical)
    - total_alerts (high + critical)
    - latest_event_timestamp
    """
    total_events = db.query(func.count(models.SecurityEvent.id)).scalar() or 0

    low_count = db.query(func.count(models.SecurityEvent.id)).filter(models.SecurityEvent.risk_level == "LOW").scalar() or 0
    medium_count = db.query(func.count(models.SecurityEvent.id)).filter(models.SecurityEvent.risk_level == "MEDIUM").scalar() or 0
    high_count = db.query(func.count(models.SecurityEvent.id)).filter(models.SecurityEvent.risk_level == "HIGH").scalar() or 0
    critical_count = db.query(func.count(models.SecurityEvent.id)).filter(models.SecurityEvent.risk_level == "CRITICAL").scalar() or 0

    total_alerts = high_count + critical_count

    latest_event = db.query(models.SecurityEvent).order_by(models.SecurityEvent.timestamp.desc()).first()
    latest_timestamp = latest_event.timestamp if latest_event else None

    return schemas.StatsResponse(
        total_events=total_events,
        low=low_count,
        medium=medium_count,
        high=high_count,
        critical=critical_count,
        total_alerts=total_alerts,
        latest_event_timestamp=latest_timestamp
    )
