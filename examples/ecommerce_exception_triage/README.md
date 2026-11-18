# Ecommerce Exception Triage

A small, read-only Python example that classifies a fictional ecommerce order export into a short exception queue.

## What it demonstrates

- Validates required status fields and ISO dates.
- Detects duplicate order IDs.
- Holds orders when payment is not marked paid or stock is not allocated.
- Flags unshipped orders whose promised date has passed.
- Distinguishes late dispatch from on-time completion.
- Produces a CSV report with a reason for each classification.

## Quick start

Requires Python 3.10+ and only the standard library.

\`\`\`bash
python examples/ecommerce_exception_triage/triage.py --as-of 2026-11-18
python examples/ecommerce_exception_triage/triage.py --as-of 2026-11-18 --output reports/ecommerce_exceptions.csv
python -m unittest discover -s tests -v
\`\`\`

The default input is the included synthetic CSV. Supply another CSV with the same six columns using \`--input\`.

## Classification rules

| Status | Meaning |
|---|---|
| \`DATA_ERROR\` | Missing/invalid fields, inconsistent dates or duplicate ID; correct the source before relying on the row |
| \`CANCELLED\` | Order is marked cancelled |
| \`HOLD\` | Payment is not paid or inventory is not allocated |
| \`LATE\` | Dispatched after the promised date |
| \`OVERDUE\` | Not dispatched and promised date has passed |
| \`COMPLETE_ON_TIME\` | Dispatched on or before the promised date |
| \`ON_TRACK\` | Not dispatched, but the promised date has not passed |

Rules are deliberately simple and ordered. A hold takes precedence over lateness because the example treats payment and stock as release gates. Real systems may need different rules, time zones, carrier events, partial shipments, returns, fraud checks and business calendars.

## Safety and limitations

This is a portfolio demonstration, not an order-management system. It reads a CSV and optionally writes a separate report. It does not connect to a shop, ERP, warehouse, carrier, payment provider or customer database; send messages; release stock; change order status; refund payments; or make fulfilment decisions.

All IDs and rows are fictional. Dates are illustrative. The script does not establish consumer-law, payment, fraud, delivery or service-level compliance. A human must verify each exception in the authoritative system before acting. Never commit real customer, employer, supplier or colleague data.
