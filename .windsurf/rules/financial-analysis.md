---
trigger: glob
globs: businesses/*/30_design/*.csv
---

# Financial Model Analysis Rule

Automatically recompute financial metrics and validate constraints when financial CSV data changes.

## Analysis Actions
- Recalculate IRR, NPV, ROI, and other viability metrics from cash flow data
- Validate capital bounds and financial constraints for the business
- Surface updated financial viability signals

## Actions
- Trigger: `python tools/compute_financials.py --business {business_slug} --auto-update`
- Trigger: `python tools/business_rule_engine.py --business {business_slug} --validate financials`