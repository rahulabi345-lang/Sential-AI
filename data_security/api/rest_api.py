from __future__ import annotations

from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query

from data_security.api.public_interface import (
    get_event_by_id,
    get_recent_events,
    get_recent_threats,
    get_threat_by_id,
    get_latest_risk_assessment,
    get_risk_history,
    update_threat_status,
)


app = FastAPI(
    title="Sentinel-AI API",
    description="Windows security monitoring and threat detection API",
    version="1.0.0",
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root() -> dict[str, Any]:
    return {
        "name": "Sentinel-AI",
        "version": "1.0.0",
        "status": "online",
        "message": "Sentinel-AI REST API is running.",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }


# ============================================================
# EVENTS
# ============================================================

@app.get("/events")
def events(
    limit: int = Query(default=50, ge=1, le=500),
    severity: Optional[str] = None,
    host: Optional[str] = None,
    source: Optional[str] = None,
) -> list[dict[str, Any]]:

    try:
        return get_recent_events(
            limit=limit,
            severity=severity,
            host=host,
            source=source,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.get("/events/{event_id}")
def event_by_id(
    event_id: str,
) -> dict[str, Any]:

    event = get_event_by_id(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found.",
        )

    return event


# ============================================================
# THREATS
# ============================================================

@app.get("/threats")
def threats(
    limit: int = Query(default=50, ge=1, le=500),
    severity: Optional[str] = None,
    status: Optional[str] = None,
    threat_type: Optional[str] = None,
) -> list[dict[str, Any]]:

    try:
        return get_recent_threats(
            limit=limit,
            severity=severity,
            status=status,
            threat_type=threat_type,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.get("/threats/{threat_id}")
def threat_by_id(
    threat_id: str,
) -> dict[str, Any]:

    threat = get_threat_by_id(threat_id)

    if threat is None:
        raise HTTPException(
            status_code=404,
            detail="Threat not found.",
        )

    return threat


@app.put("/threats/{threat_id}/status")
def change_threat_status(
    threat_id: str,
    status: str,
) -> dict[str, Any]:

    try:

        updated = update_threat_status(
            threat_id,
            status,
        )

        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Threat not found.",
            )

        threat = get_threat_by_id(threat_id)

        return {
            "success": True,
            "message": "Threat status updated.",
            "threat": threat,
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


# ============================================================
# RISK ASSESSMENTS
# ============================================================

@app.get("/risk/{scope}")
def latest_risk(
    scope: str,
) -> dict[str, Any]:

    assessment = get_latest_risk_assessment(scope)

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="No risk assessment found for this scope.",
        )

    return assessment


@app.get("/risk/{scope}/history")
def risk_history(
    scope: str,
    limit: int = Query(default=50, ge=1, le=500),
) -> list[dict[str, Any]]:

    return get_risk_history(
        scope=scope,
        limit=limit,
    )