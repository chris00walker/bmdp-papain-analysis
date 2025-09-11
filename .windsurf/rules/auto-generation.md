---
trigger: glob
globs: businesses/*/
---

# Missing Deliverables Auto-Generation Rule

Automatically generate missing BMDP deliverables using Jinja2 templates when business directories or phase folders are created/modified.

## Generation Actions
- Detect missing phase deliverables for 00/10/20/30
- Auto-generate templated files with business-specific content
- Ensure 100% structural compliance across required deliverables

## Actions
- Trigger: `python tools/workflow_enforcer.py --business {business_slug} --auto-generate`