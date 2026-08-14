import unittest
import json
import urllib.request
import urllib.error


class TestEventsAPI(unittest.TestCase):
    """Integration test hitting the running Sentinel AI FastAPI server."""

    BASE_URL = "http://127.0.0.1:8001"

    def test_post_and_get_event_risk_integration(self):
        payload = {
            "timestamp": "2026-08-11T12:00:00Z",
            "event_type": "suspicious_access",
            "source": "host_agent",
            "hostname": "workstation-01",
            "username": "alice",
            "process_name": "powershell.exe",
            "process_id": 4096,
            "severity": "high",
            "description": "Suspicious powershell execution attempted",
            "raw_data": {"failed_attempts": 4}
        }

        # 1. POST /events
        req = urllib.request.Request(
            f"{self.BASE_URL}/events",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 201)
            data = json.loads(resp.read().decode("utf-8"))

        self.assertIn("id", data)
        self.assertIn("risk_score", data)
        self.assertIn("risk_level", data)
        self.assertIn("risk_reasons", data)

        self.assertEqual(data["risk_level"], "CRITICAL")
        self.assertEqual(data["risk_score"], 95)
        self.assertIsInstance(data["risk_reasons"], list)
        self.assertGreater(len(data["risk_reasons"]), 0)

        created_id = data["id"]

        # 2. GET /events/{event_id}
        with urllib.request.urlopen(f"{self.BASE_URL}/events/{created_id}") as resp:
            self.assertEqual(resp.status, 200)
            get_data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(get_data["id"], created_id)
            self.assertEqual(get_data["risk_score"], data["risk_score"])
            self.assertEqual(get_data["risk_level"], data["risk_level"])
            self.assertEqual(get_data["risk_reasons"], data["risk_reasons"])

        # 3. GET /events
        with urllib.request.urlopen(f"{self.BASE_URL}/events") as resp:
            self.assertEqual(resp.status, 200)
            list_data = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(any(e["id"] == created_id for e in list_data))

        # 4. POST /analyze with body payload
        analyze_req = urllib.request.Request(
            f"{self.BASE_URL}/analyze",
            data=json.dumps({"event_id": created_id}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(analyze_req) as resp:
            self.assertEqual(resp.status, 200)
            analysis_data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("title", analysis_data)
            self.assertIn("summary", analysis_data)
            self.assertIn("explanation", analysis_data)
            self.assertIn("indicators", analysis_data)
            self.assertIn("recommended_actions", analysis_data)
            self.assertIn("confidence", analysis_data)

        # 5. Verify AI fields stored in GET /events/{event_id}
        with urllib.request.urlopen(f"{self.BASE_URL}/events/{created_id}") as resp:
            self.assertEqual(resp.status, 200)
            updated_event = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(updated_event["ai_title"], analysis_data["title"])
            self.assertEqual(updated_event["ai_summary"], analysis_data["summary"])
            self.assertEqual(updated_event["ai_explanation"], analysis_data["explanation"])

        # 6. GET /alerts (should include created CRITICAL event)
        with urllib.request.urlopen(f"{self.BASE_URL}/alerts") as resp:
            self.assertEqual(resp.status, 200)
            alerts_data = json.loads(resp.read().decode("utf-8"))
            self.assertIsInstance(alerts_data, list)
            target_alert = next((a for a in alerts_data if a["event_id"] == created_id), None)
            self.assertIsNotNone(target_alert)
            self.assertEqual(target_alert["event_id"], created_id)
            self.assertEqual(target_alert["event_type"], payload["event_type"])
            self.assertEqual(target_alert["process_name"], payload["process_name"])
            self.assertEqual(target_alert["risk_level"], "CRITICAL")
            self.assertIn("ai_summary", target_alert)
            self.assertIn("recommended_actions", target_alert)
            self.assertEqual(target_alert["ai_summary"], analysis_data["summary"])

        # 7. GET /alerts?risk_level=CRITICAL
        with urllib.request.urlopen(f"{self.BASE_URL}/alerts?risk_level=CRITICAL") as resp:
            self.assertEqual(resp.status, 200)
            critical_alerts = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(all(a["risk_level"] == "CRITICAL" for a in critical_alerts))
            self.assertTrue(any(a["event_id"] == created_id for a in critical_alerts))

        # 8. GET /alerts?risk_level=HIGH
        with urllib.request.urlopen(f"{self.BASE_URL}/alerts?risk_level=HIGH") as resp:
            self.assertEqual(resp.status, 200)
            high_alerts = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(all(a["risk_level"] == "HIGH" for a in high_alerts))

        # 9. GET /stats
        with urllib.request.urlopen(f"{self.BASE_URL}/stats") as resp:
            self.assertEqual(resp.status, 200)
            stats_data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("total_events", stats_data)
            self.assertIn("low", stats_data)
            self.assertIn("medium", stats_data)
            self.assertIn("high", stats_data)
            self.assertIn("critical", stats_data)
            self.assertIn("total_alerts", stats_data)
            self.assertIn("latest_event_timestamp", stats_data)
            self.assertGreater(stats_data["total_events"], 0)
            self.assertEqual(stats_data["total_alerts"], stats_data["high"] + stats_data["critical"])
            self.assertIsNotNone(stats_data["latest_event_timestamp"])

        # 10. GET /health
        with urllib.request.urlopen(f"{self.BASE_URL}/health") as resp:
            self.assertEqual(resp.status, 200)
            health_data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(health_data["status"], "healthy")
            self.assertEqual(health_data["database"], "connected")

        # 11. GET /events/999999 (Non-existent event ID -> HTTP 404)
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(f"{self.BASE_URL}/events/999999")
        self.assertEqual(ctx.exception.code, 404)

        # 12. Invalid payload POST /events -> HTTP 422
        bad_req = urllib.request.Request(
            f"{self.BASE_URL}/events",
            data=json.dumps({"invalid_field": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(bad_req)
        self.assertEqual(ctx.exception.code, 422)

        # 13. CORS Preflight test
        cors_req = urllib.request.Request(
            f"{self.BASE_URL}/events",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
            method="OPTIONS"
        )
        with urllib.request.urlopen(cors_req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.headers.get("Access-Control-Allow-Origin"), "http://localhost:5173")


if __name__ == "__main__":
    unittest.main()
