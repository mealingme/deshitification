import sys
import unittest
from pathlib import Path

EXAMPLE_DIR = Path(__file__).resolve().parents[1] / "examples" / "ai_value_scorecard"
sys.path.insert(0, str(EXAMPLE_DIR))

from scorecard import calculate  # noqa: E402


BASE = {
    "monthly_volume": 200,
    "baseline_minutes_per_case": 8,
    "assisted_minutes_per_case": 5,
    "human_review_minutes_per_case": 1,
    "monthly_maintenance_hours": 2,
    "loaded_hourly_rate_eur": 30,
    "monthly_tool_cost_eur": 50,
    "monthly_other_cash_cost_eur": 10,
    "one_time_setup_cost_eur": 600,
    "setup_amortisation_months": 12,
    "measured_monthly_cash_savings_eur": 0,
}


class ScorecardTests(unittest.TestCase):
    def test_separates_capacity_value_from_cash_impact(self):
        result = calculate(BASE)
        self.assertEqual(result["net_capacity_hours_released"], 4.67)
        self.assertEqual(result["theoretical_capacity_value_eur"], 140.0)
        self.assertEqual(result["net_capacity_value_after_costs_eur"], 30.0)
        self.assertEqual(result["net_cash_impact_after_costs_eur"], -110.0)

    def test_review_time_is_included_in_assisted_work(self):
        result = calculate(dict(BASE, human_review_minutes_per_case=3))
        self.assertEqual(result["assisted_processing_hours_including_review"], 26.67)
        self.assertEqual(result["net_capacity_hours_released"], -2.0)

    def test_negative_capacity_is_reported_not_hidden(self):
        result = calculate(dict(BASE, assisted_minutes_per_case=10))
        self.assertLess(result["net_capacity_hours_released"], 0)

    def test_missing_required_field_is_rejected(self):
        data = dict(BASE)
        del data["monthly_volume"]
        with self.assertRaisesRegex(ValueError, "monthly_volume"):
            calculate(data)

    def test_negative_cost_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "monthly_tool_cost_eur"):
            calculate(dict(BASE, monthly_tool_cost_eur=-1))

    def test_cash_savings_default_to_zero(self):
        data = dict(BASE)
        del data["measured_monthly_cash_savings_eur"]
        result = calculate(data)
        self.assertEqual(result["measured_monthly_cash_savings_eur"], 0.0)
        self.assertIn("Only measured cash savings", result["interpretation"])


if __name__ == "__main__":
    unittest.main()
