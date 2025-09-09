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

### 2. Parse business brief and create sponsor brief

```bash
# Parse business brief data
eval $(python tools/parse_business_brief.py --business $1)

# Create sponsor brief with parsed data
cat > businesses/$1/00_initiation/00_sponsor_brief.md << EOF
# Sponsor Brief - $1 Business

## Sponsor Information
- **Business**: $1 ($BUSINESS_TITLE)
- **Brief Source**: $BRIEF_FILE
- **Sponsor Commitment**: Business model design for $1 venture
- **Decision Authority**: Primary sponsor for venture development

## Business Context
**Value Proposition**: $VALUE_PROPOSITION

**Target Market**: $CUSTOMER_SEGMENTS

## Initial Scope
- **Core Activities**: $KEY_ACTIVITIES
- **Key Resources**: $KEY_RESOURCES
- **Revenue Model**: $REVENUE_STREAMS
- **Capital Requirements**: \$$CAPITAL_MIN - \$$CAPITAL_MAX BBD
- **Timeline**: $HORIZON_YEARS-year financial horizon

## Critical Constraints
- **Market Risks**: $CRITICAL_RISKS
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
cat > businesses/$1/00_initiation/01_project_charter.md << EOF
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
cat > businesses/$1/00_initiation/02_resource_plan.md << EOF
# Resource Plan - $1 Business

## Team Requirements
- **Team Lead**: [Name/TBD]
- **Business Expert**: [Name/TBD]
- **Market Analyst**: [Name/TBD]
- **Financial Analyst**: [Name/TBD]
- **Team Size**: $TEAM_SIZE members

## Budget Requirements
- **Discovery Budget**: \$$DISCOVERY_BUDGET BBD (35% of BMDP budget)
- **Validation Budget**: \$$VALIDATION_BUDGET BBD (35% of BMDP budget)
- **Scaling Budget**: \$$PHASE3_BUDGET BBD (30% of BMDP budget)
- **Total BMDP Budget**: \$$TOTAL_BUDGET BBD (15% of current unlocked capital)

## Milestone Budget Unlocks
- **Initial Capital**: \$$INITIAL_CAPITAL BBD
- **Post-Discovery**: \$$POST_DISCOVERY_CAPITAL BBD
- **Post-Validation**: \$$POST_VALIDATION_CAPITAL BBD
- **Maximum Capital**: \$$MAX_CAPITAL BBD

## Timeline
- **Discovery Duration**: 50% of timeline ($PHASE1_WEEKS weeks)
- **Validation Duration**: 33% of timeline ($PHASE2_WEEKS weeks)
- **Scaling Duration**: 17% of timeline ($PHASE3_WEEKS weeks)
- **Total Timeline**: $(($PHASE1_WEEKS + $PHASE2_WEEKS + $PHASE3_WEEKS)) weeks

## Resource Availability
- [ ] Team members confirmed
- [ ] Budget approved
- [ ] Timeline validated
EOF
```

### 5. Create readiness assessment

```bash
cat > businesses/$1/00_initiation/03_readiness_assessment.md << 'EOF'
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

### 6. Initialize evidence ledger

```bash
cat > businesses/$1/evidence_ledger.csv << 'EOF'
phase,artifact,evidence_type,source,date,confidence,notes
0,sponsor_brief,commitment,sponsor_interview,TBD,high,Initial commitment documented
0,project_charter,approval,sponsor_sign_off,TBD,high,Charter approved by sponsor
0,resource_plan,validation,team_confirmation,TBD,medium,Team availability confirmed
0,readiness_assessment,analysis,risk_workshop,TBD,medium,Initial risk assessment completed
EOF
```

### 7. Update business manifest

```bash
python tools/update_manifest.py --business $1 --validation-status "phase0_completed"
```

## Deliverables

- `businesses/${business_slug}/00_initiation/00_sponsor_brief.md` - Sponsor context and commitment
- `businesses/${business_slug}/00_initiation/01_project_charter.md` - Objectives, scope, success criteria
- `businesses/${business_slug}/00_initiation/02_resource_plan.md` - Team, budget, timeline
- `businesses/${business_slug}/00_initiation/03_readiness_assessment.md` - Risks, stakeholders, go/no-go
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