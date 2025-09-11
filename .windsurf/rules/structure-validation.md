---
trigger: glob
globs: businesses/*/
---

# BMDP Structure Validation Rule

Automatically validate BMDP directory structure and required files when businesses are created or modified.

## Validation Actions
- Ensure phase directories exist: `00_initiation`, `10_mobilize`, `20_understand`, `30_design`
- Validate required deliverable files are present per phase
- Check file naming conventions and structure compliance

## Actions
- Trigger: `python tools/workflow_validator.py --business {business_slug} --fix`