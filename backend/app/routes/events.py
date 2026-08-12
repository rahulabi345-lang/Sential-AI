from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

# APIRouter allows us to group related routes together
router = APIRouter(
    tags=["Events"]
)


# Endpoint 1: GET /events - Retrieve a list of security events from SQLite
@router.get("/events", response_model=list[schemas.SecurityEventResponse])
def get_events(db: Session = Depends(get_db)):
    """Retrieves all security events stored in SQLite database."""
    events = db.query(models.SecurityEvent).all()
    return events


# Endpoint 2: GET /events/{event_id} - Retrieve details of a specific event from SQLite
@router.get("/events/{event_id}", response_model=schemas.SecurityEventResponse)
def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    """Retrieves a single security event by its ID from SQLite database."""
    db_event = db.query(models.SecurityEvent).filter(models.SecurityEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security event with ID {event_id} not found"
        )
    return db_event

