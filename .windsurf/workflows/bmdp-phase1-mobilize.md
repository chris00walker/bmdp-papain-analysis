---
description: BMDP Phase 1 - Mobilize business model design process for a specific business
auto_execution_mode: 3
---

# Phase 1: Mobilize

Establishes legitimacy, frames objectives, assembles team, drafts v0 Canvas, runs kill/thrill, sets sprint plan, maps stakeholders, defines risks, and launches communications.

## Prerequisites

- Business slug (grower, processor, distributor, marketplace)
- Business number (1, 2, 3, 4) 
- Sponsor brief from `brief-{number}-{business}.md`

## Steps

### 1. Create project directory structure

```bash
mkdir -p businesses/{business_slug}/10_mobilize
```

### 2. Confirm legitimacy and scope

Create `businesses/{business_slug}/10_mobilize/10_brief.md` with:
- Sponsor prompt from brief-{number}-{business}.md
- Project scope and constraints
- Decision cadence (weekly/biweekly)

### 3. Assemble cross-functional team

Create team roster `businesses/{business_slug}/10_mobilize/11_team_roster.csv`:
```csv
name,role,function,allocation_pct,email
TBD,Leader,Strategy,50%,
```

Create access matrix `businesses/{business_slug}/10_mobilize/12_access_matrix.csv`:
```csv
data_source,owner,permission_status,ETA
Customer interviews,TBD,pending,TBD
```

### 4. Orient decision makers

Create `businesses/{business_slug}/10_mobilize/13_orientation_brief.md` with:
- Business Model Canvas 101 primer
- Example canvas for reference
- Storytelling template: Problem → Solution → Who → Why Now

### 5. Frame project objectives

Create `businesses/{business_slug}/10_mobilize/14_mobilize_charter.md` with:
- 3-5 SMART objectives
- Measurable KPIs for Phases 1-3
- Budget, time, and resource constraints

### 6. Draft v0 Business Model Canvas

Create `businesses/{business_slug}/10_mobilize/15_canvas_v0_main.md` with initial:
- Customer Segments
- Value Proposition  
- Channels
- Customer Relationship Management
- Revenue Streams
- Key Resources, Activities, Partners
- Cost Structure

Create `businesses/{business_slug}/10_mobilize/16_idea_stories.md` with narrative:
- Story format: problem, solution, who, why now, mechanics

### 7. Kill/Thrill session

Create `businesses/{business_slug}/10_mobilize/17_kill_thrill.csv`:
```csv
reason,polarity,theme,severity,evidence_link
Customers may not pay,kill,market,high,
Scales globally,thrill,growth,medium,
```

### 8. Preliminary micro-tests

Create `businesses/{business_slug}/10_mobilize/18_microtests.json`:
```json
{
  "microtests": [
    {
      "assumption": "Customers will sign LOIs",
      "test": "Collect 5 LOIs", 
      "metric": "≥5 LOIs",
      "owner": "BD Lead"
    }
  ]
}
```

### 9. Sprint plan

Create `businesses/{business_slug}/10_mobilize/19_sprint_plan.md`:
- Duration: 4 weeks
- Cadence: weekly standup, biweekly review
- Deliverables: insights.md, alt canvases, tests, scorecard

### 10. Stakeholder mapping

Create `businesses/{business_slug}/10_mobilize/20_stakeholder_map.csv`:
```csv
stakeholder,interest,influence,stance,mitigation,owner
BU Head,protect revenue,high,opposed,separate entity,Sponsor
```

### 11. Risk register

Create `businesses/{business_slug}/10_mobilize/21_risk_register.csv`:
```csv
risk,likelihood,impact,trigger,mitigation,owner
Overestimating idea,high,high,early excitement,kill/thrill checks,PMO
```

### 12. Communications plan

Create `businesses/{business_slug}/10_mobilize/22_comms_plan.md`:
- Audience: Execs, BU heads, team
- Message: rationale + next steps
- Channels: email, Slack, all-hands
- Cadence: biweekly updates

Create `businesses/{business_slug}/10_mobilize/23_announcement_onepager.md`:
- New Business Model Project: Why, What, How

### 13. Update evidence ledger

Append to `businesses/{business_slug}/evidence_ledger.csv`:
```csv
evidence_type,evidence_description,evidence_datum,confidence,source_link,decision_impact,owner,date
microtest,customers sign LOIs,assumption test,pending,,decision impact: go/no-go,BD Lead,today
```

## Deliverables

- [ ] Project brief and charter
- [ ] Team roster and access matrix  
- [ ] v0 Business Model Canvas
- [ ] Kill/thrill analysis
- [ ] Micro-test definitions
- [ ] Sprint plan
- [ ] Stakeholder map
- [ ] Risk register
- [ ] Communications plan
- [ ] Evidence ledger entries

## Gate Criteria

Proceed to Phase 2 only if:
- All deliverables completed
- Team assembled and committed
- Canvas v0 tells coherent story
- ≥3 evidence entries logged
- Stakeholder buy-in secured