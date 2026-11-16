# Cold-Chain Alert Monitor

A small, read-only Python demonstration for inspecting **synthetic** refrigeration temperature readings.

It checks whether readings are attributable to a sensor, whether temperatures fall outside supplied example limits, whether consecutive readings arrive within an expected interval, and whether exceptions can be exported for human review.

## Quick start

Requires Python 3.10 or later. No third-party packages or network access are required.

~~~bash
python examples/cold_chain_alert_monitor/cold_chain_monitor.py
python examples/cold_chain_alert_monitor/cold_chain_monitor.py --max-gap-minutes 15 --output findings.csv
python -m unittest discover -s tests -v
~~~

## Synthetic scenario

The sample file contains fictional assets and readings. Its thresholds and times are deliberately illustrative. It includes an out-of-range reading and a gap between readings.

The configured lower and upper limits are input data, **not recommended storage temperatures**. Real operating limits must come from the responsible product-safety authority, equipment owner and qualified operator.

## Checks

- Missing identifiers and required fields
- Duplicate reading IDs
- Invalid or timezone-naive timestamps
- Non-numeric or non-finite temperature/limit values
- Invalid threshold configuration
- Readings outside the supplied lower/upper limits
- Gaps between consecutive readings from the same sensor

A gap means only that the sample event log has no reading during that interval. It does not prove a sensor failure, a temperature excursion or a cyber incident.

## Severity

- **ERROR:** the row cannot be trusted or contains an invalid data/control condition.
- **WARNING:** the row is outside its supplied temperature band or follows a reading gap longer than the configured interval.
- **OK:** no exception was detected by these limited checks.

The script does not send alerts. It only prints a summary and optionally writes a CSV report.

## Safety and limitations

This is an educational demonstration, not a refrigeration controller, alarm service, food-safety assessment, OT security audit or production monitoring system.

It does not connect to sensors, controllers, BMS, SCADA, ERP or cloud services; read or change equipment settings; send notifications; determine whether food or medicines remain safe; establish the cause of missing readings or temperature changes; or replace validated monitoring and an incident-response plan.

Do not use the sample thresholds for real storage decisions. Do not disconnect, reboot or reconfigure industrial equipment based on this example. Real deployment requires system-owner approval, qualified OT support, validated thresholds, a tested alert path and an agreed fallback procedure.

## Privacy

All sample identifiers, assets and readings are fictional. Do not add employer, supplier, customer, employee or facility data to a public repository.

## Portfolio summary

**Cold-Chain Alert Monitor — Python / Supply Chain / Operational Resilience**

A synthetic-data, read-only example of temperature-band validation, sensor event-gap detection and exception reporting using Python's standard library.
