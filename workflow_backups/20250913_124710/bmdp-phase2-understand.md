---
description: BMDP Phase 2 - Understand market, customers, and environment for business model design
auto_execution_mode: 3
---

# Phase 2: Understand

Scans environment, studies customers, interviews experts, investigates prior failures, synthesizes insights, updates assumptions, and seeds early prototypes & tests. Emphasizes bias control and evidence-based learning.

## Prerequisites

- Phase 1 mobilization completed with all deliverables:
  - `businesses/$1/10_mobilize/11_brief.md`
  - `businesses/$1/10_mobilize/12_market_ready_canvas.md` - Business Model Canvas v0 with testable hypotheses
  - `businesses/$1/10_mobilize/13_market_validation_stories.md` - Multiple business model story variations
  - `businesses/$1/10_mobilize/14_microtests.json` - Customer validation microtests
  - `businesses/$1/10_mobilize/15_phase2_research_charter.md` - Research framework and methodology
  - `businesses/$1/10_mobilize/16_kill_thrill.csv` - Risk assessment and mitigation strategies
- Business slug and research timebox defined
- Team assembled with research capabilities
- Phase 1 gate criteria met (testable hypotheses, research methodology established)

## Steps

### 1. Create research directory

```bash
mkdir -p businesses/{business_slug}/20_understand
```

### 2. Research plan and timebox

```bash
# Parse business brief data and render research plan template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/20_research_plan.md.j2 \
  --output businesses/$1/20_understand/20_research_plan.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/20_research_plan.md
```

### 3. Research questions and hypotheses

```bash
# Parse business brief data and render research questions template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/21_research_questions.md.j2 \
  --output businesses/$1/20_understand/21_research_questions.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/21_research_questions.md
```

### 4. Environment scan (PESTLE + Value Chain)

```bash
# Parse business brief data and render environment scan template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/22_environment_scan.md.j2 \
  --output businesses/$1/20_understand/22_environment_scan.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/22_environment_scan.md
```

### 5. Secondary research summary

```bash
# Parse business brief data and render secondary research template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/23_secondary_summary.md.j2 \
  --output businesses/$1/20_understand/23_secondary_summary.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/23_secondary_summary.md

# Update evidence ledger
echo "2,secondary_research,analysis,market_reports,$(date +%Y-%m-%d),medium,Market size and pricing research completed" >> businesses/$1/evidence_ledger.csv
```

### 6. Competitor mapping and mini-canvases

```bash
# Parse business brief data and render competitor templates
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/24_competitor_list.csv.j2 \
  --output businesses/$1/20_understand/24_competitor_list.csv && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/25_competitor_canvases.md.j2 \
  --output businesses/$1/20_understand/25_competitor_canvases.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/25_competitor_canvases.md
```

### 7. Customer segmentation hypotheses

```bash
# Parse business brief data and render customer segments template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/26_customer_segments.md.j2 \
  --output businesses/$1/20_understand/26_customer_segments.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/26_customer_segments.md
```

### 8. Interview toolkit

```bash
# Parse business brief data and render interview toolkit templates
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/27_interview_guide.md.j2 \
  --output businesses/$1/20_understand/27_interview_guide.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/27_interview_guide.md && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/28_screener.md.j2 \
  --output businesses/$1/20_understand/28_screener.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/28_screener.md
```

### 9. Conduct interviews and log results

```bash
# Parse business brief data and render interviews log template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/29_interviews_log.csv.j2 \
  --output businesses/$1/20_understand/29_interviews_log.csv

# Update evidence ledger
echo "2,customer_interviews,validation,customer_calls,$(date +%Y-%m-%d),high,Customer pain points and willingness to pay validated" >> businesses/$1/evidence_ledger.csv
```

### 10. Create empathy maps and JTBD

```bash
# Parse business brief data and render empathy maps template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/30_empathy_maps.md.j2 \
  --output businesses/$1/20_understand/30_empathy_maps.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/30_empathy_maps.md
```

### 10b. Structure JTBD and Pain/Gain using VPD; validate

Use the VPD validator to ensure Jobs-to-be-Done and pain/gain mapping are structured per VPD methodology (severity/importance classification, customer-value fit signals).

```bash
# Validate VPD structure for JTBD and pain/gain (summary output)
python tools/validators/vpd_validator.py --business businesses/{business_slug} --validate jobs-to-be-done --format summary
```

Recommendations:
- Ensure `pain_gain_mapping.md` classifies pains and gains with VPD severity/importance.
- Cross-reference customer jobs with value map elements in the VPD canvas.

### 11. Create Jobs-to-be-Done analysis

```bash
# Parse business brief data and render JTBD template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/31_jobs_to_be_done.md.j2 \
  --output businesses/$1/20_understand/31_jobs_to_be_done.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/31_jobs_to_be_done.md
```

### 12. Synthesize insights

```bash
# Parse business brief data and render insights template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/32_insights.md.j2 \
  --output businesses/$1/20_understand/32_insights.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/32_insights.md
```

### 13. Update assumption backlog

```bash
# Parse business brief data and render assumption backlog template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/33_assumption_backlog.csv.j2 \
  --output businesses/$1/20_understand/33_assumption_backlog.csv

# Update evidence ledger
echo "2,assumption_backlog,analysis,synthesis_workshop,$(date +%Y-%m-%d),medium,Key assumptions prioritized for testing" >> businesses/$1/evidence_ledger.csv
```

### 14. Create early prototypes and test cards

```bash
# Parse business brief data and render prototype/test card templates
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/34_concept_cards.md.j2 \
  --output businesses/$1/20_understand/34_concept_cards.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/34_concept_cards.md && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/35_test_cards.json.j2 \
  --output businesses/$1/20_understand/35_test_cards.json
```

### 15. Analyze failures and expert input

```bash
# Parse business brief data and render failure analysis templates
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/36_failure_analysis.md.j2 \
  --output businesses/$1/20_understand/36_failure_analysis.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/36_failure_analysis.md && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/37_expert_panel_summary.md.j2 \
  --output businesses/$1/20_understand/37_expert_panel_summary.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/37_expert_panel_summary.md
```

### 16. Bias check and progress demo

```bash
# Parse business brief data and render final templates
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/38_bias_check.md.j2 \
  --output businesses/$1/20_understand/38_bias_check.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/38_bias_check.md && \
python tools/generators/render_template.py \
  --template templates/deliverables/20_understand/39_progress_demo.md.j2 \
  --output businesses/$1/20_understand/39_progress_demo.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/20_understand/39_progress_demo.md

# Final evidence ledger update
echo "2,research_synthesis,analysis,progress_demo,$(date +%Y-%m-%d),high,Phase 2 research completed with key insights" >> businesses/$1/evidence_ledger.csv
```

## Deliverables

- [ ] Research plan with timebox
- [ ] Environment scan (PESTLE + value chain)
- [ ] Secondary research summary  
- [ ] Competitor analysis
- [ ] Customer segments and interview toolkit
- [ ] Interview logs (≥8 interviews)
- [ ] Empathy maps and JTBD
- [ ] VPD-structured JTBD and pain/gain classification (validated)
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