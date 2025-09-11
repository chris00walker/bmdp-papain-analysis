---
trigger: glob
globs: businesses/*/30_design/phase_completion.md
---

# Methodology Phase Gate Rule

Validate methodology compliance before allowing phase transitions (e.g., attempting to mark a phase as complete).

## Gate Validation
- Check VPD completion requirements (customer jobs, pain/gain mapping, VPD canvas)
- Validate BMG nine building blocks coherence and viability assessment
- Ensure TBI evidence quality standards and learning integration are met

## Actions
- Trigger: `python tools/workflow_checkpoint.py --business {business_slug} --phase {phase} --validate-gates`