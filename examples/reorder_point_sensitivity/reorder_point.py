"""Read-only reorder-point calculator for fictional inventory data.

This is an educational planning aid, not a forecasting or purchasing system.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = {
    "sku",
    "average_daily_demand",
    "current_stock",
    "lead_time_days",
    "safety_stock_units",
    "unit_cost_eur",
}


def _number(row: dict[str, str], key: str, *, minimum: float = 0.0) -> float:
    try:
        value = float(row[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be a number") from exc
    if not math.isfinite(value) or value < minimum:
        raise ValueError(f"{key} must be finite and at least {minimum}")
    return value


def calculate_item(
    row: dict[str, str],
    *,
    demand_variation: float = 0.20,
    lead_time_variation: float = 0.25,
) -> dict[str, object]:
    """Calculate a base threshold and simple low/high sensitivity cases.

    Variations are fractions (0.20 means +/-20%). The stress cases combine
    demand and lead-time changes; they are scenarios, not probabilities.
    """
    missing = REQUIRED_COLUMNS.difference(row)
    if missing:
        raise ValueError("missing columns: " + ", ".join(sorted(missing)))

    sku = row["sku"].strip()
    if not sku:
        raise ValueError("sku must not be empty")

    demand = _number(row, "average_daily_demand", minimum=0.000001)
    stock = _number(row, "current_stock")
    lead_time = _number(row, "lead_time_days", minimum=0.000001)
    safety_stock = _number(row, "safety_stock_units")
    unit_cost = _number(row, "unit_cost_eur")

    for name, variation in (
        ("demand_variation", demand_variation),
        ("lead_time_variation", lead_time_variation),
    ):
        if not math.isfinite(variation) or not 0 <= variation <= 1:
            raise ValueError(f"{name} must be between 0 and 1")

    base = math.ceil(demand * lead_time + safety_stock)
    low = math.ceil(
        demand * (1 - demand_variation)
        * lead_time * (1 - lead_time_variation)
        + safety_stock
    )
    high = math.ceil(
        demand * (1 + demand_variation)
        * lead_time * (1 + lead_time_variation)
        + safety_stock
    )
    days_cover = stock / demand
    gap = max(0, base - stock)

    return {
        "sku": sku,
        "current_stock": round(stock, 2),
        "base_reorder_point": base,
        "low_case_reorder_point": low,
        "high_case_reorder_point": high,
        "days_cover": round(days_cover, 1),
        "units_to_base_threshold": round(gap, 2),
        "illustrative_threshold_value_eur": round(gap * unit_cost, 2),
        "decision": "REVIEW_REORDER" if stock <= base else "MONITOR",
    }


def read_items(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("input CSV must include a header row")
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames)
        if missing:
            raise ValueError("missing columns: " + ", ".join(sorted(missing)))
        rows = list(reader)
    if not rows:
        raise ValueError("input CSV contains no item rows")
    return rows


def write_results(rows: Iterable[dict[str, object]], path: Path) -> None:
    fields = [
        "sku",
        "current_stock",
        "base_reorder_point",
        "low_case_reorder_point",
        "high_case_reorder_point",
        "days_cover",
        "units_to_base_threshold",
        "illustrative_threshold_value_eur",
        "decision",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate illustrative reorder thresholds from a CSV."
    )
    parser.add_argument(
        "--input", type=Path,
        default=Path("examples/reorder_point_sensitivity/sample_items.csv"),
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path("reports/reorder_point_sensitivity.csv"),
    )
    parser.add_argument("--demand-variation", type=float, default=0.20)
    parser.add_argument("--lead-time-variation", type=float, default=0.25)
    args = parser.parse_args()

    try:
        items = read_items(args.input)
        results = [
            calculate_item(
                item,
                demand_variation=args.demand_variation,
                lead_time_variation=args.lead_time_variation,
            )
            for item in items
        ]
        write_results(results, args.output)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Processed {len(results)} fictional items; wrote {args.output}")
    print("Review flagged items before making any purchasing decision.")


if __name__ == "__main__":
    main()
