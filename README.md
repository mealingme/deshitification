# Deshitification — Practical Workflow Audit Starter

A small, transparent Python example for measuring a fictional order-fulfilment workflow before deciding whether to automate it.

**Purpose:** demonstrate practical process measurement, exception visibility and human-led improvement using synthetic data only.

## What it does
- Reads a CSV of fictional orders.
- Calculates order volume, on-time rate, average processing time and exception count.
- Lists delayed or unresolved orders for human review.
- Writes a JSON summary to `reports/workflow_summary.json`.

## Quick start
Requires Python 3.10+ and uses only the Python standard library.

```bash
python workflow_audit.py
```

## Safety and scope
- Educational demonstration only; not production software.
- No external services, API keys, network calls or customer data.
- No automatic changes to orders or business systems.
- Human review is required before operational decisions.

All sample records are synthetic. Never commit employer, client, supplier, colleague or customer data.

## Project structure
```text
workflow_audit.py
examples/sample_orders.csv
docs/automation-readiness-checklist.md
docs/safe-demo-guidelines.md
tests/test_workflow_audit.py
.github/workflows/tests.yml
```

MIT licence — see [LICENSE](LICENSE).
