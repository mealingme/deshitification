import sys
import unittest
from datetime import date
from pathlib import Path

EXAMPLE_DIR = Path(__file__).resolve().parents[1] / "examples" / "ecommerce_exception_triage"
sys.path.insert(0, str(EXAMPLE_DIR))

from triage import classify_order, triage_rows  # noqa: E402

AS_OF = date(2026, 11, 18)


def order(**overrides):
    row = {"order_id": "DEMO-1", "payment_status": "paid",
           "inventory_status": "allocated", "dispatch_status": "not_dispatched",
           "promised_date": "2026-11-20", "dispatched_date": ""}
    row.update(overrides)
    return row


class EcommerceExceptionTriageTests(unittest.TestCase):
    def test_pending_payment_is_held(self):
        status, reason = classify_order(order(payment_status="pending"), AS_OF)
        self.assertEqual(status, "HOLD")
        self.assertIn("Payment", reason)

    def test_unallocated_inventory_is_held(self):
        status, reason = classify_order(order(inventory_status="unavailable"), AS_OF)
        self.assertEqual(status, "HOLD")
        self.assertIn("Inventory", reason)

    def test_unshipped_past_promise_is_overdue(self):
        status, _ = classify_order(order(promised_date="2026-11-17"), AS_OF)
        self.assertEqual(status, "OVERDUE")

    def test_late_dispatch_is_distinguished_from_on_time(self):
        late, _ = classify_order(order(dispatch_status="dispatched",
                                       dispatched_date="2026-11-19",
                                       promised_date="2026-11-17"), AS_OF)
        on_time, _ = classify_order(order(dispatch_status="dispatched",
                                          dispatched_date="2026-11-17",
                                          promised_date="2026-11-17"), AS_OF)
        self.assertEqual(late, "LATE")
        self.assertEqual(on_time, "COMPLETE_ON_TIME")

    def test_cancelled_order_is_not_treated_as_overdue(self):
        status, _ = classify_order(order(dispatch_status="cancelled",
                                         promised_date="2026-11-01"), AS_OF)
        self.assertEqual(status, "CANCELLED")

    def test_inconsistent_dispatch_date_is_data_error(self):
        status, reason = classify_order(order(dispatched_date="2026-11-17"), AS_OF)
        self.assertEqual(status, "DATA_ERROR")
        self.assertIn("Only dispatched", reason)

    def test_invalid_date_is_data_error(self):
        status, reason = classify_order(order(promised_date="18/11/2026"), AS_OF)
        self.assertEqual(status, "DATA_ERROR")
        self.assertIn("ISO date", reason)

    def test_every_duplicate_id_is_flagged(self):
        results = triage_rows([order(), order()], AS_OF)
        self.assertEqual([item["status"] for item in results],
                         ["DATA_ERROR", "DATA_ERROR"])


if __name__ == "__main__":
    unittest.main()
