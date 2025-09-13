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

### 2. Design brief and timebox

```bash
# Parse business brief data and render design brief template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/30_design_brief.md.j2 \
  --output businesses/$1/30_design/30_design_brief.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/30_design_brief.md
```

### 3. Ideation session

```bash
# Parse business brief data and render ideation template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/31_ideation.md.j2 \
  --output businesses/$1/30_design/31_ideation.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/31_ideation.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/31_ideation.md
```

### 4. Create prototype canvases

```bash
# Create prototypes directory and render canvas templates
mkdir -p businesses/$1/30_design/32_prototypes

# Parse business brief data and render prototype A canvas
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/32_prototypes/prototype_A_canvas.md.j2 \
  --output businesses/$1/30_design/32_prototypes/prototype_A_canvas.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/32_prototypes/prototype_A_canvas.md

# Parse business brief data and render prototype B canvas
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/32_prototypes/prototype_B_canvas.md.j2 \
  --output businesses/$1/30_design/32_prototypes/prototype_B_canvas.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/32_prototypes/prototype_B_canvas.md

# Parse business brief data and render prototype C canvas
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/32_prototypes/prototype_C_canvas.md.j2 \
  --output businesses/$1/30_design/32_prototypes/prototype_C_canvas.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/32_prototypes/prototype_C_canvas.md
```

### 5. Prototype testing and validation

```bash
# Parse business brief data and render prototype testing template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/32_prototype_testing.md.j2 \
  --output businesses/$1/30_design/32_prototype_testing.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/32_prototype_testing.md
```

### 6. Build-Measure-Learn cycles

```bash
# Parse business brief data and render Build-Measure-Learn template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/33_build_measure_learn.md.j2 \
  --output businesses/$1/30_design/33_build_measure_learn.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/33_build_measure_learn.md
```

### 7. Pivot decision framework

```bash
# Parse business brief data and render pivot decision template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/34_pivot_decision.md.j2 \
  --output businesses/$1/30_design/34_pivot_decision.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/34_pivot_decision.md
```

### 8. Stakeholder feedback collection

```bash
# Parse business brief data and render feedback log template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/35_feedback_log.csv.j2 \
  --output businesses/$1/30_design/35_feedback_log.csv
```

### 9. Selection criteria and scorecard

```bash
# Parse business brief data and render selection criteria template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/36_selection_criteria.md.j2 \
  --output businesses/$1/30_design/36_selection_criteria.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/36_selection_criteria.md

# Parse business brief data and render selection scorecard template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/37_selection_scorecard.csv.j2 \
  --output businesses/$1/30_design/37_selection_scorecard.csv
```

### 10. BMG viability assessment

Validate Business Model Generation (BMG) coherence and viability for selected prototype.

```bash
# Validate BMG nine building blocks coherence (summary output)
python tools/validators/bmg_validator.py --business businesses/{business_slug} --validate viability --format summary
```

### 11. Financial projections

```bash
# Parse business brief data and render financial projections template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/38_financial_projections.md.j2 \
  --output businesses/$1/30_design/38_financial_projections.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/38_financial_projections.md
```

### 12. Implementation roadmap

```bash
# Parse business brief data and render implementation roadmap template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/39_implementation_roadmap.md.j2 \
  --output businesses/$1/30_design/39_implementation_roadmap.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/39_implementation_roadmap.md
```

### 13. Risk assessment and mitigation

```bash
# Parse business brief data and render risk mitigation template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/40_risk_mitigation.md.j2 \
  --output businesses/$1/30_design/40_risk_mitigation.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/40_risk_mitigation.md
```

### 14. Integration/separation decision

```bash
# Parse business brief data and render integration decision template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/40_integration_decision.md.j2 \
  --output businesses/$1/30_design/40_integration_decision.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/40_integration_decision.md
```

### 15. Final recommendation

```bash
# Parse business brief data and render final recommendation template
eval $(python tools/parsers/brief_parser.py --business $1 --output-format env) && \
python tools/generators/render_template.py \
  --template templates/deliverables/30_design/41_final_recommendation.md.j2 \
  --output businesses/$1/30_design/41_final_recommendation.md && \
python tools/processors/llm_processor.py \
  --input businesses/$1/30_design/41_final_recommendation.md

# Update evidence ledger
echo "3,prototype_selection,analysis,selection_scorecard,$(date +%Y-%m-%d),high,Business model prototype selected based on evaluation criteria" >> businesses/$1/evidence_ledger.csv
echo "3,stakeholder_feedback,validation,feedback_sessions,$(date +%Y-%m-%d),medium,Stakeholder input collected on prototype options" >> businesses/$1/evidence_ledger.csv
echo "3,financial_projections,analysis,financial_model,$(date +%Y-%m-%d),medium,5-year financial projections completed" >> businesses/$1/evidence_ledger.csv
echo "3,design_completion,milestone,final_recommendation,$(date +%Y-%m-%d),high,Phase 3 design completed with final recommendation" >> businesses/$1/evidence_ledger.csv
```

## Deliverables

- [ ] Design brief with timebox
- [ ] Ideation session with ≥3 alternatives
- [ ] ≥3 prototype business model canvases
- [ ] Prototype testing with customer validation
- [ ] Build-Measure-Learn cycle documentation
- [ ] Pivot/persevere decisions with rationale
- [ ] Stakeholder feedback from ≥9 sources
- [ ] Selection criteria and scorecard
- [ ] BMG viability assessment (validated)
- [ ] Financial projections for selected model
- [ ] Implementation roadmap
- [ ] Risk assessment and mitigation plan
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