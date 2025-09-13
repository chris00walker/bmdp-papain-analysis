---
description: BMDP Phase 1 - Mobilize business model design process for a specific business
auto_execution_mode: 3
---

# Phase 1: Mobilize

Develops market-ready business model hypotheses, prepares customer research framework, and establishes validation methodology for Phase 2 customer discovery and market validation.

## Overview

The mobilization phase transforms business briefs into testable market hypotheses and prepares comprehensive research frameworks for customer discovery. This phase ensures Phase 2 has clear validation targets and methodologies.

## Usage

Run this workflow with a business parameter: grower, processor, distributor, or marketplace

## Prerequisites

- Business slug (grower, processor, distributor, marketplace)
- Business number (1, 2, 3, 4)
- Sponsor brief from `brief-{number}-{business}.md`
- Phase 0 initiation completed with all deliverables:
  - `businesses/$1/00_initiation/00_sponsor_brief.md`
  - `businesses/$1/00_initiation/01_project_charter.md`
  - `businesses/$1/00_initiation/02_resource_plan.md`
  - `businesses/$1/00_initiation/03_team_roster.csv`
  - `businesses/$1/00_initiation/04_access_matrix.csv`
  - `businesses/$1/00_initiation/05_sprint_plan.md`
  - `businesses/$1/00_initiation/06_readiness_assessment.md` (GO decision confirmed)
  - `businesses/$1/evidence_ledger.csv` initialized

## Steps

### 1. Parse business brief and set environment variables

```bash
# Parse business brief data and export environment variables
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env)

# Calculate budgets and timelines using modular tools
python tools/calculators/budget_calculator.py --business $1 --output-format env >> /tmp/budget_vars.env
source /tmp/budget_vars.env
```

### 2. Create Phase 1 brief

```bash
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/11_brief.md.j2 \
  --output businesses/$1/10_mobilize/11_brief.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/10_mobilize/11_brief.md
```

### 3. Develop Business Model Canvas v0 with testable hypotheses

```bash
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/12_market_ready_canvas.md.j2 \
  --output businesses/$1/10_mobilize/12_market_ready_canvas.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/10_mobilize/12_market_ready_canvas.md
```

### 4. Create Value Proposition Canvas and Customer Jobs Analysis (VPD)

```bash
# Generate enhanced Value Proposition Canvas with adaptive LLM prompts
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/value_proposition_canvas.md.j2 \
  --output businesses/$1/10_mobilize/value_proposition_canvas.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/10_mobilize/value_proposition_canvas.md

# Generate customer jobs analysis using VPD framework
python tools/generators/vpd_canvas_creator.py --business businesses/$1 --apply --focus customer_jobs

# Generate pain & gain mapping with business context
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/pain_gain_mapping.md.j2 \
  --output businesses/$1/10_mobilize/pain_gain_mapping.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/10_mobilize/pain_gain_mapping.md

# Generate customer interview targets from VPD analysis
python tools/validators/vpd_validator.py --business businesses/$1 --generate interview_targets
```

### 5. Develop multiple business model stories for validation

```bash
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/13_market_validation_stories.md.j2 \
  --output businesses/$1/10_mobilize/13_market_validation_stories.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/10_mobilize/13_market_validation_stories.md
```

### 6. Design customer validation microtests

```bash
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/14_microtests.json.j2 \
  --output businesses/$1/10_mobilize/14_microtests.json
```

### 7. Prepare Phase 2 research framework

```bash
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/15_phase2_research_charter.md.j2 \
  --output businesses/$1/10_mobilize/15_phase2_research_charter.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/10_mobilize/15_phase2_research_charter.md
```

### 8. Create risk assessment (Kill/Thrill analysis)

```bash
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/16_kill_thrill.csv.j2 \
  --output businesses/$1/10_mobilize/16_kill_thrill.csv
```

### 9. Establish validation metrics and success criteria

```bash
# Generate validation scorecard with enhanced adaptive framework
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/17_validation_scorecard.md.j2 \
  --output businesses/$1/10_mobilize/17_validation_scorecard.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/10_mobilize/17_validation_scorecard.md
```

### 10. Communications and stakeholder engagement

```bash
# Generate communications plan with enhanced adaptive framework
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/18_comms_plan.md.j2 \
  --output businesses/$1/10_mobilize/18_comms_plan.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/10_mobilize/18_comms_plan.md

# Generate announcement with enhanced adaptive framework
python tools/generators/render_template.py \
  --template deliverables/10_mobilize/19_announcement_onepager.md.j2 \
  --output businesses/$1/10_mobilize/19_announcement_onepager.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/10_mobilize/19_announcement_onepager.md
```

### 11. Update evidence ledger with market hypotheses

```bash
# Log market-focused evidence entries
echo "1,canvas_v0,hypothesis,canvas_workshop,$(date +%Y-%m-%d),high,Business model hypotheses defined for validation" >> businesses/$1/evidence_ledger.csv
echo "1,customer_jobs,hypothesis,vpd_analysis,$(date +%Y-%m-%d),high,Customer job hypotheses ready for testing" >> businesses/$1/evidence_ledger.csv
echo "1,value_prop_variants,hypothesis,story_workshop,$(date +%Y-%m-%d),medium,Multiple value proposition stories developed" >> businesses/$1/evidence_ledger.csv
echo "1,research_framework,methodology,research_design,$(date +%Y-%m-%d),high,Phase 2 customer research methodology prepared" >> businesses/$1/evidence_ledger.csv
```

## Deliverables

- [ ] `businesses/$1/10_mobilize/11_brief.md` - Phase 1 mobilization brief
- [ ] `businesses/$1/10_mobilize/12_market_ready_canvas.md` - Business Model Canvas v0 with testable hypotheses
- [ ] `businesses/$1/10_mobilize/12_canvas_assumptions.csv` - Canvas assumptions register for Phase 2 validation
- [ ] `businesses/$1/10_mobilize/13_market_validation_stories.md` - Multiple business model story variations
- [ ] `businesses/$1/10_mobilize/14_microtests.json` - Customer validation microtests
- [ ] `businesses/$1/10_mobilize/15_phase2_research_charter.md` - Phase 2 research framework and methodology
- [ ] `businesses/$1/10_mobilize/16_kill_thrill.csv` - Risk assessment and mitigation strategies
- [ ] Value Proposition Canvas with customer job hypotheses
- [ ] Customer segments and interview target profiles
- [ ] Competitive landscape hypotheses for investigation
- [ ] Validation scorecard and success metrics
- [ ] Stakeholder communication plan
- [ ] Evidence ledger updated with market hypotheses

## Gate Criteria

Proceed to Phase 2 only if:

- Canvas v0 contains specific, testable market hypotheses
- Customer job hypotheses ready for Phase 2 validation
- Multiple business model stories with validation criteria
- Phase 2 research methodology established
- Customer access strategy confirmed (15+ interview prospects)
- Competitive research framework defined
- Validation scorecard with measurable success criteria
- Evidence ledger updated with market-focused hypotheses
- ≥3 customer segments identified with interview targets
- ≥2 alternative business model stories developed
- ≥5 customer validation microtests defined
- Phase 2 research methodology and interview framework prepared
- Competitive research priorities identified
- Validation success criteria established
- ≥4 market hypothesis evidence entries logged