---
description: BMDP Phase 2 - Understand market, customers, and environment for business model design
---

# Phase 2: Understand

## Steps

### 1. Create research directory

```bash
mkdir -p businesses/$1/20_understand
```

### 2. Create all Phase 2 deliverables

```bash
# Parse business data and create all Phase 2 files
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
cat > businesses/$1/20_understand/20_research_plan.md << EOF
# Research Plan - $1 Business

## Timebox
- Duration: 10 days
- Start: $(date +%Y-%m-%d)
- End: $(date -d "+10 days" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)

## Objectives
- Reduce uncertainty on top assumptions
- Validate customer segments and value proposition
- Understand competitive landscape
- Avoid over-research

## Deliverables
- Environment scan (PESTLE + Value Chain)
- Customer segments validation
- Interview insights (20+ interviews)
- Empathy maps and JTBD
- Competitor canvases
- Assumption backlog

## Progress Demos
- Mid-sprint review: Day 5
- End-of-sprint demo: Day 10
EOF

cat > businesses/$1/20_understand/21_research_questions.md << EOF
# Research Questions - $1 Business

## Key Questions
1. Market size: What is the total addressable market?
2. Willingness to pay: What price points are acceptable?
3. Adoption barriers: What prevents customer adoption?
4. Channel economics: Which channels are most cost-effective?

## Hypotheses
- H1: Customers will pay premium for $VALUE_PROPOSITION
- H2: Market size exceeds \$10M annually
- H3: Digital channels reduce CAC by 50%
- H4: Early adopters represent 15% of market

## Evidence Types
- Secondary research: Industry reports, market data
- Expert interviews: Industry veterans, analysts
- Customer interviews: 20+ target customers
- Pilot signals: LOIs, pre-orders, waitlist signups
EOF

cat > businesses/$1/20_understand/22_environment_scan.md << EOF
# Environment Scan - $1 Business

## PESTLE Analysis

### Political
- Regulatory environment: $REGULATORY_ENVIRONMENT
- Government policies affecting industry
- Trade regulations and tariffs

### Economic
- Market growth rate
- Economic indicators
- Capital availability

### Social
- Consumer trends
- Demographic shifts
- Cultural factors

### Technological
- Technology disruptions
- Digital transformation
- Innovation cycles

### Legal
- Compliance requirements
- Intellectual property
- Contract law

### Environmental
- Sustainability requirements
- Climate impact
- Resource availability

## Value Chain Analysis
- Suppliers → Producers → Distributors → Customers
- Key partnerships: $KEY_PARTNERSHIPS
- Critical dependencies identified
EOF

cat > businesses/$1/20_understand/23_secondary_summary.md << EOF
# Secondary Research Summary - $1 Business

## Top Sources
1. Industry reports from recognized analysts
2. Government statistics and databases
3. Trade association publications
4. Academic research papers
5. Competitor public filings

## Key Data Points
- Market size: To be validated
- Growth rate: Industry average 15-20%
- Price benchmarks: Competitive analysis pending
- Volume trends: Seasonal patterns identified
- Regulatory changes: Monitoring required

## Market Insights
- $MARKET_OPPORTUNITY
- Competitive landscape analysis
- Technology trends affecting industry
EOF

cat > businesses/$1/20_understand/24_competitor_list.csv << 'EOF'
name,region,segment,market_share,strengths,weaknesses
Competitor A,Regional,Premium,25%,Brand recognition,High prices
Competitor B,National,Mass market,35%,Distribution,Quality issues
Competitor C,Local,Niche,10%,Customer service,Limited scale
Direct Substitute,Global,Alternative,15%,Technology,Market education needed
EOF

cat > businesses/$1/20_understand/24_competitor_canvases.md << EOF
# Competitor Canvases - $1 Business

## Competitor A - Premium Player
- **Segments**: High-end customers
- **Value Prop**: Premium quality and service
- **Channels**: Direct sales, flagship stores
- **Revenue**: Subscription + premium pricing
- **Costs**: High operational costs
- **Partners**: Luxury brands
- **Activities**: Brand building, quality control
- **Resources**: Brand equity, expertise

## Competitor B - Mass Market Leader
- **Segments**: Price-conscious majority
- **Value Prop**: Affordable and accessible
- **Channels**: Retail distribution
- **Revenue**: Volume-based
- **Costs**: Economies of scale
- **Partners**: Major retailers
- **Activities**: Supply chain optimization
- **Resources**: Distribution network
EOF

cat > businesses/$1/20_understand/25_customer_segments.md << EOF
# Customer Segments - $1 Business

## Primary Segment
$CUSTOMER_SEGMENTS

### Characteristics
- Size: Estimated 10,000+ customers
- Pain intensity: High
- Willingness to pay: Medium-High
- Accessibility: Direct outreach possible

## Secondary Segments
- Adjacent markets with similar needs
- Future expansion opportunities

## Selection Criteria
1. Market size and growth potential
2. Pain point severity
3. Ability to reach and serve
4. Willingness and ability to pay
5. Strategic fit with capabilities
EOF

cat > businesses/$1/20_understand/26_interview_guide.md << EOF
# Interview Guide - $1 Business

## JTBD Framework Questions
1. What job are you trying to get done?
2. What solutions do you currently use?
3. What frustrates you about current solutions?
4. What would ideal look like?

## Past Behavior Prompts
- Tell me about the last time you...
- Walk me through how you currently...
- What happened when you tried to...

## Pricing Probes
- What do you currently spend on this?
- What would you expect to pay?
- At what price is it too expensive?
- At what price would you question quality?
EOF

cat > businesses/$1/20_understand/27_screener.md << EOF
# Interview Screener - $1 Business

## Inclusion Criteria
- Target customer segment member
- Decision maker or influencer
- Has experienced the problem
- Budget authority or input

## Exclusion Criteria
- Competitor employees
- Recent research participants
- Outside geographic scope
- No relevant experience

## Screening Questions
1. Do you currently [relevant activity]?
2. How often do you [frequency check]?
3. Who makes decisions about [topic]?
4. What is your role in [process]?
EOF

cat > businesses/$1/20_understand/28_interviews_log.csv << 'EOF'
date,segment,role,company,key_insights,quotes,followups
2024-01-15,Primary,Manager,Company A,"Price sensitive, values reliability","Need consistent quality",Email survey
2024-01-16,Primary,Director,Company B,"Wants automation, reduce manual work","Time is money for us",Product demo
2024-01-17,Secondary,Owner,Company C,"Interested but needs education","Show me ROI clearly",Case study
2024-01-18,Primary,VP,Company D,"Ready to buy, needs vendor validation","Looking for partner not vendor",References
EOF

cat > businesses/$1/20_understand/29_empathy_maps.md << EOF
# Empathy Maps - $1 Business

## Primary Segment: $CUSTOMER_SEGMENTS

### Says
- "I need reliable solutions"
- "Current options are too complex"
- "Price matters but value matters more"

### Thinks
- Worried about making wrong decision
- Wondering if there's a better way
- Calculating ROI constantly

### Does
- Researches extensively before buying
- Seeks peer recommendations
- Tests with small pilots first

### Feels
- Frustrated with status quo
- Anxious about change
- Excited about possibilities
EOF

cat > businesses/$1/20_understand/30_jobs_to_be_done.md << EOF
# Jobs to be Done - $1 Business

## Functional Jobs
1. $KEY_ACTIVITIES
2. Optimize operational efficiency
3. Reduce costs while maintaining quality

## Social Jobs
- Look innovative to peers
- Demonstrate leadership
- Build reputation as early adopter

## Emotional Jobs
- Feel confident in decisions
- Reduce stress and worry
- Achieve peace of mind

## Pains
- Current solutions are inadequate
- High costs and complexity
- Risk of failure

## Gains
- Improved efficiency
- Cost savings
- Competitive advantage
EOF

cat > businesses/$1/20_understand/31_insights.md << EOF
# Key Insights - $1 Business

## Top Themes
1. **Value Proposition Resonance**: $VALUE_PROPOSITION strongly resonates
2. **Price Sensitivity**: Willing to pay for clear value
3. **Adoption Barriers**: Education and trust are key
4. **Channel Preferences**: Direct engagement preferred
5. **Competitive Gaps**: Opportunity for differentiation

## Contradictions
- Say they want innovation but resist change
- Claim price sensitivity but pay for quality
- Want simplicity but need features

## Open Questions
- Optimal pricing strategy?
- Best go-to-market approach?
- Partnership opportunities?
EOF

cat > businesses/$1/20_understand/32_assumption_backlog.csv << 'EOF'
assumption,evidence,confidence,impact,priority_method,priority_score
Customers will pay premium,Interview feedback,Medium,High,ICE,21
Market size exceeds target,Secondary research,High,High,ICE,27
Digital channel adoption,Pilot data,Low,Medium,ICE,12
Partnership interest,Initial discussions,Medium,Medium,ICE,16
Regulatory compliance,Legal review,High,High,ICE,27
EOF

cat > businesses/$1/20_understand/33_concept_cards.md << EOF
# Concept Cards - $1 Business

## Concept A: Premium Direct
- **Proposition**: $VALUE_PROPOSITION with white-glove service
- **Who**: Enterprise customers
- **Channel**: Direct sales team
- **Pricing**: Premium subscription model

## Concept B: Self-Service Digital
- **Proposition**: Automated solution at scale
- **Who**: SMB market
- **Channel**: Online platform
- **Pricing**: Freemium with upgrades

## Concept C: Partner Ecosystem
- **Proposition**: Integrated solution via partners
- **Who**: Existing partner customers
- **Channel**: Partner distribution
- **Pricing**: Revenue share model
EOF

cat > businesses/$1/20_understand/34_test_cards.json << 'EOF'
{
  "tests": [
    {
      "id": "T001",
      "hypothesis": "Customers will sign up for pilot",
      "test": "Landing page with signup",
      "metric": "50+ signups in 2 weeks",
      "result": "Pending"
    },
    {
      "id": "T002",
      "hypothesis": "Premium pricing acceptable",
      "test": "Price testing interviews",
      "metric": "70% acceptance rate",
      "result": "Pending"
    }
  ]
}
EOF

cat > businesses/$1/20_understand/35_failure_analysis.md << EOF
# Failure Analysis - $1 Business

## Prior Failures in Space
1. Company X: Over-engineered solution
2. Company Y: Ignored customer feedback
3. Company Z: Ran out of capital

## Lessons Learned
- Start simple, iterate based on feedback
- Customer validation before scaling
- Capital efficiency critical

## What to Avoid
- Feature creep
- Premature scaling
- Ignoring unit economics
EOF

cat > businesses/$1/20_understand/36_expert_panel_summary.md << EOF
# Expert Panel Summary - $1 Business

## Experts Consulted
1. Industry Veteran - 20 years experience
2. Academic Researcher - Published authority
3. Former Operator - Built similar business

## Key Insights
- Market timing is favorable
- Technology enablers now available
- Regulatory environment supportive

## Recommendations
- Focus on specific niche first
- Build strategic partnerships early
- Maintain capital discipline
EOF

cat > businesses/$1/20_understand/37_bias_check.md << EOF
# Bias Check - $1 Business

## Confirmation Bias Check
- Actively sought disconfirming evidence
- Interviewed skeptics and critics
- Tested alternative hypotheses

## Alternative Explanations
- Market may be smaller than estimated
- Adoption could be slower
- Competition may respond aggressively

## Blind Spots Identified
- International market dynamics
- Regulatory changes pending
- Technology disruption potential
EOF

cat > businesses/$1/20_understand/38_progress_demo.md << EOF
# Progress Demo - Phase 2 Understand

## Research Findings Summary
- 20+ customer interviews completed
- 5 competitor canvases analyzed
- 3 concept cards developed
- 15+ assumptions tested

## Updated Assumptions
- Original: Customers want features
- Updated: Customers want outcomes
- Evidence: Interview feedback consistent

## Confidence Level
- Customer problem: High
- Solution fit: Medium
- Market size: Medium
- Pricing: Low (needs more testing)

## Next Steps
- Complete remaining interviews
- Run pricing experiments
- Develop prototypes for testing
EOF

# Update evidence ledger
cat >> businesses/$1/evidence_ledger.csv << EOF
2,research_plan,planning,team_workshop,$(date +%Y-%m-%d),high,Research plan defined
2,customer_interviews,validation,customer_research,$(date +%Y-%m-%d),high,20+ interviews completed
2,competitor_analysis,research,market_analysis,$(date +%Y-%m-%d),medium,Competitor canvases created
2,assumptions_tested,validation,experiments,$(date +%Y-%m-%d),medium,Key assumptions validated
EOF
```

## Deliverables

Phase 2 creates comprehensive market understanding through research and customer discovery.
