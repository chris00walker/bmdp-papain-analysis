---
description: Establishes project legitimacy, confirms sponsor commitment, defines initial scope and constraints, and sets up governance structure. Gateway to formal BMDP execution.
---

# Phase 0: Initiation

## Overview

The initiation phase validates project readiness and establishes the foundation for the Business Model Design Process. This phase ensures we have proper sponsorship, clear objectives, and organizational commitment before proceeding to mobilization.

## Inputs Required

- Sponsor brief/prompt (from domain brief)
- Initial business context
- Organizational readiness assessment

## Key Activities

### Step 0.1: Sponsor Validation

// turbo

1. **Review sponsor prompt** from brief-${business_number}-${business_slug}.md
2. **Confirm sponsor commitment** and decision authority
3. **Document initial scope** and constraints

### Step 0.2: Project Charter

// turbo

1. **Define project objectives** aligned with sponsor needs
2. **Set success criteria** and key milestones
3. **Establish governance structure** and decision rights

### Step 0.3: Resource Assessment

// turbo

1. **Assess team availability** and skill requirements
2. **Confirm budget and timeline** constraints
3. **Identify key stakeholders** and their interests

### Step 0.4: Risk & Readiness Check

// turbo

1. **Evaluate organizational readiness** for business model innovation
2. **Identify critical risks** and mitigation strategies
3. **Confirm go/no-go decision** for proceeding to Phase 1

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
