---
trigger: glob
globs: businesses/*/30_design/financials_*.csv
---

# Financial Constraints Validation Rule

Validate financial model constraints and BMG viability when financial CSVs are created or modified.

## Validation Actions
- Check capital bounds and financial constraints
- Validate BMG financial viability criteria
- Ensure revenue model coherence with canvas and manifest context

## Actions
- Trigger: `python tools/business_rule_engine.py --business {business_slug} --validate financials`