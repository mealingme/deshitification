import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "examples" / "cold_chain_alert_monitor"),
)

from cold_chain_monitor import inspect_readings


def row(reading_id="r1", recorded_at="2026-11-15T08:00:00Z",
        temperature="-18", lower="-25", upper="-15", sensor="s1"):
    return {
        "reading_id": reading_id,
        "asset_id": "FREEZER-A",
        "sensor_id": sensor,
        "recorded_at": recorded_at,
        "temperature_c": temperature,
        "lower_limit_c": lower,
        "upper_limit_c": upper,
    }


class ColdChainMonitorTests(unittest.TestCase):
    def test_in_range_reading_is_ok(self):
        result = inspect_readings([row()])
        self.assertEqual(result[0].severity, "OK")

    def test_out_of_band_reading_is_warning(self):
        result = inspect_readings([row(temperature="-14")])
        self.assertEqual(result[0].severity, "WARNING")
        self.assertIn("TEMPERATURE_OUTSIDE_CONFIGURED_BAND", result[0].codes)

    def test_long_gap_is_warning_on_later_reading(self):
        result = inspect_readings([
            row("r1", "2026-11-15T08:00:00Z"),
            row("r2", "2026-11-15T08:25:00Z"),
        ], max_gap_minutes=15)
        self.assertEqual(result[1].severity, "WARNING")
        self.assertIn("READING_GAP_OVER_THRESHOLD", result[1].codes)
        self.assertEqual(result[1].gap_minutes, 25.0)

    def test_duplicate_reading_id_is_error(self):
        result = inspect_readings([
            row("same"),
            row("same", "2026-11-15T08:01:00Z"),
        ])
        self.assertEqual(result[1].severity, "ERROR")
        self.assertIn("DUPLICATE_READING_ID", result[1].codes)

    def test_timezone_naive_timestamp_is_error(self):
        result = inspect_readings([row(recorded_at="2026-11-15T08:00:00")])
        self.assertEqual(result[0].severity, "ERROR")
        self.assertIn("INVALID_TIMESTAMP", result[0].codes)

    def test_invalid_threshold_range_is_error(self):
        result = inspect_readings([row(lower="-15", upper="-25")])
        self.assertEqual(result[0].severity, "ERROR")
        self.assertIn("INVALID_LIMIT_RANGE", result[0].codes)

    def test_non_numeric_temperature_is_error(self):
        result = inspect_readings([row(temperature="unknown")])
        self.assertEqual(result[0].severity, "ERROR")
        self.assertIn("INVALID_TEMPERATURE", result[0].codes)

    def test_negative_gap_threshold_rejected(self):
        with self.assertRaises(ValueError):
            inspect_readings([row()], max_gap_minutes=-1)


if __name__ == "__main__":
    unittest.main()
