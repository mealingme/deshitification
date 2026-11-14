# Workflow Reliability Lab

A small Python portfolio example for a fictional ecommerce order-notification workflow. It uses synthetic CSV data only and has no live integrations.

## What it demonstrates
- Event and timestamp validation
- Duplicate event-ID detection
- Destination acknowledgement monitoring
- A configurable acknowledgement threshold
- Exception classification and CSV reporting
- Unit tests using Python's standard library

## Run it
From this folder, run:
python workflow_health_check.py

Optional:
python workflow_health_check.py --input sample_data/orders.csv --sla-minutes 15 --output findings.csv

The tests are included in the repository's root test suite and run through GitHub Actions.

## Safety and limitations
This is an educational, read-only demonstration, not production software, a formal audit or a delivery guarantee. It does not connect to ecommerce, email, ERP or warehouse systems; authenticate; send or modify orders; retry events; or prove downstream processing.

All example records are fictional. Do not add customer, supplier, employee or employer data, credentials, API keys, internal URLs or real logs. Any adaptation to a real system requires explicit system-owner approval, an authorised test environment, data-handling review and a rollback plan.

## Architecture
See docs/architecture.svg for the workflow diagram.

This project is part of the public mealingme/deshitification repository and is covered by its root MIT licence.
