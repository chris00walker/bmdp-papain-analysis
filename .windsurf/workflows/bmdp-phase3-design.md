---
description: Generates, prototypes, and tests multiple bold business model options, co-created across the organization. Produces narratives, risk/reward profiles, test cards, and a selection scorecard to choose the best model(s).
auto_execution_mode: 1
---

# BMDP Phase 3: Design

## Workflow Configuration

name: bmdp_phase3_design
version: "1.0"

parameters:
  repo_root:
    type: string
    default: "./bmdp"
  min_alternatives:
    type: integer
    default: 3
  min_tests:
    type: integer
    default: 3
  selection_threshold:
    type: number
    default: 0.7   # min weighted score required to advance

artifacts:

## Inputs from prior phases

  insights_md:      "${repo_root}/20_understand/31_insights.md"
  assumptions_csv:  "${repo_root}/20_understand/32_assumption_backlog.csv"
  concepts_md:      "${repo_root}/20_understand/33_concept_cards.md"
  testcards_json:   "${repo_root}/20_understand/34_test_cards.json"
  evidence_csv:     "${repo_root}/common/evidence_ledger.csv"

## Phase 3 outputs

  ideation_md:      "${repo_root}/30_design/30_ideation.md"
  prototypes_dir:   "${repo_root}/30_design/prototypes"
  prototypes_md:    "${repo_root}/30_design/31_prototypes_summary.md"
  narratives_md:    "${repo_root}/30_design/32_narratives.md"
  riskreward_csv:   "${repo_root}/30_design/33_risk_reward_profiles.csv"
  feedback_csv:     "${repo_root}/30_design/34_feedback_log.csv"
  scorecard_md:     "${repo_root}/30_design/35_scorecard.md"
  selected_md:      "${repo_root}/30_design/36_selected_model.md"
  integration_md:   "${repo_root}/30_design/37_integration_choice.md"
  designreview_md:  "${repo_root}/30_design/38_design_review.md"

