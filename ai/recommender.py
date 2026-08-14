"""Recommend defensive actions based on analysis results."""

from typing import List


def recommend(category: str, risk_score: float) -> List[str]:
    """Return defensive actions based on threat category and risk score."""

    category = category.lower().strip()

    if category == "benign":
        return [
            "Continue monitoring the activity.",
        ]

    if category == "suspicious":
        recommendations = [
            "Investigate the event and review related security logs.",
            "Check the affected account or system for additional suspicious activity.",
        ]

        if risk_score >= 70:
            recommendations.append(
                "Consider enabling stronger authentication controls such as MFA."
            )

        return recommendations

    if category == "malicious":
        return [
            "Isolate the affected system if possible.",
            "Investigate the event and review related security logs.",
            "Reset potentially compromised credentials.",
            "Escalate the incident for immediate security response.",
        ]

    return [
        "Collect additional information about the event.",
        "Review related security logs before taking further action.",
    ]