---
description: BMDP Phase 2 - Understand market, customers, and environment for business model design
---

# Phase 2: Understand

Scans environment, studies customers, interviews experts, investigates prior failures, synthesizes insights, updates assumptions, and seeds early prototypes & tests. Emphasizes bias control and evidence-based learning.

## Prerequisites

- Phase 1 completed with v0 Canvas
- Business slug and research timebox defined
- Team assembled with research capabilities

## Steps

### 1. Create research directory

```bash
mkdir -p businesses/{business_slug}/20_understand
```

### 2. Research plan and timebox

Create `businesses/{business_slug}/20_understand/20_research_plan.md`:

- Timebox: 10 days (default)
- Objectives: Reduce uncertainty on top assumptions; avoid over-research
- Deliverables: env_scan, segments, interviews, empathy/JTBD, insights, competitor canvases
- Progress demos: mid-sprint & end-of-sprint

### 3. Research questions and hypotheses

Create `businesses/{business_slug}/20_understand/21_research_questions.md`:

- Questions: market size, willingness to pay, adoption barriers, channel economics
- Hypotheses: H1-Hn with pass/fail thresholds
- Evidence types: secondary, expert, customer, pilot signals

### 4. Environment scan (PESTLE + Value Chain)

Create `businesses/{business_slug}/20_understand/22_environment_scan.md`:

- PESTLE: Political, Economic, Social, Technological, Legal, Environmental
- Value chain: suppliers → producers → distributors → customers
- Regulations/Standards: certifications, quality, safety; emerging trends

### 5. Secondary research summary

Create `businesses/{business_slug}/20_understand/23_secondary_summary.md`:

- Top sources: 5-10 credible market/tech/regulatory sources
- Key data points: prices, volumes, growth, benchmarks

Update evidence ledger:

```csv
evidence_type,evidence_description,evidence_datum,confidence,source_link,decision_impact,owner,date
secondary,market growth estimate,TBD datum,medium,,sizes TAM/SAM/SOM,Analyst,today
secondary,pricing corridor,TBD datum,high,,sets WTP prior,Analyst,today
```

### 6. Competitor mapping and mini-canvases

Create `businesses/{business_slug}/20_understand/24_competitor_list.csv`:

```csv
name,region,segment,notes
TBD_1,TBD,TBD,
```

Create `businesses/{business_slug}/20_understand/24_competitor_canvases.md`:

- Competitor 1 Canvas (mini): Segments, VP, Channels, Revenue, Costs, Partners, Activities, Resources

### 7. Customer segmentation hypotheses

Create `businesses/{business_slug}/20_understand/25_customer_segments.md`:

- Segments: primary, secondary, exploratory
- Selection criteria: size, pain intensity, access, willingness to pay

### 8. Interview toolkit

Create `businesses/{business_slug}/20_understand/26_interview_guide.md`:

- JTBD framing, past-behavior prompts, pricing probes

Create `businesses/{business_slug}/20_understand/27_screener.md`:

- Inclusion/exclusion criteria
- Sample screening questions

### 9. Conduct interviews and log results

Create `businesses/{business_slug}/20_understand/28_interviews_log.csv`:

```csv
date,segment,role,company,key_insights,quotes,followups
TBD,TBD,TBD,TBD,pain point X,"quote",next step
```

Update evidence ledger:

```csv
evidence_type,evidence_description,evidence_datum,confidence,source_link,decision_impact,owner,date
customer,pain point X,interview note,medium,,refines VP,Research,today
```

### 10. Create empathy maps and JTBD

Create `businesses/{business_slug}/20_understand/29_empathy_maps.md`:

- Segment A: Says/Thinks/Does/Feels

Create `businesses/{business_slug}/20_understand/30_jobs_to_be_done.md`:

- Functional, Social, Emotional jobs
- Pains and gains

### 11. Synthesize insights

Create `businesses/{business_slug}/20_understand/31_insights.md`:

- Top themes (3-7)
- Contradictions & open questions
- Implications for design

### 12. Update assumption backlog

Create `businesses/{business_slug}/20_understand/32_assumption_backlog.csv`:

```csv
assumption,evidence,confidence,impact,priority_method,priority_score
Customers pay X,weak,low,high,ICE,0.3
```

Update evidence ledger:

```csv
evidence_type,evidence_description,evidence_datum,confidence,source_link,decision_impact,owner,date
synthesis,top assumptions identified,list,medium,,sets test focus,PM,today
```

### 13. Create early prototypes and test cards

Create `businesses/{business_slug}/20_understand/33_concept_cards.md`:

- Concept A: proposition, who, channel, pricing hypothesis
- Concept B: proposition, who, channel, pricing hypothesis

Create `businesses/{business_slug}/20_understand/34_test_cards.json`:

```json
{
  "tests": [
    {
      "assumption": "WTP >= $X",
      "test": "price interviews (n=5)",
      "metric": "≥3 accept",
      "stop_condition": "timebox or 2 fails"
    },
    {
      "assumption": "Channel partner interest",
      "test": "2 partner calls",
      "metric": "≥1 LOI",
      "stop_condition": "timebox"
    }
  ]
}
```

### 14. Analyze failures and expert input

Create `businesses/{business_slug}/20_understand/35_failure_analysis.md`:

- Prior failures in this space
- Lessons learned
- What to avoid

Create `businesses/{business_slug}/20_understand/36_expert_panel_summary.md`:

- Expert interviews summary
- Industry insights
- Validation/contradiction of assumptions

### 15. Bias check and progress demo

Create `businesses/{business_slug}/20_understand/37_bias_check.md`:

- Confirmation bias check
- Alternative explanations
- Blind spots identified

Create `businesses/{business_slug}/20_understand/38_progress_demo.md`:

- Research findings summary
- Updated assumptions
- Recommended next steps

## Deliverables

- [ ] Research plan with timebox
- [ ] Environment scan (PESTLE + value chain)
- [ ] Secondary research summary  
- [ ] Competitor analysis
- [ ] Customer segments and interview toolkit
- [ ] Interview logs (≥8 interviews)
- [ ] Empathy maps and JTBD
- [ ] Insights synthesis
- [ ] Updated assumption backlog
- [ ] Early concept cards and test cards
- [ ] Failure analysis and expert input
- [ ] Bias check and progress demo
- [ ] ≥10 evidence ledger entries

## Gate Criteria

Proceed to Phase 3 only if:

- All deliverables completed within timebox
- ≥8 customer interviews conducted
- Top 3-5 insights clearly articulated
- Assumption backlog prioritized (ICE/RICE)
- Test cards defined for riskiest assumptions
- Evidence ledger has ≥10 entries
