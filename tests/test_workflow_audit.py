import tempfile
import unittest
from pathlib import Path

from workflow_audit import build_summary, load_orders


class WorkflowAuditTests(unittest.TestCase):
    def test_sample_data_metrics(self):
        summary = build_summary(load_orders(Path("examples/sample_orders.csv")))
        self.assertEqual(summary["record_count"], 15)
        self.assertEqual(summary["completed_count"], 11)
        self.assertEqual(summary["unresolved_count"], 4)
        self.assertEqual(summary["on_time_count"], 7)
        self.assertEqual(summary["exception_count"], 7)
        self.assertEqual(summary["late_completed_count"], 4)
        self.assertEqual(len(summary["human_review_queue"]), 8)

    def test_rejects_invalid_status(self):
        content = (
            "order_id,created_at,completed_at,due_at,status,exception\n"
            "X1,2026-01-01T09:00:00,,2026-01-01T10:00:00,unknown,\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.csv"
            path.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "status must be"):
                load_orders(path)

    def test_rejects_completion_before_creation(self):
        content = (
            "order_id,created_at,completed_at,due_at,status,exception\n"
            "X1,2026-01-01T10:00:00,2026-01-01T09:00:00,"
            "2026-01-01T11:00:00,completed,\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.csv"
            path.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "precedes created_at"):
                load_orders(path)


if __name__ == "__main__":
    unittest.main()
