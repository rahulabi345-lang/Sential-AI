import json
import os
import re
import urllib.request
import urllib.error
from typing import Any, Dict, List, Union


def _load_env_file():
    """Helper to read .env file if present and populate os.environ without requiring external packages."""
    env_paths = [
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    ]
    for env_path in env_paths:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, val = line.split("=", 1)
                            key = key.strip()
                            val = val.strip().strip("'\"")
                            if key and key not in os.environ:
                                os.environ[key] = val
            except Exception:
                pass


_load_env_file()


def _get_attr(obj: Union[Dict[str, Any], Any], key: str, default: Any = "") -> Any:
    """Helper to extract attribute or key value from dictionary or object safely."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def generate_fallback_analysis(
    event: Union[Dict[str, Any], Any],
    risk_score: int,
    risk_level: str,
    risk_reasons: List[str]
) -> Dict[str, Any]:
    """
    Generates a basic, safe, defensive explanation and recommendations
    directly from Risk Engine data when no AI provider API key is configured
    or when an external API call fails.
    """
    event_type = str(_get_attr(event, "event_type", "security_event")).lower()
    process_name = str(_get_attr(event, "process_name", "unknown_process"))
    severity = str(_get_attr(event, "severity", "medium")).lower()
    description = str(_get_attr(event, "description", "")).strip()
    hostname = str(_get_attr(event, "hostname", "unknown_host"))
    username = str(_get_attr(event, "username", "unknown_user"))

    # Title formatting
    formatted_type = event_type.replace("_", " ").title()
    title = f"{formatted_type} Analysis" if formatted_type else "Security Event Analysis"

    # Simple language summary
    if description:
        summary = f"{description} (Process: '{process_name}' on host '{hostname}')."
    else:
        summary = f"A process ('{process_name}') triggered a {severity} severity security event."

    # Explainable Risk Engine reason text
    reasons_str = ", ".join(risk_reasons) if risk_reasons else "standard security risk indicators"
    explanation = (
        f"The event received a {risk_level} risk rating (score: {risk_score}/100) "
        f"because it was flagged with severity '{severity}' and key risk factors: {reasons_str}."
    )

    # Gather relevant indicators from event
    indicators: List[str] = [
        f"{severity.title()} severity level",
        f"Event type: {event_type}",
        f"Process: {process_name}"
    ]
    if risk_reasons:
        indicators.extend(risk_reasons)
    
    # Deduplicate indicators preserving order
    seen = set()
    unique_indicators = []
    for ind in indicators:
        if ind not in seen:
            seen.add(ind)
            unique_indicators.append(ind)

    # Safe defensive recommendations
    recommended_actions: List[str] = [
        f"Verify whether the process '{process_name}' was intentionally started by user '{username}'.",
        f"Review related security events and system logs on host '{hostname}'."
    ]

    if risk_level in ["HIGH", "CRITICAL"]:
        recommended_actions.append("Investigate process arguments and parent execution hierarchy for unexpected behavior.")
        recommended_actions.append("Consider isolating or monitoring host traffic pending security investigation.")
    else:
        recommended_actions.append("Investigate further if the activity is unexpected or unauthorized.")

    # Calculate confidence based on available information completeness
    confidence = 85
    if not description or description == "":
        confidence = 65
        explanation += " Note: Information is limited due to an empty event description."

    return {
        "title": title,
        "summary": summary,
        "explanation": explanation,
        "indicators": unique_indicators,
        "recommended_actions": recommended_actions,
        "confidence": confidence
    }


def analyze_event(
    event: Union[Dict[str, Any], Any],
    risk_score: int,
    risk_level: str,
    risk_reasons: List[str]
) -> Dict[str, Any]:
    """
    Analyzes a security event using an AI Provider (Gemini / OpenAI / Custom REST) if configured.
    Falls back gracefully to rule-based fallback analysis if no API key is present or on API error.

    Returns structured dictionary:
    {
        "title": str,
        "summary": str,
        "explanation": str,
        "indicators": List[str],
        "recommended_actions": List[str],
        "confidence": int
    }
    """
    # 1. Check configured AI credentials
    api_key = (
        os.getenv("AI_API_KEY")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    provider = os.getenv("AI_PROVIDER", "gemini").lower()
    
    # If no key or provider disabled, use fallback immediately
    if not api_key or provider in ["none", "disabled", "false"]:
        return generate_fallback_analysis(event, risk_score, risk_level, risk_reasons)

    # 2. Extract event attributes
    event_dict = {
        "event_type": _get_attr(event, "event_type", ""),
        "source": _get_attr(event, "source", ""),
        "hostname": _get_attr(event, "hostname", ""),
        "username": _get_attr(event, "username", ""),
        "process_name": _get_attr(event, "process_name", ""),
        "process_id": _get_attr(event, "process_id", 0),
        "severity": _get_attr(event, "severity", ""),
        "description": _get_attr(event, "description", ""),
        "raw_data": _get_attr(event, "raw_data", {})
    }

    # 3. Construct defensive prompt
    system_prompt = (
        "You are Sentinel AI, an expert defensive security analyst. "
        "Your task is to analyze security events, explain risk scores, and provide defensive recommendations. "
        "CRITICAL RULES:\n"
        "1. Focus ONLY on defensive security, explainability, and incident triage.\n"
        "2. Do NOT generate offensive code, exploits, malware, persistence, or evasion techniques.\n"
        "3. State clearly if information is insufficient.\n"
        "4. Output MUST be strictly raw valid JSON (no markdown block wrapper) with key fields:\n"
        '{"title": str, "summary": str, "explanation": str, "indicators": [str], "recommended_actions": [str], "confidence": int}\n'
    )

    user_payload = {
        "event": event_dict,
        "risk_engine": {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_reasons": risk_reasons
        }
    }

    user_prompt = (
        f"Analyze the following security event and risk engine assessment:\n"
        f"{json.dumps(user_payload, indent=2)}\n\n"
        "Respond with a JSON object containing:\n"
        "- title: Concise title summarizing the event\n"
        "- summary: Simple 1-2 sentence explanation of what occurred\n"
        "- explanation: Explanation of why the Risk Engine assigned the risk score and level\n"
        "- indicators: List of key security indicators identified in the event\n"
        "- recommended_actions: List of safe, actionable defensive recommendations\n"
        "- confidence: Integer confidence score (0-100)\n"
    )

    # 4. Attempt API Call
    try:
        raw_response_text = ""

        if provider in ["gemini", "google"]:
            model = os.getenv("AI_MODEL", "gemini-1.5-flash")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            req_data = json.dumps({
                "contents": [
                    {"role": "user", "parts": [{"text": system_prompt + "\n\n" + user_prompt}]}
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "responseMimeType": "application/json"
                }
            }).encode("utf-8")
            
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                candidates = resp_json.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        raw_response_text = parts[0].get("text", "")

        elif provider in ["openai", "custom"]:
            model = os.getenv("AI_MODEL", "gpt-4o-mini")
            url = os.getenv("AI_API_URL", "https://api.openai.com/v1/chat/completions")
            req_data = json.dumps({
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"}
            }).encode("utf-8")
            
            req = urllib.request.Request(
                url,
                data=req_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                choices = resp_json.get("choices", [])
                if choices:
                    raw_response_text = choices[0].get("message", {}).get("content", "")

        if raw_response_text:
            # Clean markdown JSON fences if present
            cleaned_text = raw_response_text.strip()
            if cleaned_text.startswith("```"):
                cleaned_text = re.sub(r"^```[a-z]*\n?", "", cleaned_text)
                cleaned_text = re.sub(r"\n?```$", "", cleaned_text)
            
            parsed_data = json.loads(cleaned_text)

            # Ensure all required keys are present
            return {
                "title": str(parsed_data.get("title", "Security Event Analysis")),
                "summary": str(parsed_data.get("summary", "Security event evaluated.")),
                "explanation": str(parsed_data.get("explanation", "Evaluated based on risk rules.")),
                "indicators": list(parsed_data.get("indicators", [])),
                "recommended_actions": list(parsed_data.get("recommended_actions", [])),
                "confidence": int(parsed_data.get("confidence", 80))
            }

    except Exception:
        # On any network failure, timeout, or parsing error, fallback gracefully
        pass

    return generate_fallback_analysis(event, risk_score, risk_level, risk_reasons)
