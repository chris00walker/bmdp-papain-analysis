---
trigger: glob
globs: businesses/**/*.md
---

# Continuous Quality Analysis Rule

Automatically update quality and methodology compliance signals when content changes.

## Analysis Actions
- Recompute content quality and methodology checks (VPD/BMG/TBI heuristics)
- Surface updated quality status for the current business
- Keep analysis lightweight to avoid IDE impact

## Actions
- Trigger: `python tools/content_validator.py --business {business_slug} --analysis semantic --mode all --format summary`
- Trigger: `python tools/quality_scorer.py --business {business_slug} --format summary`