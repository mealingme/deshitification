"""Read-only exception triage for a fictional ecommerce order export."""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Iterable

FIELDS = ("order_id", "payment_status", "inventory_status", "dispatch_status",
          "promised_date", "dispatched_date")
PAYMENT_STATUSES = {"paid", "pending", "failed"}
INVENTORY_STATUSES = {"allocated", "unavailable", "pending"}
DISPATCH_STATUSES = {"not_dispatched", "dispatched", "cancelled"}
OUTPUT_FIELDS = ("order_id", "status", "reason", "as_of_date")


def _parse_iso_date(value: str, field: str, *, optional: bool = False) -> date | None:
    value = (value or "").strip()
    if optional and not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO date (YYYY-MM-DD)") from exc


def classify_order(row: dict[str, str], as_of: date,
                   duplicate_ids: set[str] | None = None) -> tuple[str, str]:
    """Return a deterministic status and explanation; never changes an order."""
    duplicate_ids = duplicate_ids or set()
    order_id = (row.get("order_id") or "").strip()
    if not order_id:
        return "DATA_ERROR", "Missing order_id"
    if order_id in duplicate_ids:
        return "DATA_ERROR", "Duplicate order_id in input"

    payment = (row.get("payment_status") or "").strip().lower()
    inventory = (row.get("inventory_status") or "").strip().lower()
    dispatch = (row.get("dispatch_status") or "").strip().lower()
    if payment not in PAYMENT_STATUSES:
        return "DATA_ERROR", "Unknown or missing payment_status"
    if inventory not in INVENTORY_STATUSES:
        return "DATA_ERROR", "Unknown or missing inventory_status"
    if dispatch not in DISPATCH_STATUSES:
        return "DATA_ERROR", "Unknown or missing dispatch_status"

    try:
        promised = _parse_iso_date(row.get("promised_date", ""), "promised_date")
        dispatched = _parse_iso_date(row.get("dispatched_date", ""),
                                     "dispatched_date", optional=True)
    except ValueError as exc:
        return "DATA_ERROR", str(exc)

    if dispatch == "dispatched" and dispatched is None:
        return "DATA_ERROR", "Dispatched order has no dispatched_date"
    if dispatch != "dispatched" and dispatched is not None:
        return "DATA_ERROR", "Only dispatched orders may have dispatched_date"

    if dispatch == "cancelled":
        return "CANCELLED", "Order is marked cancelled"
    if payment != "paid":
        return "HOLD", f"Payment status is {payment}; release requires paid status"
    if inventory != "allocated":
        return "HOLD", f"Inventory status is {inventory}; allocation is incomplete"
    if dispatch == "dispatched":
        if dispatched and dispatched > promised:
            return "LATE", "Dispatch date is after the promised date"
        return "COMPLETE_ON_TIME", "Dispatched on or before the promised date"
    if promised < as_of:
        return "OVERDUE", "Not dispatched and promised date has passed"
    return "ON_TRACK", "Not dispatched; promised date has not passed"


def triage_rows(rows: Iterable[dict[str, str]], as_of: date) -> list[dict[str, str]]:
    """Classify rows and flag every occurrence of a duplicate non-empty order ID."""
    materialised = list(rows)
    counts = Counter((row.get("order_id") or "").strip() for row in materialised)
    duplicates = {key for key, count in counts.items() if key and count > 1}
    results = []
    for row in materialised:
        status, reason = classify_order(row, as_of, duplicates)
        results.append({"order_id": (row.get("order_id") or "").strip(),
                         "status": status, "reason": reason,
                         "as_of_date": as_of.isoformat()})
    return results


def read_orders(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(FIELDS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing CSV columns: " + ", ".join(sorted(missing)))
        return list(reader)


def write_report(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path,
                        default=Path(__file__).with_name("sample_orders.csv"),
                        help="CSV order export (defaults to the included synthetic example)")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="Evaluation date in YYYY-MM-DD format (defaults to today)")
    parser.add_argument("--output", type=Path, help="Optional CSV report destination")
    args = parser.parse_args()
    try:
        results = triage_rows(read_orders(args.input), args.as_of)
    except (OSError, csv.Error, ValueError) as exc:
        parser.error(str(exc))
    for item in results:
        print(f'{item["order_id"] or "(missing ID)"}: {item["status"]} — {item["reason"]}')
    if args.output:
        write_report(args.output, results)
        print(f"\nReport written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
