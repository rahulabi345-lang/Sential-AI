from typing import Any, Dict, List, Union


def calculate_risk(event: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
    """
    Rule-Based Risk Engine for Security Events.

    Calculates a transparent, explainable risk score (0-100), maps it to a risk level,
    and returns a list of human-readable reasons explaining why the score was assigned.

    Risk Levels:
        0 - 24   : LOW
        25 - 49  : MEDIUM
        50 - 74  : HIGH
        75 - 100 : CRITICAL
    """
    def get_attr(key: str, default: Any = "") -> Any:
        if isinstance(event, dict):
            return event.get(key, default)
        return getattr(event, key, default)

    severity = str(get_attr("severity", "")).lower()
    event_type = str(get_attr("event_type", "")).lower()
    process_name = str(get_attr("process_name", "")).lower()
    description = str(get_attr("description", "")).lower()
    raw_data = get_attr("raw_data", {}) or {}

    score = 0
    reasons: List[str] = []

    # 1. Base Score based on Severity
    if severity == "low":
        score += 10
        reasons.append("Event severity is low")
    elif severity == "medium":
        score += 35
        reasons.append("Event severity is medium")
    elif severity == "high":
        score += 55
        reasons.append("Event severity is high")
    elif severity == "critical":
        score += 80
        reasons.append("Event severity is critical")
    else:
        score += 0
        reasons.append("Event severity is informational or unspecified")

    # 2. Additional Indicator Rules
    combined_text = f"{event_type} {description}"

    # Suspicious indicator check
    if "suspicious" in combined_text:
        score += 15
        reasons.append("Event was classified as suspicious")

    # Failed or unauthorized access check
    unauthorized_keywords = ["failed", "unauthorized", "denied", "forbidden"]
    if any(keyword in combined_text for keyword in unauthorized_keywords):
        score += 10
        reasons.append("Contains failed or unauthorized activity indicator")

    # Administrative or privileged access check
    privilege_keywords = ["admin", "root", "privilege", "sudo"]
    if any(keyword in combined_text for keyword in privilege_keywords):
        score += 10
        reasons.append("Targeting administrative or privileged access")

    # Shell / command interpreter check
    shell_processes = ["cmd.exe", "powershell.exe", "bash", "sh", "zsh", "nc", "netcat"]
    if any(proc in process_name for proc in shell_processes) or "suspicious" in process_name:
        score += 10
        reasons.append("Executed process is a system command interpreter")

    # Raw metadata indicators
    if isinstance(raw_data, dict):
        failed_attempts = raw_data.get("failed_attempts", 0)
        if isinstance(failed_attempts, (int, float)) and failed_attempts > 3:
            score += 15
            reasons.append("Repeated failed attempts detected in metadata")
        if raw_data.get("suspicious") is True:
            score += 10
            reasons.append("Suspicious flag present in raw metadata")

    # 3. Clamp final score between 0 and 100
    risk_score = max(0, min(100, score))

    # 4. Determine Risk Level
    if risk_score <= 24:
        risk_level = "LOW"
    elif risk_score <= 49:
        risk_level = "MEDIUM"
    elif risk_score <= 74:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons
    }
