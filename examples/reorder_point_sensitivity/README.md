# Reorder-Point Sensitivity Lab

A read-only Python example showing how average daily demand, replenishment lead time and a manually supplied safety-stock allowance affect a simple reorder-point threshold.

All item codes and quantities are fictional.

## What it does

For each item, it calculates:

- **Base threshold:** average daily demand × lead-time days + safety-stock units, rounded up.
- **Low/high scenarios:** simple combined demand and lead-time variations (defaults: ±20% and ±25%).
- **Days of cover:** current stock divided by average daily demand.
- **Threshold gap:** units needed to reach the base threshold, if stock is below it.
- **Illustrative value:** threshold gap × unit cost. This is not a purchase order value or a recommendation to buy.

The stress scenarios are sensitivity checks, not probability estimates or statistical forecasts.

## Run

Requires Python 3.10+ and only the standard library.

```bash
python -m examples.reorder_point_sensitivity.reorder_point
python -m examples.reorder_point_sensitivity.reorder_point --demand-variation 0.30 --lead-time-variation 0.40
python -m unittest discover -s tests -v
```

The default output is `reports/reorder_point_sensitivity.csv`. Override `--input` or `--output` to use another CSV path.

## Assumptions and limitations

- Average demand and lead time are supplied by the user; this script does not forecast them.
- Safety stock is supplied by the user; it does not calculate safety stock from service levels or demand variability.
- The low/high cases multiply the demand and lead-time assumptions by fixed variation percentages. They do not model correlations, supplier calendars, minimum order quantities, pack sizes, review periods, seasonality or stock already on order.
- The threshold gap is not an order quantity. It excludes open purchase orders, reservations, backorders and economic order quantity.
- `REVIEW_REORDER` is a prompt for a human to inspect the item, not an automatic purchasing instruction.

This is an educational planning aid, not production inventory software, food-safety advice or a substitute for checking source data and operational constraints. It has no ERP connection, network access, write-back or purchasing capability.
