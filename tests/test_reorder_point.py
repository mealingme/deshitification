import csv
import tempfile
import unittest
from pathlib import Path

from examples.reorder_point_sensitivity.reorder_point import (
    calculate_item,
    read_items,
    write_results,
)


class ReorderPointTests(unittest.TestCase):
    def setUp(self):
        self.row = {
            "sku": "SYN-100",
            "average_daily_demand": "4",
            "current_stock": "30",
            "lead_time_days": "5",
            "safety_stock_units": "8",
            "unit_cost_eur": "12.50",
        }

    def test_base_reorder_point_and_decision(self):
        result = calculate_item(self.row)
        self.assertEqual(result["base_reorder_point"], 28)
        self.assertEqual(result["decision"], "MONITOR")
        self.assertEqual(result["units_to_base_threshold"], 0)

    def test_low_and_high_sensitivity_cases(self):
        result = calculate_item(self.row)
        self.assertEqual(result["low_case_reorder_point"], 20)
        self.assertEqual(result["high_case_reorder_point"], 38)

    def test_stock_at_threshold_is_flagged(self):
        row = {**self.row, "current_stock": "28"}
        self.assertEqual(calculate_item(row)["decision"], "REVIEW_REORDER")

    def test_gap_value_is_only_an_illustrative_threshold_gap(self):
        row = {**self.row, "current_stock": "20"}
        result = calculate_item(row)
        self.assertEqual(result["units_to_base_threshold"], 8)
        self.assertEqual(result["illustrative_threshold_value_eur"], 100.0)

    def test_rejects_zero_daily_demand(self):
        row = {**self.row, "average_daily_demand": "0"}
        with self.assertRaisesRegex(ValueError, "average_daily_demand"):
            calculate_item(row)

    def test_rejects_negative_stock(self):
        row = {**self.row, "current_stock": "-1"}
        with self.assertRaisesRegex(ValueError, "current_stock"):
            calculate_item(row)

    def test_rejects_variation_over_100_percent(self):
        with self.assertRaisesRegex(ValueError, "demand_variation"):
            calculate_item(self.row, demand_variation=1.1)

    def test_csv_read_and_write(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "items.csv"
            output = Path(folder) / "out.csv"
            source.write_text(
                "sku,average_daily_demand,current_stock,lead_time_days,"
                "safety_stock_units,unit_cost_eur\n"
                "SYN-100,4,20,5,8,12.50\n",
                encoding="utf-8",
            )
            result = calculate_item(read_items(source)[0])
            write_results([result], output)
            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["decision"], "REVIEW_REORDER")
            self.assertEqual(rows[0]["base_reorder_point"], "28")


if __name__ == "__main__":
    unittest.main()
