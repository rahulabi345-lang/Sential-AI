"""Analyze security events and telemetry for suspicious patterns."""

from typing import Any

from ai.classifier import classify
from ai.explainer import explain
from ai.recommender import recommend
from ai.risk_scoring import calculate_risk_score


def analyze(event: dict[str, Any]) -> dict[str, Any]:
    """Run the complete Sentinel AI analysis pipeline."""

    classification = classify(event)

    risk_score = calculate_risk_score(
        classification,
        event,
    )

    explanation = explain(
        event,
        classification,
        risk_score,
    )

    recommendations = recommend(
        classification,
        risk_score,
    )

    return {
        "event_id": event.get("id"),
        "classification": classification,
        "risk_score": risk_score,
        "explanation": explanation,
        "recommendations": recommendations,
    }