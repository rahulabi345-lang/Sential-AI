"""Local LLM integration using Ollama."""

from typing import Any

import ollama

MODEL = "llama3.2"


def ask_llm(prompt: str) -> str:
    """Send a prompt to the local Ollama model."""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]


def analyze_with_llm(event: dict[str, Any]) -> str:
    """Ask the local LLM to analyze a security event."""

    prompt = f"""
You are a defensive cybersecurity analyst.

Analyze the following security event.

Event:
{event}

Provide:

1. What happened
2. Why it may be suspicious
3. Potential risk
4. Recommended defensive actions

Do not provide instructions for attacking systems.
"""

    return ask_llm(prompt)