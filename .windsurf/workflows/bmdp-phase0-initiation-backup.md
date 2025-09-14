---
description: Establishes project legitimacy, confirms sponsor commitment, defines initial scope and constraints, and sets up governance structure. Gateway to formal BMDP execution.
auto_execution_mode: 3
---

# Phase 0: Initiation

## Overview

The initiation phase validates project readiness and establishes the foundation for the Business Model Design Process. This phase ensures we have proper sponsorship, clear objectives, and organizational commitment before proceeding to mobilization.

## Usage

Run this workflow with a business parameter: grower, processor, distributor, or marketplace

## Steps

### 1. Create initiation directory

```bash
mkdir -p businesses/$1/00_initiation
```

### 1b. Methodology setup and workspace rules orientation

Introduce methodology prerequisites and ensure base structure exists. This step is idempotent.

```bash
# Run setup checks (safe, no changes) or apply minimal structure fixes if desired
python tools/methodology_setup.py --business businesses/$1 --format summary

# Optional (creates missing directories only; no content overwritten)
# python tools/methodology_setup.py --business businesses/$1 --apply --format summary
```

Workspace rules now active for continuous validation:

- `.windsurf/rules/structure-validation.md` — structure checks on business changes
- `.windsurf/rules/vpd-compliance.md` — VPD validation on VPD-related edits
- `.windsurf/rules/financial-validation.md` — financial CSV validation on change
- `.windsurf/rules/auto-generation.md` — generate missing deliverables when directories are added
- `.windsurf/rules/phase-gates.md` — enforce methodology gates before phase transitions

### 2. Parse business brief and create sponsor brief

```bash
# Parse business brief data and calculate budgets/timelines
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env)

# Calculate proper budgets and phase durations using modular tools
python tools/calculators/budget_calculator.py --business $1 --output-format env >> /tmp/budget_vars.env
source /tmp/budget_vars.env

# Render sponsor brief template with calculated values
python tools/generators/render_template.py \
  --template deliverables/00_initiation/00_sponsor_brief.md.j2 \
  --output businesses/$1/00_initiation/00_sponsor_brief.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/00_initiation/00_sponsor_brief.md
---
phase: 0
artifact: sponsor_brief
business: $1
---

# Sponsor Brief - ${BUSINESS_TITLE}

## Sponsor Information
- **Business**: $1 ($BUSINESS_TITLE)
- **Brief Source**: $BRIEF_FILE
- **Sponsor Commitment**: Business model design for $1 venture
- **Decision Authority**: Primary sponsor for venture development

## Business Context
**Value Proposition**:
$VALUE_PROPOSITION

**Target Market**:
$CUSTOMER_SEGMENTS

## Initial Scope
- **Core Activities**:
$KEY_ACTIVITIES
- **Key Resources**:
$KEY_RESOURCES
- **Revenue Model**:
$REVENUE_STREAMS
- **Capital Requirements**: \$$CAPITAL_MIN - \$$CAPITAL_MAX BBD
- **Timeline**: $HORIZON_YEARS-year financial horizon

## Critical Constraints
- **Market Risks**:
$CRITICAL_RISKS
- **Financial**: Discount rate $DISCOUNT_RATE%, capital bounds \$$CAPITAL_MIN-\$$CAPITAL_MAX BBD

## Success Criteria
- [ ] Viable business model within capital bounds
- [ ] Competitive market positioning established
- [ ] Risk mitigation strategies defined
- [ ] Sustainable revenue streams validated

## Next Steps
- [ ] Confirm sponsor commitment to venture
- [ ] Validate decision authority for investment
- [ ] Document regulatory and operational constraints
EOF
```

### 3. Create project charter

```bash
python tools/generators/render_template.py \
  --template deliverables/00_initiation/01_project_charter.md.j2 \
  --output businesses/$1/00_initiation/01_project_charter.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/00_initiation/01_project_charter.md
# Project Charter - $1 Business Model Design

## Project Objectives
1. Design viable business model for $1 venture within \$$CAPITAL_MIN-\$$CAPITAL_MAX BBD capital bounds
2. Validate market positioning against competitive threats and pricing pressures
3. Develop risk mitigation strategies for identified critical risks

## Success Criteria
- [ ] Business model achieves target financial performance: $FINANCIAL_METRICS over $HORIZON_YEARS years
- [ ] IRR ≥ $DISCOUNT_RATE%, positive NPV, ROI ≥ $ROI_TARGET%
- [ ] Revenue model validated with realistic market assumptions
- [ ] Risk mitigation plan addresses all critical threats

## Governance Structure
- **Project Sponsor**: Primary venture sponsor
- **Decision Rights**: Full authority for business model selection and capital allocation
- **Escalation Path**: Direct to sponsor for strategic decisions

## Scope & Constraints
- **In Scope**: Business model design, financial projections, risk assessment
- **Out of Scope**: Detailed operational planning, regulatory approvals
- **Constraints**: \$$CAPITAL_MIN-\$$CAPITAL_MAX BBD capital bounds, $HORIZON_YEARS-year timeline
EOF
```

### 4. Create resource plan

