#!/usr/bin/env python3
"""Read-only inspection of a synthetic cold-chain temperature event log."""
from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

REQUIRED_FIELDS = {
    "reading_id", "asset_id", "sensor_id", "recorded_at",
    "temperature_c", "lower_limit_c", "upper_limit_c",
}


@dataclass(frozen=True)
class Finding:
    reading_id: str
    asset_id: str
    sensor_id: str
    severity: str
    codes: tuple[str, ...]
    temperature_c: float | None
    gap_minutes: float | None


def parse_timestamp(value: str) -> datetime | None:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    # Require an explicit offset rather than guessing local time.
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def parse_number(value: str) -> float | None:
    try:
        number = float((value or "").strip())
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def severity_for(codes: list[str]) -> str:
    error_codes = {
        "MISSING_REQUIRED_FIELD", "MISSING_READING_ID", "DUPLICATE_READING_ID",
        "INVALID_TIMESTAMP", "INVALID_TEMPERATURE", "INVALID_LIMIT",
        "INVALID_LIMIT_RANGE",
    }
    if any(code in error_codes for code in codes):
        return "ERROR"
    return "WARNING" if codes else "OK"


def inspect_readings(
    rows: Iterable[dict[str, str]],
    max_gap_minutes: float = 15.0,
) -> list[Finding]:
    if max_gap_minutes < 0:
        raise ValueError("max_gap_minutes must be zero or greater")

    parsed_rows: list[dict] = []
    seen_ids: set[str] = set()

    for row in rows:
        codes: list[str] = []
        reading_id = (row.get("reading_id") or "").strip()
        asset_id = (row.get("asset_id") or "").strip()
        sensor_id = (row.get("sensor_id") or "").strip()

        if any(not (row.get(field) or "").strip() for field in REQUIRED_FIELDS):
            codes.append("MISSING_REQUIRED_FIELD")

        if not reading_id:
            codes.append("MISSING_READING_ID")
        elif reading_id in seen_ids:
            codes.append("DUPLICATE_READING_ID")
        else:
            seen_ids.add(reading_id)

        timestamp = parse_timestamp(row.get("recorded_at", ""))
        if timestamp is None:
            codes.append("INVALID_TIMESTAMP")

        temperature = parse_number(row.get("temperature_c", ""))
        lower = parse_number(row.get("lower_limit_c", ""))
        upper = parse_number(row.get("upper_limit_c", ""))

        if temperature is None:
            codes.append("INVALID_TEMPERATURE")
        if lower is None or upper is None:
            codes.append("INVALID_LIMIT")
        elif lower >= upper:
            codes.append("INVALID_LIMIT_RANGE")

        if temperature is not None and lower is not None and upper is not None and lower < upper:
            if temperature < lower or temperature > upper:
                codes.append("TEMPERATURE_OUTSIDE_CONFIGURED_BAND")

        parsed_rows.append({
            "reading_id": reading_id,
            "asset_id": asset_id,
            "sensor_id": sensor_id,
            "timestamp": timestamp,
            "temperature": temperature,
            "codes": codes,
            "gap_minutes": None,
        })

    # Detect long intervals between valid consecutive readings per sensor.
    by_sensor: dict[str, list[dict]] = {}
    for item in parsed_rows:
        if item["timestamp"] is not None and item["sensor_id"]:
            by_sensor.setdefault(item["sensor_id"], []).append(item)

    for sensor_rows in by_sensor.values():
        sensor_rows.sort(key=lambda item: item["timestamp"])
        previous = None
        for item in sensor_rows:
            if previous is not None:
                gap = (item["timestamp"] - previous["timestamp"]).total_seconds() / 60
                item["gap_minutes"] = round(gap, 2)
                if gap > max_gap_minutes:
                    item["codes"].append("READING_GAP_OVER_THRESHOLD")
            previous = item

    findings: list[Finding] = []
    for item in parsed_rows:
        codes = item["codes"]
        findings.append(Finding(
            reading_id=item["reading_id"] or "(missing)",
            asset_id=item["asset_id"] or "(missing)",
            sensor_id=item["sensor_id"] or "(missing)",
            severity=severity_for(codes),
            codes=tuple(codes or ["NO_EXCEPTION_DETECTED"]),
            temperature_c=item["temperature"],
            gap_minutes=item["gap_minutes"],
        ))
    return findings


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_FIELDS.difference(reader.fieldnames or [])
        if missing:
            raise ValueError("CSV is missing required columns: " + ", ".join(sorted(missing)))
        return list(reader)


def write_report(path: Path, findings: list[Finding]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "reading_id", "asset_id", "sensor_id", "severity", "codes",
            "temperature_c", "gap_minutes",
        ])
        writer.writeheader()
        for item in findings:
            writer.writerow({
                "reading_id": item.reading_id,
                "asset_id": item.asset_id,
                "sensor_id": item.sensor_id,
                "severity": item.severity,
                "codes": ";".join(item.codes),
                "temperature_c": "" if item.temperature_c is None else item.temperature_c,
                "gap_minutes": "" if item.gap_minutes is None else item.gap_minutes,
            })


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect a synthetic cold-chain temperature CSV (read-only)."
    )
    parser.add_argument("--input", type=Path,
                        default=Path("examples/cold_chain_alert_monitor/sample_data/temperature_readings.csv"))
    parser.add_argument("--max-gap-minutes", type=float, default=15.0)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    if args.max_gap_minutes < 0:
        parser.error("--max-gap-minutes must be zero or greater")
    if not args.input.is_file():
        parser.error(f"Input file not found: {args.input}")

    try:
        findings = inspect_readings(read_csv(args.input), args.max_gap_minutes)
    except ValueError as exc:
        parser.error(str(exc))

    errors = sum(item.severity == "ERROR" for item in findings)
    warnings = sum(item.severity == "WARNING" for item in findings)
    clean = sum(item.severity == "OK" for item in findings)

    print("COLD-CHAIN ALERT MONITOR — SYNTHETIC DATA ONLY")
    print(f"Readings inspected: {len(findings)}")
    print(f"Clean: {clean} | Warnings: {warnings} | Errors: {errors}")
    print("\nExceptions:")
    for item in findings:
        if item.severity != "OK":
            print(f"- {item.reading_id} / {item.asset_id}: {item.severity} — {', '.join(item.codes)}")

    if args.output:
        write_report(args.output, findings)
        print(f"\nReport written to: {args.output}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
