---
trigger: glob
globs: businesses/*/{10_mobilize,20_understand,30_design}/*.md
---

# VPD Methodology Compliance Rule

Continuously validate Value Proposition Design (VPD) methodology compliance when relevant content changes.

## Validation Actions
- Validate customer jobs analysis (functional, emotional, social)
- Check pain/gain mapping and VPD classification
- Ensure Value Proposition Canvas coherence and completeness

## Actions
- Trigger: `python tools/vpd_validator.py --business {business_slug} --validate all`