```bash
python tools/generators/render_template.py \
  --template deliverables/00_initiation/02_resource_plan.md.j2 \
  --output businesses/$1/00_initiation/02_resource_plan.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/00_initiation/02_resource_plan.md
# Resource Plan - $1 Business

## Team Requirements
- **Team Lead**: [Name/TBD]
- **Business Expert**: [Name/TBD]
- **Market Analyst**: [Name/TBD]
- **Financial Analyst**: [Name/TBD]
- **Team Size**: $TEAM_SIZE members

## BMDP Process Costs
*Operational expenses for executing the business model design process*

- **Discovery Budget**: \$$DISCOVERY_BUDGET BBD
- **Validation Budget**: \$$VALIDATION_BUDGET BBD
- **Scaling Budget**: \$$PHASE3_BUDGET BBD
- **Total BMDP Budget**: \$$TOTAL_BUDGET BBD

## Business Capital Available
*Total funding available to the business at each milestone*

- **Initial Capital**: \$$INITIAL_CAPITAL BBD
- **Post-Discovery**: \$$POST_DISCOVERY_CAPITAL BBD
- **Post-Validation**: \$$POST_VALIDATION_CAPITAL BBD
- **Maximum Capital**: \$$MAX_CAPITAL BBD

## Timeline
- **Discovery Duration**: $PHASE1_WEEKS weeks
- **Validation Duration**: $PHASE2_WEEKS weeks
- **Scaling Duration**: $PHASE3_WEEKS weeks
- **Total Timeline**: $(($PHASE1_WEEKS + $PHASE2_WEEKS + $PHASE3_WEEKS)) weeks

## Resource Availability
- [ ] Team members confirmed
- [ ] Budget approved
- [ ] Timeline validated
EOF
```

### 3. Generate team roster

```bash
python tools/generators/render_template.py \
  --template deliverables/00_initiation/03_team_roster.csv.j2 \
  --output businesses/$1/00_initiation/03_team_roster.csv
```

### 4. Create data access matrix

```bash
python tools/generators/render_template.py \
  --template deliverables/00_initiation/04_access_matrix.csv.j2 \
  --output businesses/$1/00_initiation/04_access_matrix.csv
```

### 5. Establish sprint plan

```bash
python tools/generators/render_template.py \
  --template deliverables/00_initiation/05_sprint_plan.md.j2 \
  --output businesses/$1/00_initiation/05_sprint_plan.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/00_initiation/05_sprint_plan.md
```

### 6. Create readiness assessment

```bash
python tools/generators/render_template.py \
  --template deliverables/00_initiation/06_readiness_assessment.md.j2 \
  --output businesses/$1/00_initiation/06_readiness_assessment.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/00_initiation/06_readiness_assessment.md
# Readiness Assessment - $1 Business

## Organizational Readiness Score: __/10

### Risk Assessment
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Strategy] |
| [Risk 2] | [H/M/L] | [H/M/L] | [Strategy] |

### Stakeholder Analysis
| Stakeholder | Interest Level | Influence | Engagement Strategy |
|-------------|----------------|-----------|-------------------|
| [Name/Role] | [H/M/L] | [H/M/L] | [Strategy] |

### Go/No-Go Decision
- [ ] Sponsor commitment confirmed
- [ ] Resources secured
- [ ] No critical blocking risks
- [ ] Readiness score ≥ 7/10

**Decision**: [ ] GO / [ ] NO-GO

**Rationale**: [Explain decision]
EOF
```

### 7. Initialize evidence ledger

```bash
python tools/generators/render_template.py \
  --template deliverables/shared/evidence_ledger.csv.j2 \
  --output businesses/$1/evidence_ledger.csv
```

### 8. Update business manifest

```bash
python tools/update_manifest.py --business $1 --validation-status "phase0_completed"
```

## Deliverables

- `businesses/${business_slug}/00_initiation/00_sponsor_brief.md` - Sponsor context and commitment
- `businesses/${business_slug}/00_initiation/01_project_charter.md` - Objectives, scope, success criteria
- `businesses/${business_slug}/00_initiation/02_resource_plan.md` - Team, budget, timeline
- `businesses/${business_slug}/00_initiation/03_team_roster.csv` - Team member roles and contacts
- `businesses/${business_slug}/00_initiation/04_access_matrix.csv` - Data source access permissions
- `businesses/${business_slug}/00_initiation/05_sprint_plan.md` - Sprint cadence and deliverable timeline
- `businesses/${business_slug}/00_initiation/06_readiness_assessment.md` - Risks, stakeholders, go/no-go
- Evidence logged in `businesses/${business_slug}/evidence_ledger.csv`

## Acceptance Criteria

- [ ] Sponsor commitment documented and confirmed
- [ ] Project charter approved with clear objectives
- [ ] Resource plan validated and committed
- [ ] Readiness assessment shows green light for Phase 1
- [ ] All artifacts created and evidence logged

## Gate Decision

**Proceed to Phase 1 (Mobilize) only if:**

- Sponsor demonstrates active commitment
- Resources are secured for at least Phases 1-2
- No critical blocking risks identified
- Organizational readiness score ≥ 7/10