workflow:
  setup:
    - create_directories:
        paths:
          - "${repo_root}/30_design"
          - "${artifacts.prototypes_dir}"

  phases:
    - id: phase3_design
      name: "Phase 3 — Design"
      tasks:

        # ---- Step 3.1: Ideation Session ----
        - id: step_31_ideation
          description: Generate multiple bold alternatives beyond status quo.
          inputs:
            insights: "${artifacts.insights_md}"
          run:
            write_markdown:
              path: "${artifacts.ideation_md}"
              title: "Ideation Session"
              sections:
                - "Alternatives brainstormed: ≥${parameters.min_alternatives}"
                - "Source inspirations: insights, competitor patterns, blue ocean moves"
          gate:
            must_contain:
              path: "${artifacts.ideation_md}"
              substrings: ["Alternatives"]

        # ---- Step 3.2: Prototypes (Canvas Drafts) ----
        - id: step_32_prototypes
          depends_on: [step_31_ideation]
          description: Create prototype canvases for each alternative.
          run:
            write_markdown:
              path: "${artifacts.prototypes_md}"
              title: "Prototypes Summary"
              sections:
                - "Prototype A: Canvas + hypothesis"
                - "Prototype B: Canvas + hypothesis"
            write_markdown:
              path: "${artifacts.prototypes_dir}/prototype_A.md"
              title: "Prototype A Canvas"
              sections: ["Customer Segments: TBD","Value Proposition: TBD","Channels: TBD","Revenue: TBD"]
            write_markdown:
              path: "${artifacts.prototypes_dir}/prototype_B.md"
              title: "Prototype B Canvas"
              sections: ["Customer Segments: TBD","Value Proposition: TBD","Channels: TBD","Revenue: TBD"]
          gate:
            must_exist:
              - "${artifacts.prototypes_md}"

        # ---- Step 3.3: Narratives for Each Prototype ----
        - id: step_33_narratives
          depends_on: [step_32_prototypes]
          description: Write stories for each prototype.
          run:
            write_markdown:
              path: "${artifacts.narratives_md}"
              title: "Prototype Narratives"
              sections:
                - "Prototype A Story: problem → solution → why now"
                - "Prototype B Story: problem → solution → why now"
          gate:
            must_exist:
              - "${artifacts.narratives_md}"

        # ---- Step 3.4: Risk/Reward Profiles ----
        - id: step_34_riskreward
          depends_on: [step_33_narratives]
          description: Create risk/reward matrix for each prototype.
          run:
            write_csv:
              path: "${artifacts.riskreward_csv}"
              header: ["prototype","profit_potential","loss_risk","brand_impact","conflicts","customer_reaction","uncertainties"]
              rows:
                - ["A","high","medium","positive","low","favorable","pricing"]
                - ["B","medium","high","neutral","medium","uncertain","channel adoption"]
          gate:
            must_exist:
              - "${artifacts.riskreward_csv}"

        # ---- Step 3.5: Test Cards & Evidence Logging ----
        - id: step_35_testcards
          depends_on: [step_34_riskreward]
          description: Assign test cards to riskiest assumptions of each prototype.
          run:
            append_json:
              path: "${artifacts.testcards_json}"
              content:
                tests:
                  - prototype: "A"
                    assumption: "Customers pay $X"
                    test: "price interviews (n=5)"
                    metric: "≥3 accept"
                  - prototype: "B"
                    assumption: "Partners sign LOIs"
                    test: "2 partner LOIs"
                    metric: "≥1 signed"
            append_csv:
              path: "${artifacts.evidence_csv}"
              rows:
                - ["design","prototype A assumption","pending test","low","","design test","PM","today"]
          gate:
            json_schema:
              path: "${artifacts.testcards_json}"
              schema:
                type: object
                required: ["tests"]

        # ---- Step 3.6: Feedback Sessions ----
        - id: step_36_feedback
          depends_on: [step_35_testcards]
          description: Capture expert and customer feedback on prototypes.
          run:
            write_csv:
              path: "${artifacts.feedback_csv}"
              header: ["prototype","source","feedback","sentiment","implication"]
              rows:
                - ["A","customer","Too complex","negative","simplify"]
                - ["B","expert","Channel interest is strong","positive","pursue pilot"]
            append_csv:
              path: "${artifacts.evidence_csv}"
              rows:
                - ["feedback","prototype feedback","notes","medium","","inform scorecard","Analyst","today"]
          gate:
            must_exist:
              - "${artifacts.feedback_csv}"

        # ---- Step 3.7: Selection Scorecard ----
        - id: step_37_scorecard
          depends_on: [step_36_feedback]
          description: Score prototypes on desirability, feasibility, viability, and risk.
          run:
            write_markdown:
              path: "${artifacts.scorecard_md}"
              title: "Selection Scorecard"
              sections:
                - "| Prototype | Desirability | Feasibility | Viability | Risk | Weighted Score |"
                - "|-----------|-------------:|------------:|----------:|-----:|---------------:|"
                - "| A         | 7            | 6           | 8         | 5    | 0.72           |"
                - "| B         | 6            | 7           | 6         | 4    | 0.65           |"
          gate:
            must_contain:
              path: "${artifacts.scorecard_md}"
              substrings: ["Weighted Score"]

        # ---- Step 3.8: Select Model(s) ----
        - id: step_38_select
          depends_on: [step_37_scorecard]
          description: Select one or two prototypes that exceed threshold.
          run:
            write_markdown:
              path: "${artifacts.selected_md}"
              title: "Selected Prototype(s)"
              sections:
                - "Prototype A selected — score 0.72 (≥${parameters.selection_threshold})"
                - "Rationale: higher viability and customer validation"
          gate:
            must_exist:
              - "${artifacts.selected_md}"

        # ---- Step 3.9: Integration vs Separation Decision ----
        - id: step_39_integration
          depends_on: [step_38_select]
          description: Decide whether to integrate or separate from old business model.
          run:
            write_markdown:
              path: "${artifacts.integration_md}"
              title: "Integration vs Separation"
              sections:
                - "Decision: Separate entity"
                - "Rationale: reduces conflicts, allows speed"
          gate:
            must_exist:
              - "${artifacts.integration_md}"

        # ---- Step 3.10: Design Review ----
        - id: step_310_review
          depends_on: [step_39_integration]
          description: Summarize design phase and readiness for implementation.
          run:
            write_markdown:
              path: "${artifacts.designreview_md}"
              title: "Design Review"
              sections:
                - "What we tried: # of prototypes"
                - "What we learned: key insights & feedback"
                - "What we selected: chosen model(s)"
                - "Next steps: prep for implementation pilot"
          gate:
            must_exist:
              - "${artifacts.designreview_md}"

  acceptance:
    all_of:
      - exists: "${artifacts.ideation_md}"
      - exists: "${artifacts.prototypes_md}"
      - exists: "${artifacts.narratives_md}"
      - exists: "${artifacts.riskreward_csv}"
      - exists: "${artifacts.testcards_json}"
      - exists: "${artifacts.feedback_csv}"
      - exists: "${artifacts.scorecard_md}"
      - exists: "${artifacts.selected_md}"
      - exists: "${artifacts.integration_md}"
      - exists: "${artifacts.designreview_md}"
      - csv_min_rows:
          path: "${artifacts.evidence_csv}"
          min_rows: "${parameters.min_tests}"
