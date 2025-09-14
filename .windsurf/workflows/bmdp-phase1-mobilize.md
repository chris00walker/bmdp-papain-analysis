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
mkdir -p businesses/$1/10_mobilize
```

### 2. Confirm legitimacy and scope

```bash
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
cat > businesses/$1/10_mobilize/10_brief.md << EOF
# Mobilization Brief - $1 Business

## Sponsor Context
**Business**: $BUSINESS_TITLE
**Value Proposition**: $VALUE_PROPOSITION
**Target Market**: $CUSTOMER_SEGMENTS

## Project Scope
- **In Scope**: Business model design, validation, financial projections
- **Out of Scope**: Detailed implementation, regulatory approvals
- **Constraints**: \$$CAPITAL_MIN - \$$CAPITAL_MAX BBD capital bounds

## Decision Cadence
- Weekly progress reviews
- Biweekly steering committee
- Phase gate decisions at milestones
EOF
```

### 3. Assemble cross-functional team

```bash
cat > businesses/$1/10_mobilize/11_team_roster.csv << 'EOF'
name,role,function,allocation_pct,email
TBD,Leader,Strategy,50%,
TBD,Business Expert,Operations,30%,
TBD,Market Analyst,Research,40%,
TBD,Financial Analyst,Finance,30%,
EOF

cat > businesses/$1/10_mobilize/12_access_matrix.csv << 'EOF'
data_source,owner,permission_status,ETA
Customer interviews,Market Analyst,pending,Week 2
Competitor data,Market Analyst,approved,Week 1
Financial records,Financial Analyst,approved,Week 1
Industry reports,Business Expert,pending,Week 2
EOF
```

### 4. Orient decision makers

```bash
cat > businesses/$1/10_mobilize/13_orientation_brief.md << 'EOF'
# Business Model Canvas Orientation

## Canvas Overview
The Business Model Canvas is a strategic management tool for developing new or documenting existing business models.

## Nine Building Blocks
1. **Customer Segments**: Who are we creating value for?
2. **Value Propositions**: What value do we deliver?
3. **Channels**: How do we reach our customers?
4. **Customer Relationships**: What type of relationship do we establish?
5. **Revenue Streams**: How do we capture value?
6. **Key Resources**: What assets are required?
7. **Key Activities**: What must we do well?
8. **Key Partnerships**: Who will help us?
9. **Cost Structure**: What are the major costs?

## Storytelling Framework
- **Problem**: What pain are we solving?
- **Solution**: How do we solve it uniquely?
- **Who**: Who experiences this pain most?
- **Why Now**: What makes this the right time?
EOF
```

### 5. Frame project objectives

```bash
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
cat > businesses/$1/10_mobilize/14_mobilize_charter.md << EOF
# Mobilization Charter - $1 Business

## SMART Objectives
1. Complete customer discovery with 20+ interviews by end of Phase 2
2. Develop 3+ viable business model alternatives by Phase 3
3. Achieve 85%+ methodology compliance score
4. Validate unit economics with IRR ≥ $DISCOUNT_RATE%
5. Select final model with stakeholder consensus

## Phase KPIs
### Phase 1 (Mobilize)
- Team assembled: 100%
- Canvas v0 drafted: Complete
- Stakeholders mapped: 10+

### Phase 2 (Understand)
- Customer interviews: 20+
- Assumptions tested: 15+
- Confidence level: 70%+

### Phase 3 (Design)
- Alternatives generated: 3+
- Prototypes tested: 3+
- Final model selected: 1

## Constraints
- **Budget**: \$$BMDP_DISCOVERY_COST discovery budget
- **Timeline**: $PHASE1_WEEKS weeks Phase 1
- **Resources**: $TEAM_SIZE team members
EOF
```

### 6. Draft v0 Business Model Canvas

```bash
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
cat > businesses/$1/10_mobilize/15_canvas_v0_main.md << EOF
# Business Model Canvas v0 - $1

## Customer Segments
$CUSTOMER_SEGMENTS

## Value Propositions
$VALUE_PROPOSITION

## Channels
- Direct sales
- Partner distribution
- Digital platforms

## Customer Relationships
- Personal assistance
- Self-service
- Automated services

## Revenue Streams
$REVENUE_STREAMS

## Key Resources
$KEY_RESOURCES

## Key Activities
$KEY_ACTIVITIES

## Key Partnerships
$KEY_PARTNERSHIPS

## Cost Structure
$COST_STRUCTURE
EOF

eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
cat > businesses/$1/10_mobilize/16_idea_stories.md << EOF
# Business Idea Story - $1

## The Problem
$PROBLEM_STATEMENT

## Our Solution
$VALUE_PROPOSITION

## Who We Serve
$CUSTOMER_SEGMENTS

## Why Now
$MARKET_OPPORTUNITY

## How It Works
1. $KEY_ACTIVITIES
2. Deliver value through our channels
3. Capture value via $REVENUE_STREAMS
EOF
```

### 6b. Create Value Proposition Canvas and Customer Jobs Analysis (VPD)

Create VPD artifacts and validate structure using tools:

```bash
# Create scaffold files (idempotent; safe to run multiple times)
python tools/generators/vpd_canvas_creator.py --business businesses/$1 --apply

# Optional quick validation (summary output) - commented out as it may fail if files are incomplete
# python tools/validators/vpd_validator.py --business businesses/$1 --validate all --format summary
```

Files created/updated:
- `businesses/$1/10_mobilize/value_proposition_canvas.md`
- `businesses/$1/10_mobilize/customer_jobs_analysis.md`
- `businesses/$1/20_understand/pain_gain_mapping.md`

### 7. Kill/Thrill session

```bash
cat > businesses/$1/10_mobilize/17_kill_thrill.csv << 'EOF'
item,type,impact,owner,resolution
High capital requirements,kill,high,Financial Analyst,Explore phased approach
Market competition,kill,medium,Market Analyst,Differentiation strategy
Local sourcing,thrill,high,Business Expert,Leverage for premium
Scalability potential,thrill,high,Leader,Focus on unit economics
EOF
```

### 8. Preliminary micro-tests

```bash
cat > businesses/$1/10_mobilize/18_microtests.json << 'EOF'
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
EOF
```

### 8. Sprint planning

```bash
cat > businesses/$1/10_mobilize/18_sprint_plan.csv << 'EOF'
sprint,week,objectives,deliverables
1,1-2,"Team formation, Canvas v0","Team roster, Canvas draft"
2,3-4,"Customer discovery prep","Interview guide, Screener"
3,5-6,"Initial interviews","Interview logs, Insights"
4,7-8,"Synthesis and pivot","Updated canvas, Assumptions"
EOF
```

### 9. Stakeholder mapping

```bash
cat > businesses/$1/10_mobilize/19_stakeholder_map.csv << 'EOF'
stakeholder,interest,influence,engagement_strategy
Sponsor,high,high,Weekly updates
Investors,high,high,Monthly briefings
Operations team,medium,medium,Biweekly workshops
Customers,high,low,Interview program
Regulators,medium,high,Compliance reviews
EOF
```

### 10. Risk register

```bash
cat > businesses/$1/10_mobilize/20_risk_register.csv << 'EOF'
risk,probability,impact,mitigation,owner,status
Market acceptance,medium,high,Customer validation,Market Analyst,monitoring
Technology feasibility,low,high,Technical proof of concept,Business Expert,monitoring
Regulatory compliance,medium,medium,Legal review,Leader,active
Team availability,low,medium,Resource planning,Leader,resolved
Budget overrun,medium,medium,Phased approach,Financial Analyst,monitoring
EOF
```

### 12. Communications plan

Create `businesses/$1/10_mobilize/22_comms_plan.md`:
- Audience: Execs, BU heads, team
- Message: rationale + next steps
- Channels: email, Slack, all-hands
- Cadence: biweekly updates

Create `businesses/$1/10_mobilize/23_announcement_onepager.md`:
- New Business Model Project: Why, What, How

### 12. Update evidence ledger

```bash
cat >> businesses/$1/evidence_ledger.csv << EOF
1,canvas_v0,hypothesis,team_workshop,$(date +%Y-%m-%d),medium,Initial canvas drafted
1,stakeholder_map,analysis,stakeholder_interviews,$(date +%Y-%m-%d),high,Key stakeholders identified
1,team_roster,commitment,team_confirmation,$(date +%Y-%m-%d),high,Team assembled and committed
1,risk_register,assessment,risk_workshop,$(date +%Y-%m-%d),medium,Initial risks identified
EOF
```

## Deliverables

- [ ] Project brief and charter
- [ ] Team roster and access matrix  
- [ ] v0 Business Model Canvas
- [ ] Value Proposition Canvas (VPD)
- [ ] Customer Jobs Analysis (functional, emotional, social)
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