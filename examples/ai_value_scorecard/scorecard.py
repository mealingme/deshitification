"""Transparent monthly AI-workflow value calculator using synthetic or approved inputs."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def _number(data: dict[str, Any], key: str, *, default: float | None = None) -> float:
    if key not in data:
        if default is None:
            raise ValueError(f"Missing required field: {key}")
        value = default
    else:
        value = data[key]
    if isinstance(value, bool):
        raise ValueError(f"{key} must be a number, not a boolean")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be numeric") from exc
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{key} must be a finite, non-negative number")
    return number


def _positive_int(data: dict[str, Any], key: str) -> int:
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{key} must be a positive integer")
    return value


def calculate(data: dict[str, Any]) -> dict[str, Any]:
    """Calculate capacity value and cash impact without treating them as equivalent."""
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object")

    volume = _positive_int(data, "monthly_volume")
    baseline_minutes = _number(data, "baseline_minutes_per_case")
    if baseline_minutes <= 0:
        raise ValueError("baseline_minutes_per_case must be greater than zero")

    assisted_minutes = _number(data, "assisted_minutes_per_case")
    review_minutes = _number(data, "human_review_minutes_per_case")
    maintenance_hours = _number(data, "monthly_maintenance_hours")
    hourly_rate = _number(data, "loaded_hourly_rate_eur")
    tool_cost = _number(data, "monthly_tool_cost_eur")
    other_cost = _number(data, "monthly_other_cash_cost_eur", default=0)
    setup_cost = _number(data, "one_time_setup_cost_eur")
    amortisation_months = _positive_int(data, "setup_amortisation_months")
    measured_savings = _number(data, "measured_monthly_cash_savings_eur", default=0)

    baseline_hours = volume * baseline_minutes / 60
    assisted_hours = volume * (assisted_minutes + review_minutes) / 60
    net_capacity_hours = baseline_hours - assisted_hours - maintenance_hours
    capacity_value = net_capacity_hours * hourly_rate
    setup_amortisation = setup_cost / amortisation_months
    recurring_cash_cost = tool_cost + other_cost
    total_monthly_cost = recurring_cash_cost + setup_amortisation

    return {
        "monthly_volume": volume,
        "baseline_processing_hours": round(baseline_hours, 2),
        "assisted_processing_hours_including_review": round(assisted_hours, 2),
        "monthly_maintenance_hours": round(maintenance_hours, 2),
        "net_capacity_hours_released": round(net_capacity_hours, 2),
        "theoretical_capacity_value_eur": round(capacity_value, 2),
        "monthly_recurring_cash_cost_eur": round(recurring_cash_cost, 2),
        "setup_amortisation_per_month_eur": round(setup_amortisation, 2),
        "net_capacity_value_after_costs_eur": round(capacity_value - total_monthly_cost, 2),
        "measured_monthly_cash_savings_eur": round(measured_savings, 2),
        "net_cash_impact_after_costs_eur": round(measured_savings - total_monthly_cost, 2),
        "minimum_measured_cash_savings_for_break_even_eur": round(total_monthly_cost, 2),
        "interpretation": (
            "Negative capacity hours mean the assisted workflow adds work. "
            "Capacity value is theoretical, not a cash saving. Only measured "
            "cash savings are included in net cash impact."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).with_name("sample_workflow.json"),
        help="JSON input file (defaults to the included synthetic example)",
    )
    parser.add_argument("--output", type=Path, help="Optional path for a JSON report")
    args = parser.parse_args()

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        result = calculate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
