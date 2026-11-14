# Deshitification — Practical Workflow Audit Starter

A small, transparent Python example for measuring a fictional order-fulfilment workflow before deciding whether to automate it.

**Purpose:** demonstrate practical process measurement, exception visibility and human-led improvement using synthetic data only.

## What it does
- Reads a CSV of fictional orders.
- Calculates order volume, on-time rate, average processing time and exception count.
- Lists delayed or unresolved orders for human review.
- Writes a JSON summary to reports/workflow_summary.json.

## Quick start
Requires Python 3.10+ and uses only the Python standard library.

python workflow_audit.py

## Additional example: Workflow Reliability Lab
See the new [Workflow Reliability Lab](examples/workflow_reliability_lab/README.md). It demonstrates event validation, duplicate detection, destination acknowledgement monitoring and exception reporting for a fictional order-notification workflow. It includes synthetic CSV fixtures, an architecture diagram and five unit tests.

## Safety and scope
- Educational demonstrations only; not production software.
- No external services, API keys, network calls or customer data.
- No automatic changes to orders or business systems.
- Human review is required before operational decisions.

All sample records are synthetic. Never commit employer, client, supplier, colleague or customer data.

## Project structure
workflow_audit.py
examples/sample_orders.csv
examples/workflow_reliability_lab/
docs/automation-readiness-checklist.md
docs/safe-demo-guidelines.md
tests/
.github/workflows/tests.yml

MIT licence — see LICENSE.
