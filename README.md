# Deshitification — Practical Workflow Improvement & AI Education

A collection of practical educational material and small, transparent tools for understanding workflows, measuring automation reliability and applying AI responsibly.

**Purpose:** explain how to fix, simplify, automate and secure business processes using evidence-led methods and synthetic examples.

## Repository map
- `articles/educational/` — evergreen guides and practical explainers, one Markdown file per article.
- `articles/current-affairs/YYYY/` — time-sensitive technology and AI analysis, grouped by year.
- `articles/templates/` — reusable article structure and editorial conventions.
- `diagrams/` — original diagram source files and exports, grouped by topic.
- `workflow_audit.py` — simple synthetic order-fulfilment workflow audit.
- `examples/` — synthetic workflow examples, including the Workflow Reliability Lab.
- `docs/` — checklists and safe-demonstration guidance.
- `tests/` and `.github/workflows/` — automated tests and CI.
- `reports/` — local/generated reports; do not commit real operational data.

See [the article library guide](articles/README.md) for article organisation and status conventions.

## What the workflow audit demonstrates
- Reads fictional CSV data.
- Calculates order volume, on-time rate, average processing time and exception count.
- Lists delayed or unresolved orders for human review.
- Writes a JSON summary to `reports/workflow_summary.json`.

## Quick start
Requires Python 3.10+ and uses only the Python standard library.

```bash
python workflow_audit.py
python -m unittest discover -s tests -v
```

## Additional example: Cold-Chain Alert Monitor

See [Cold-Chain Alert Monitor](examples/cold_chain_alert_monitor/README.md). It inspects fictional temperature readings, flags values outside supplied example limits, detects gaps between sensor events and exports a human-review CSV. It is read-only and has no live equipment connection. The configured thresholds are illustrative, not food-safety guidance.

## Additional example: Workflow Reliability Lab
See [Workflow Reliability Lab](examples/workflow_reliability_lab/README.md). It demonstrates event validation, duplicate detection, destination acknowledgement monitoring and exception reporting for a fictional order-notification workflow. It includes synthetic CSV fixtures, an architecture diagram and unit tests.

## Safety and scope
- Educational demonstrations only; not production software.
- No external services, API keys, network calls or customer data.
- No automatic changes to orders or business systems.
- Human review is required before operational decisions.
- All sample records are synthetic. Never commit employer, client, supplier, colleague or customer data.

## Article workflow
WordPress is the public publishing source of truth. Markdown files in this repository are version-controlled editorial snapshots. Keep the WordPress post ID, status and canonical URL in front matter, and update the snapshot when the article changes. A Git commit does not publish a WordPress post.

MIT licence — see [LICENSE](LICENSE).

## Additional example: AI Workflow Value Scorecard

See [AI Workflow Value Scorecard](examples/ai_value_scorecard/README.md). This dependency-free calculator keeps theoretical staff-capacity value separate from measured cash savings, includes human review and maintenance time, and deducts recurring costs plus setup-cost amortisation. The sample data is fictional. An original [calculation-flow diagram](examples/ai_value_scorecard/scorecard_flow.svg) explains the two value views.

## Additional example: Ecommerce Exception Triage

See [Ecommerce Exception Triage](examples/ecommerce_exception_triage/README.md). It validates a fictional order export, detects duplicate IDs, classifies payment and inventory holds, and separates overdue orders from late and on-time dispatches. It writes a human-review CSV and never changes an order or sends a message. An original [triage-flow diagram](examples/ecommerce_exception_triage/triage_flow.svg) shows the read-only design.

## Additional example: Reorder-Point Sensitivity Lab

See [Reorder-Point Sensitivity Lab](examples/reorder_point_sensitivity/README.md). It calculates a transparent reorder threshold from fictional daily demand, lead time and manually supplied safety stock, then compares simple low/high sensitivity scenarios. It is read-only, uses only the Python standard library and leaves all purchasing decisions to a human reviewer.
