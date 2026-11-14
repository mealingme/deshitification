#!/usr/bin/env python3
"""Measure a fictional order workflow using synthetic CSV data."""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime
from pathlib import Path
from statistics import mean

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
VALID_STATUSES = {"completed", "in_progress", "blocked"}

def parse_time(value: str, field: str, row_number: int):
    if not value.strip(): return None
    try: return datetime.strptime(value.strip(), TIME_FORMAT)
    except ValueError as exc:
        raise ValueError(f"Row {row_number}: invalid {field} timestamp {value!r}; expected YYYY-MM-DDTHH:MM:SS") from exc

def load_orders(path: Path) -> list[dict]:
    required = {"order_id", "created_at", "completed_at", "due_at", "status", "exception"}
    orders=[]
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader=csv.DictReader(handle)
        missing=required-set(reader.fieldnames or [])
        if missing: raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
        for row_number,row in enumerate(reader,start=2):
            status=row["status"].strip().lower()
            if status not in VALID_STATUSES: raise ValueError(f"Row {row_number}: status must be one of {sorted(VALID_STATUSES)}")
            created=parse_time(row["created_at"],"created_at",row_number)
            due=parse_time(row["due_at"],"due_at",row_number)
            completed=parse_time(row["completed_at"],"completed_at",row_number)
            if created is None or due is None: raise ValueError(f"Row {row_number}: created_at and due_at are required")
            if completed and completed < created: raise ValueError(f"Row {row_number}: completed_at precedes created_at")
            orders.append({"order_id":row["order_id"].strip(),"created_at":created,"completed_at":completed,"due_at":due,"status":status,"exception":row["exception"].strip()})
    return orders

def build_summary(orders: list[dict]) -> dict:
    completed=[o for o in orders if o["status"]=="completed" and o["completed_at"]]
    on_time=[o for o in completed if o["completed_at"]<=o["due_at"]]
    durations=[(o["completed_at"]-o["created_at"]).total_seconds()/3600 for o in completed]
    exceptions=[o for o in orders if o["exception"]]
    unresolved=[o for o in orders if o["status"]!="completed"]
    late=[o for o in completed if o["completed_at"]>o["due_at"]]
    return {"record_count":len(orders),"completed_count":len(completed),"unresolved_count":len(unresolved),"on_time_count":len(on_time),"on_time_rate_percent":round(len(on_time)/len(completed)*100,1) if completed else None,"average_processing_hours":round(mean(durations),2) if durations else None,"exception_count":len(exceptions),"late_completed_count":len(late),"human_review_queue":[{"order_id":o["order_id"],"status":o["status"],"exception":o["exception"] or "none recorded","reason":"unresolved" if o["status"]!="completed" else "completed after due time"} for o in (unresolved+late)],"limitations":["Metrics depend on accurate timestamps and status values.","Unresolved orders are not counted in the on-time-rate denominator.","A recorded exception is not necessarily a process failure.","This report does not recommend or trigger automation."]}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,default=Path("examples/sample_orders.csv"),help="Path to the order CSV")
    parser.add_argument("--output",type=Path,default=Path("reports/workflow_summary.json"),help="Path for the JSON report")
    args=parser.parse_args()
    try:
        orders=load_orders(args.input); summary=build_summary(orders)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(summary,indent=2),encoding="utf-8")
    except (OSError,ValueError) as exc: parser.error(str(exc))
    print(f"Analysed {summary['record_count']} synthetic orders.")
    print(f"On-time rate: {summary['on_time_rate_percent']}%")
    print(f"Human review queue: {len(summary['human_review_queue'])}")
    print(f"Report written to: {args.output}")
    return 0

if __name__=="__main__": raise SystemExit(main())
