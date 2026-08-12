import unittest
from datetime import datetime
from app.risk_engine import calculate_risk


class TestRiskEngine(unittest.TestCase):
    """Test suite for the Sentinel AI Rule-Based Risk Engine."""

    def test_low_severity_event(self):
        event = {
            "severity": "low",
            "event_type": "user_login",
            "process_name": "explorer.exe",
            "description": "User logged in normally"
        }
        res = calculate_risk(event)
        self.assertEqual(res["risk_level"], "LOW")
        self.assertTrue(0 <= res["risk_score"] <= 24)
        self.assertIn("Event severity is low", res["reasons"])

    def test_medium_severity_event(self):
        event = {
            "severity": "medium",
            "event_type": "file_access",
            "process_name": "notepad.exe",
            "description": "Sensitive config file opened"
        }
        res = calculate_risk(event)
        self.assertEqual(res["risk_level"], "MEDIUM")
        self.assertTrue(25 <= res["risk_score"] <= 49)
        self.assertIn("Event severity is medium", res["reasons"])

    def test_high_severity_event(self):
        event = {
            "severity": "high",
            "event_type": "system_modification",
            "process_name": "notepad.exe",
            "description": "Suspicious system change attempted"
        }
        res = calculate_risk(event)
        self.assertEqual(res["risk_score"], 70)
        self.assertEqual(res["risk_level"], "HIGH")
        self.assertIn("Event severity is high", res["reasons"])
        self.assertIn("Event was classified as suspicious", res["reasons"])

    def test_critical_severity_event(self):
        event = {
            "severity": "critical",
            "event_type": "unauthorized_access",
            "process_name": "powershell.exe",
            "description": "Root admin privilege escalation failed"
        }
        res = calculate_risk(event)
        self.assertEqual(res["risk_level"], "CRITICAL")
        self.assertTrue(75 <= res["risk_score"] <= 100)
        self.assertIn("Event severity is critical", res["reasons"])

    def test_score_bounds_clamping(self):
        # Scenario with zero indicators
        event_low_bound = {
            "severity": "info",
            "event_type": "system_info",
            "process_name": "sys.exe",
            "description": "System check"
        }
        res_low = calculate_risk(event_low_bound)
        self.assertGreaterEqual(res_low["risk_score"], 0)

        # Scenario triggering many additive score rules exceeding 100
        event_high_bound = {
            "severity": "critical",
            "event_type": "suspicious_failed_login",
            "process_name": "powershell.exe",
            "description": "Suspicious admin privilege escalation attempt with failed credentials",
            "raw_data": {"failed_attempts": 10, "suspicious": True}
        }
        res_high = calculate_risk(event_high_bound)
        self.assertEqual(res_high["risk_score"], 100)
        self.assertEqual(res_high["risk_level"], "CRITICAL")
        self.assertTrue(len(res_high["reasons"]) > 1)


if __name__ == "__main__":
    unittest.main()
