from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(
    tags=["Alerts"]
)


@router.get("/alerts", response_model=List[schemas.AlertResponse])
def get_alerts(
    risk_level: Optional[str] = Query(None, description="Optional risk level filter (e.g. HIGH or CRITICAL)"),
    db: Session = Depends(get_db)
):
    """
    GET /alerts
    Retrieves security events from SQLite where risk_level is HIGH or CRITICAL.
    Supports optional filtering by risk_level (e.g. GET /alerts?risk_level=HIGH).
    """
    query = db.query(models.SecurityEvent)

    if risk_level:
        target_level = risk_level.strip().upper()
        query = query.filter(models.SecurityEvent.risk_level == target_level)
    else:
        query = query.filter(models.SecurityEvent.risk_level.in_(["HIGH", "CRITICAL"]))

    events = query.all()

    alerts = []
    for event in events:
        alerts.append(
            schemas.AlertResponse(
                event_id=event.id,
                timestamp=event.timestamp,
                event_type=event.event_type,
                process_name=event.process_name,
                risk_score=event.risk_score,
                risk_level=event.risk_level,
                risk_reasons=event.risk_reasons or [],
                ai_summary=event.ai_summary,
                recommended_actions=event.ai_recommended_actions if event.ai_recommended_actions else None
            )
        )
    return alerts
