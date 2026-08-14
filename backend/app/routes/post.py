from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from app.risk_engine import calculate_risk

# APIRouter allows us to group related routes together
router = APIRouter(
    tags=["Events"]
)


# Endpoint: POST /events - Create a new security event and store in SQLite
@router.post("/events", response_model=schemas.SecurityEventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.SecurityEventCreate, db: Session = Depends(get_db)):
    """Receives a security event payload, evaluates risk, saves it into SQLite database, and returns created event."""
    event_data = event.model_dump()

    # Calculate risk score, level, and reasons if not explicitly provided
    if event_data.get("risk_score") is None:
        risk_info = calculate_risk(event_data)
        event_data["risk_score"] = risk_info["risk_score"]
        event_data["risk_level"] = risk_info["risk_level"]
        event_data["risk_reasons"] = risk_info["reasons"]

    db_event = models.SecurityEvent(**event_data)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


