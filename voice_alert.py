import time
import requests
import pyttsx3

# ============================================================
# Sentinel AI Voice Alert
# Change ONLY this URL when your backend is finalized.
# Example:
# BACKEND_URL = "http://127.0.0.1:8000"
# ============================================================
BACKEND_URL = "http://127.0.0.1:8000"

ALERT_ENDPOINT = f"{BACKEND_URL}/alerts"
CHECK_INTERVAL = 3

# ------------------------------------------------------------
# Text-to-Speech setup
# ------------------------------------------------------------
engine = pyttsx3.init()

voices = engine.getProperty("voices")

# Microsoft Zira
if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)
else:
    engine.setProperty("voice", voices[0].id)

engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)


# ------------------------------------------------------------
# Speak an alert
# ------------------------------------------------------------
def speak_alert(message):
    print(f"[VOICE ALERT] {message}")
    engine.say(message)
    engine.runAndWait()


# ------------------------------------------------------------
# Check backend for HIGH / CRITICAL alerts
# ------------------------------------------------------------
def check_alerts(spoken_alerts):
    try:
        response = requests.get(
            ALERT_ENDPOINT,
            timeout=5
        )

        response.raise_for_status()

        alerts = response.json()

        if not isinstance(alerts, list):
            print("Unexpected response from backend.")
            return

        for alert in alerts:

            event_id = alert.get("event_id")
            risk_level = str(
                alert.get("risk_level", "")
            ).upper()

            process_name = alert.get(
                "process_name",
                "unknown process"
            )

            ai_summary = alert.get(
                "ai_summary",
                ""
            )

            # Prevent repeating the same alert
            if event_id in spoken_alerts:
                continue

            # Only speak HIGH and CRITICAL alerts
            if risk_level not in {"HIGH", "CRITICAL"}:
                continue

            # Remember that this event was already spoken
            spoken_alerts.add(event_id)

            if risk_level == "CRITICAL":

                message = (
                    f"Critical security alert. "
                    f"Potentially dangerous activity was detected "
                    f"in {process_name}."
                )

            else:

                message = (
                    f"Warning. High risk security activity "
                    f"was detected in {process_name}."
                )

            speak_alert(message)

            # Show the backend's AI explanation in terminal
            if ai_summary:
                print(f"[AI SUMMARY] {ai_summary}")

    except requests.exceptions.ConnectionError:
        print(
            f"[BACKEND OFFLINE] Cannot connect to {ALERT_ENDPOINT}"
        )

    except requests.exceptions.Timeout:
        print("[BACKEND TIMEOUT] Backend took too long to respond.")

    except requests.exceptions.HTTPError as error:
        print(f"[BACKEND HTTP ERROR] {error}")

    except ValueError:
        print("[BACKEND ERROR] Backend returned invalid JSON.")

    except Exception as error:
        print(f"[VOICE ERROR] {error}")


# ------------------------------------------------------------
# Main program
# ------------------------------------------------------------
def main():

    print("=" * 50)
    print("Sentinel AI Voice Alert Started")
    print(f"Monitoring: {ALERT_ENDPOINT}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print("=" * 50)

    # Stores event IDs that have already been spoken
    spoken_alerts = set()

    while True:

        check_alerts(spoken_alerts)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()