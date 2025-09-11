---
description: BMDP Phase 3 - Generate, prototype, and test multiple business model options with selection scorecard
auto_execution_mode: 3
---

# Phase 3: Design

Generates, prototypes, and tests multiple business model options with selection scorecard. Emphasizes creative ideation, rapid prototyping, stakeholder feedback, and evidence-based selection.

## Prerequisites

- Phase 2 completed with insights and assumptions
- Business slug and design timebox defined
- Team assembled with design capabilities

## Steps

### 1. Create design directory

```bash
mkdir -p businesses/{business_slug}/30_design
```

### 6b. BMG viability assessment (validate)

Validate Business Model Generation (BMG) coherence and viability for candidate prototypes using the BMG validator.

```bash
# Validate BMG nine building blocks coherence (summary output)
python tools/bmg_validator.py --business businesses/{business_slug} --validate viability --format summary
```

Recommendations:
- Ensure selected prototype's canvas elements reinforce each other (nine blocks).
- Align financial projections and cost structure with the canvas assumptions.

### 2. Design brief and timebox

Create `businesses/{business_slug}/30_design/30_design_brief.md`:

- Timebox: 15 days (default)
- Objectives: Generate ≥3 viable alternatives; select best option
- Deliverables: ideation, prototypes, feedback, selection scorecard
- Progress demos: mid-sprint & end-of-sprint

### 3. Ideation session

Create `businesses/{business_slug}/30_design/31_ideation.md`:

- Alternatives brainstormed: ≥3 bold options beyond status quo
- Source inspirations: insights, competitor patterns, blue ocean moves
- Constraint challenges: what if budget was 10x? 1/10x?

### 4. Create prototype canvases

Create `businesses/{business_slug}/30_design/32_prototypes/`:

For each alternative, create a business model canvas:
- `prototype_A_canvas.md`
- `prototype_B_canvas.md` 
- `prototype_C_canvas.md`

Each canvas includes:
- Customer Segments
- Value Propositions
- Channels
- Customer Relationships
- Revenue Streams
- Key Resources
- Key Activities
- Key Partnerships
- Cost Structure

### 5. Stakeholder feedback collection

Create `businesses/{business_slug}/30_design/33_feedback_log.csv`:

```csv
date,stakeholder,role,prototype,feedback,concerns,preferences
TBD,TBD,customer,A,positive on feature X,worried about price,prefers option A
```

Collect feedback from:
- ≥5 potential customers
- ≥2 industry experts
- ≥2 internal stakeholders

### 6. Selection criteria and scorecard

Create `businesses/{business_slug}/30_design/34_selection_criteria.md`:

Define weighted criteria:
- Market attractiveness (25%)
- Competitive advantage (20%)
- Financial viability (20%)
- Implementation feasibility (15%)
- Strategic fit (10%)
- Risk level (10%)

Create `businesses/{business_slug}/30_design/35_selection_scorecard.csv`:

```csv
criteria,weight,prototype_A,prototype_B,prototype_C
market_attractiveness,0.25,7,8,6
competitive_advantage,0.20,6,7,9
financial_viability,0.20,8,6,7
implementation_feasibility,0.15,9,5,6
strategic_fit,0.10,7,8,8
risk_level,0.10,6,7,5
weighted_score,,7.1,6.8,7.0
```

### 7. Financial projections

Create `businesses/{business_slug}/30_design/36_financial_projections.md`:

For selected prototype:
- 5-year revenue projections
- Cost structure breakdown
- Investment requirements
- Break-even analysis
- ROI/IRR calculations

### 8. Implementation roadmap

Create `businesses/{business_slug}/30_design/37_implementation_roadmap.md`:

- Phase 1: MVP development (months 1-6)
- Phase 2: Market validation (months 7-12)
- Phase 3: Scale preparation (months 13-18)
- Key milestones and decision points

### 9. Risk assessment and mitigation

Create `businesses/{business_slug}/30_design/38_risk_mitigation.md`:

- Top 5 risks identified
- Probability and impact assessment
- Mitigation strategies
- Contingency plans

### 10. Test cards for validation

Create `businesses/{business_slug}/30_design/39_test_cards.json`:

```json
{
  "tests": [
    {
      "assumption": "Customers will pay $X",
      "test": "pricing survey (n=20)",
      "metric": "≥70% accept price",
      "timeline": "2 weeks"
    },
    {
      "assumption": "Channel partners interested",
      "test": "partner interviews (n=3)",
      "metric": "≥2 express interest",
      "timeline": "1 week"
    }
  ]
}
```

### 11. Integration/separation decision

Create `businesses/{business_slug}/30_design/40_integration_decision.md`:

- Standalone business vs integration with existing operations
- Synergies and conflicts analysis
- Resource sharing opportunities
- Organizational implications

### 12. Create financial cash flow data

Create `businesses/{business_slug}/30_design/financials_cashflow.csv`:

```csv
year,revenues_bbd,capex_bbd,opex_bbd,working_cap_change_bbd,notes
0,0,750000,50000,100000,Initial investment phase
1,705000,0,634500,25000,Market entry phase
2,1680000,75000,924000,50000,Scale operations
3,2450000,50000,1314000,75000,Mature operations
4,2600000,25000,1397000,25000,Optimized operations
5,2805000,0,1545000,-25000,Stable operations
```

**Required for**: Financial analysis and validation workflow

### 13. Final recommendation

Create `businesses/{business_slug}/30_design/41_final_recommendation.md`:

- Executive summary with selected prototype
- Selection rationale and scoring results
- Implementation timeline and resource requirements
- Financial projections and ROI analysis
- Risk assessment and mitigation strategies
- Next steps and validation requirements

**Deliverable**: Comprehensive business model recommendation ready for validation phase.

Update evidence ledger:

```csv
evidence_type,evidence_description,evidence_datum,confidence,source_link,decision_impact,owner,date
design,prototype selection,selected model A,high,,final recommendation,PM,today
design,stakeholder feedback,positive reception,medium,,validates approach,Design,today
design,financial projections,ROI 25%,medium,,investment decision,Finance,today
```

## Deliverables

- [ ] Design brief with timebox
- [ ] Ideation session with ≥3 alternatives
- [ ] ≥3 prototype business model canvases
- [ ] Stakeholder feedback from ≥9 sources
- [ ] Selection criteria and scorecard
- [ ] BMG viability assessment (validated)
- [ ] Financial projections for selected model
- [ ] Implementation roadmap
- [ ] Risk assessment and mitigation plan
- [ ] Test cards for key assumptions
- [ ] TBI testing rigor (validated)
- [ ] Integration/separation decision
- [ ] Final recommendation with rationale
- [ ] ≥5 evidence ledger entries

## Gate Criteria

Proceed to Phase 4 (Implementation) only if:

- ≥3 prototypes created and evaluated
- At least 1 prototype scores ≥0.7 on selection criteria
- Stakeholder feedback collected from ≥9 sources
- Integration/separation decision made
- Test cards defined for implementation risks
- Evidence ledger updated with design insights