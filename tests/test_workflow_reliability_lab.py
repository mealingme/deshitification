import sys
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1] / "examples" / "workflow_reliability_lab"
sys.path.insert(0, str(PROJECT))

from workflow_health_check import inspect_rows


class WorkflowReliabilityLabTests(unittest.TestCase):
    def test_clean_event(self):
        row = {
            "event_id": "evt-1", "order_ref": "ORD-1", "payment_status": "paid",
            "event_time": "2026-10-01T09:00:00Z", "notification_created": "true",
            "ack_received": "true", "ack_time": "2026-10-01T09:05:00Z", "retry_count": "0",
        }
        finding = inspect_rows([row], sla_minutes=15)[0]
        self.assertEqual(finding.severity, "OK")
        self.assertEqual(finding.acknowledgement_minutes, 5.0)

    def test_late_acknowledgement_is_warning(self):
        row = {
            "event_id": "evt-1", "order_ref": "ORD-1", "payment_status": "paid",
            "event_time": "2026-10-01T09:00:00Z", "notification_created": "true",
            "ack_received": "true", "ack_time": "2026-10-01T09:20:00Z", "retry_count": "0",
        }
        finding = inspect_rows([row], sla_minutes=15)[0]
        self.assertEqual(finding.severity, "WARNING")
        self.assertIn("ACK_OVER_SLA", finding.codes)

    def test_missing_acknowledgement_is_error(self):
        row = {
            "event_id": "evt-1", "order_ref": "ORD-1", "payment_status": "paid",
            "event_time": "2026-10-01T09:00:00Z", "notification_created": "true",
            "ack_received": "false", "ack_time": "", "retry_count": "0",
        }
        finding = inspect_rows([row])[0]
        self.assertEqual(finding.severity, "ERROR")
        self.assertIn("DESTINATION_NOT_ACKNOWLEDGED", finding.codes)

    def test_duplicate_event_id_is_detected(self):
        base = {
            "order_ref": "ORD-1", "payment_status": "paid",
            "event_time": "2026-10-01T09:00:00Z", "notification_created": "true",
            "ack_received": "true", "ack_time": "2026-10-01T09:01:00Z", "retry_count": "0",
        }
        rows = [
            {"event_id": "evt-1", **base},
            {"event_id": "evt-1", **{**base, "order_ref": "ORD-2"}},
        ]
        findings = inspect_rows(rows)
        self.assertIn("DUPLICATE_EVENT_ID", findings[1].codes)
        self.assertEqual(findings[1].severity, "ERROR")

    def test_invalid_timestamp_is_error(self):
        row = {
            "event_id": "evt-1", "order_ref": "ORD-1", "payment_status": "paid",
            "event_time": "not-a-date", "notification_created": "true",
            "ack_received": "false", "ack_time": "", "retry_count": "0",
        }
        finding = inspect_rows([row])[0]
        self.assertIn("INVALID_EVENT_TIMESTAMP", finding.codes)
        self.assertEqual(finding.severity, "ERROR")


if __name__ == "__main__":
    unittest.main()
