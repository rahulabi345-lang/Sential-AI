from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from app.risk_engine import calculate_risk
from app.ai_analyzer import analyze_event

router = APIRouter(
    tags=["AI Analysis"]
)


@router.post("/analyze", response_model=schemas.AIAnalysisResponse, status_code=status.HTTP_200_OK)
def analyze_event_endpoint(
    payload: Optional[schemas.AnalyzeRequest] = None,
    event_id: Optional[int] = Query(None, description="ID of the security event to analyze"),
    db: Session = Depends(get_db)
):
    """
    POST /analyze
    Fetches a security event by ID, retrieves or calculates its risk assessment,
    generates an AI-driven explanation and safe defensive recommendations,
    persists the analysis in SQLite, and returns structured JSON output.
    """
    target_id = None
    if payload and payload.event_id is not None:
        target_id = payload.event_id
    elif event_id is not None:
        target_id = event_id

    if target_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="event_id must be provided in request body JSON or as a query parameter."
        )

    # 1. Get event from SQLite database
    db_event = db.query(models.SecurityEvent).filter(models.SecurityEvent.id == target_id).first()
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security event with ID {target_id} not found"
        )

    # 2. Get risk score, risk level, and risk reasons (calculate if missing)
    risk_score = db_event.risk_score
    risk_level = db_event.risk_level
    risk_reasons = db_event.risk_reasons or []

    if risk_score is None or (risk_score == 0 and not risk_reasons):
        risk_info = calculate_risk(db_event)
        risk_score = risk_info["risk_score"]
        risk_level = risk_info["risk_level"]
        risk_reasons = risk_info["reasons"]
        
        # Save calculated risk back to event
        db_event.risk_score = risk_score
        db_event.risk_level = risk_level
        db_event.risk_reasons = risk_reasons

    # 3. Send event information to AI Analyzer (fallback on any error)
    try:
        analysis = analyze_event(
            event=db_event,
            risk_score=risk_score,
            risk_level=risk_level,
            risk_reasons=risk_reasons
        )
    except Exception:
        from app.ai_analyzer import generate_fallback_analysis
        analysis = generate_fallback_analysis(
            event=db_event,
            risk_score=risk_score,
            risk_level=risk_level,
            risk_reasons=risk_reasons
        )

    # 4. Store AI analysis in SQLite
    db_event.ai_title = analysis["title"]
    db_event.ai_summary = analysis["summary"]
    db_event.ai_explanation = analysis["explanation"]
    db_event.ai_indicators = analysis["indicators"]
    db_event.ai_recommended_actions = analysis["recommended_actions"]
    db_event.ai_confidence = analysis["confidence"]

    db.commit()
    db.refresh(db_event)

    # 5. Return structured JSON matching AIAnalysisResponse
    return analysis


@router.post("/events/{event_id}/analyze", response_model=schemas.AIAnalysisResponse, status_code=status.HTTP_200_OK)
def analyze_event_by_path_endpoint(
    event_id: int,
    db: Session = Depends(get_db)
):
    """
    POST /events/{event_id}/analyze (Alias route)
    Allows analyzing an event using path parameter.
    """
    return analyze_event_endpoint(payload=schemas.AnalyzeRequest(event_id=event_id), db=db)
