#!/usr/bin/env python3
"""Inspect a synthetic order-notification event log.

Educational, read-only CSV example. It does not connect to live systems.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

ACCEPTED_PAYMENT_STATES = {"paid", "captured"}


@dataclass(frozen=True)
class Finding:
    event_id: str
    order_ref: str
    severity: str
    codes: tuple[str, ...]
    acknowledgement_minutes: float | None


def parse_bool(value: str) -> bool | None:
    normalised = (value or "").strip().lower()
    if normalised in {"true", "1", "yes", "y"}:
        return True
    if normalised in {"false", "0", "no", "n"}:
        return False
    return None


def parse_timestamp(value: str) -> datetime | None:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def inspect_rows(rows: Iterable[dict[str, str]], sla_minutes: float = 15.0) -> list[Finding]:
    """Return one finding record per input row."""
    seen_event_ids: set[str] = set()
    findings: list[Finding] = []

    for row in rows:
        event_id = (row.get("event_id") or "").strip()
        order_ref = (row.get("order_ref") or "").strip()
        codes: list[str] = []
        severities: list[str] = []
        latency: float | None = None

        if not event_id:
            codes.append("MISSING_EVENT_ID")
            severities.append("ERROR")
        elif event_id in seen_event_ids:
            codes.append("DUPLICATE_EVENT_ID")
            severities.append("ERROR")
        else:
            seen_event_ids.add(event_id)

        payment_state = (row.get("payment_status") or "").strip().lower()
        if payment_state not in ACCEPTED_PAYMENT_STATES:
            codes.append("UNSUPPORTED_PAYMENT_STATE")
            severities.append("WARNING")

        event_time = parse_timestamp(row.get("event_time", ""))
        if event_time is None:
            codes.append("INVALID_EVENT_TIMESTAMP")
            severities.append("ERROR")

        created = parse_bool(row.get("notification_created", ""))
        if created is False:
            codes.append("NOTIFICATION_NOT_CREATED")
            severities.append("ERROR")
        elif created is None:
            codes.append("NOTIFICATION_CREATED_UNKNOWN")
            severities.append("ERROR")

        acknowledged = parse_bool(row.get("ack_received", ""))
        if acknowledged is False:
            codes.append("DESTINATION_NOT_ACKNOWLEDGED")
            severities.append("ERROR")
        elif acknowledged is None:
            codes.append("ACKNOWLEDGEMENT_UNKNOWN")
            severities.append("ERROR")
        elif acknowledged is True:
            ack_time = parse_timestamp(row.get("ack_time", ""))
            if ack_time is None:
                codes.append("INVALID_ACK_TIMESTAMP")
                severities.append("ERROR")
            elif event_time is not None:
                if (event_time.tzinfo is None) != (ack_time.tzinfo is None):
                    codes.append("INCONSISTENT_TIMESTAMP_TIMEZONES")
                    severities.append("ERROR")
                else:
                    latency = (ack_time - event_time).total_seconds() / 60
                    if latency < 0:
                        codes.append("ACK_BEFORE_EVENT")
                        severities.append("ERROR")
                    elif latency > sla_minutes:
                        codes.append("ACK_OVER_SLA")
                        severities.append("WARNING")

        try:
            retry_count = int((row.get("retry_count") or "0").strip())
            if retry_count < 0:
                raise ValueError
            if retry_count > 0:
                codes.append("RETRIED")
                severities.append("INFO")
        except ValueError:
            codes.append("INVALID_RETRY_COUNT")
            severities.append("ERROR")

        severity = (
            "ERROR" if "ERROR" in severities
            else "WARNING" if "WARNING" in severities
            else "INFO" if "INFO" in severities
            else "OK"
        )
        findings.append(Finding(
            event_id=event_id or "(missing)",
            order_ref=order_ref or "(missing)",
            severity=severity,
            codes=tuple(codes or ["NO_EXCEPTION_DETECTED"]),
            acknowledgement_minutes=round(latency, 2) if latency is not None else None,
        ))

    return findings


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_findings(path: Path, findings: list[Finding]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["event_id", "order_ref", "severity", "codes", "acknowledgement_minutes"],
        )
        writer.writeheader()
        for item in findings:
            writer.writerow({
                "event_id": item.event_id,
                "order_ref": item.order_ref,
                "severity": item.severity,
                "codes": ";".join(item.codes),
                "acknowledgement_minutes": (
                    "" if item.acknowledgement_minutes is None
                    else item.acknowledgement_minutes
                ),
            })


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect a synthetic order-notification CSV.")
    parser.add_argument("--input", type=Path, default=Path("sample_data/orders.csv"))
    parser.add_argument("--sla-minutes", type=float, default=15.0)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    if args.sla_minutes < 0:
        parser.error("--sla-minutes must be zero or greater")
    if not args.input.is_file():
        parser.error(f"Input file not found: {args.input}")

    findings = inspect_rows(read_csv(args.input), args.sla_minutes)
    errors = sum(item.severity == "ERROR" for item in findings)
    warnings = sum(item.severity == "WARNING" for item in findings)
    clean = sum(item.severity == "OK" for item in findings)

    print("WORKFLOW RELIABILITY LAB — SYNTHETIC DATA")
    print(f"Rows inspected: {len(findings)}")
    print(f"Clean: {clean} | Warnings: {warnings} | Errors: {errors}")
    print("\nExceptions:")
    for item in findings:
        if item.severity != "OK":
            print(f"- {item.event_id} / {item.order_ref}: {item.severity} — {', '.join(item.codes)}")

    if args.output:
        write_findings(args.output, findings)
        print(f"\nFindings written to: {args.output}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
