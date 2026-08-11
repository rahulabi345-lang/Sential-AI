"""Sentinel AI Security Assistant."""

from typing import Any

from ai.analyzer import analyze
from ai.llm import ask_llm


def build_security_prompt(
    event: dict[str, Any],
    analysis: dict[str, Any],
) -> str:
    """Build a safe prompt for the local security assistant."""

    return f"""
You are Sentinel AI, a defensive cybersecurity assistant.

Analyze the security event using the supplied Sentinel-AI analysis.

Security event:
{event}

Sentinel-AI analysis:
{analysis}

Provide:

1. A short summary of what happened.
2. Why the event may be suspicious or risky.
3. The risk level based on the supplied analysis.
4. Recommended defensive actions.

Do not provide instructions for attacking systems,
bypassing security controls, stealing credentials,
or causing damage.

Keep the response concise and practical.
""".strip()


def assist(event: dict[str, Any]) -> dict[str, Any]:
    """Analyze a security event and generate an assistant response."""

    analysis = analyze(event)

    prompt = build_security_prompt(event, analysis)

    response = ask_llm(prompt)

    return {
        "event_id": event.get("id"),
        "analysis": analysis,
        "assistant_response": response,
    }