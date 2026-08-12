import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.ai_analyzer import analyze_event, generate_fallback_analysis
from app.ai_analyzer import analyze_event, generate_fallback_analysis


class TestAIAnalyzer(unittest.TestCase):
    """Test suite for Sentinel AI Analyzer module."""

    def test_fallback_analyzer_structure(self):
        event = {
            "event_type": "suspicious_process",
            "process_name": "unknown.exe",
            "severity": "high",
            "description": "An unusual process was detected",
            "hostname": "host-01",
            "username": "admin_user"
        }
        risk_score = 72
        risk_level = "HIGH"
        risk_reasons = [
            "Event severity is high",
            "Suspicious activity indicator detected"
        ]

        analysis = generate_fallback_analysis(event, risk_score, risk_level, risk_reasons)

        self.assertIn("title", analysis)
        self.assertIn("summary", analysis)
        self.assertIn("explanation", analysis)
        self.assertIn("indicators", analysis)
        self.assertIn("recommended_actions", analysis)
        self.assertIn("confidence", analysis)

        self.assertIsInstance(analysis["title"], str)
        self.assertIsInstance(analysis["summary"], str)
        self.assertIsInstance(analysis["explanation"], str)
        self.assertIsInstance(analysis["indicators"], list)
        self.assertIsInstance(analysis["recommended_actions"], list)
        self.assertIsInstance(analysis["confidence"], int)

        self.assertTrue(0 <= analysis["confidence"] <= 100)
        self.assertGreater(len(analysis["indicators"]), 0)
        self.assertGreater(len(analysis["recommended_actions"]), 0)
        self.assertIn("HIGH", analysis["explanation"])

    def test_analyze_event_default_fallback(self):
        event = {
            "event_type": "failed_login",
            "process_name": "sshd",
            "severity": "medium",
            "description": "Multiple failed SSH authentication attempts",
            "hostname": "server-02",
            "username": "root"
        }
        analysis = analyze_event(
            event=event,
            risk_score=45,
            risk_level="MEDIUM",
            risk_reasons=["Contains failed or unauthorized activity indicator"]
        )

        self.assertIsNotNone(analysis.get("title"))
        self.assertIsNotNone(analysis.get("summary"))
        self.assertIsNotNone(analysis.get("explanation"))
        self.assertIsInstance(analysis.get("indicators"), list)
        self.assertIsInstance(analysis.get("recommended_actions"), list)
        self.assertIsInstance(analysis.get("confidence"), int)


if __name__ == "__main__":
    unittest.main()
