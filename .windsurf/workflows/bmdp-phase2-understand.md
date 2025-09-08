---
description: Understand for Business Model Design Process. Scans environment, studies customers, interviews experts, investigates prior failures, synthesizes insights, updates assumptions, and seeds early prototypes & tests.Emphasizes bias contro
auto_execution_mode: 1
---

name: bmdp_phase2_understand
version: "1.0"
parameters:
  repo_root:
    type: string
    default: "./bmdp"
  research_timebox_days:
    type: integer
    default: 10
  min_interviews:
    type: integer
    default: 8
  competitor_target_count:
    type: integer
    default: 5
  min_evidence_rows:
    type: integer
    default: 10

artifacts:
  # Inputs from prior phases
  canvas_v0_main:   "${repo_root}/10_mobilize/15_canvas_v0_main.md"
  evidence_csv:     "${repo_root}/common/evidence_ledger.csv"

  # Phase 2 outputs
  research_plan_md: "${repo_root}/20_understand/20_research_plan.md"
  questions_md:     "${repo_root}/20_understand/21_research_questions.md"
  env_scan_md:      "${repo_root}/20_understand/22_environment_scan.md"
  secondary_md:     "${repo_root}/20_understand/23_secondary_summary.md"
  competitors_csv:  "${repo_root}/20_understand/24_competitor_list.csv"
  competitors_md:   "${repo_root}/20_understand/24_competitor_canvases.md"
  segments_md:      "${repo_root}/20_understand/25_customer_segments.md"
  interview_guide:  "${repo_root}/20_understand/26_interview_guide.md"
  screener_md:      "${repo_root}/20_understand/27_screener.md"
  interviews_csv:   "${repo_root}/20_understand/28_interviews_log.csv"
  empathy_md:       "${repo_root}/20_understand/29_empathy_maps.md"
  jobs_md:          "${repo_root}/20_understand/30_jobs_to_be_done.md"
  insights_md:      "${repo_root}/20_understand/31_insights.md"
  assumptions_csv:  "${repo_root}/20_understand/32_assumption_backlog.csv"
  concepts_md:      "${repo_root}/20_understand/33_concept_cards.md"
  testcards_json:   "${repo_root}/20_understand/34_test_cards.json"
  failures_md:      "${repo_root}/20_understand/35_failure_analysis.md"
  experts_md:       "${repo_root}/20_understand/36_expert_panel_summary.md"
  biascheck_md:     "${repo_root}/20_understand/37_bias_check.md"
  progress_md:      "${repo_root}/20_understand/38_progress_demo.md"

workflow:
  setup:
    - create_directories:
        paths:
          - "${repo_root}/20_understand"

  phases:
    - id: phase2_understand
      name: "Phase 2 — Understand"
      tasks:

        # ---- Step 2.1: Research Plan & Timebox ----
        - id: step_21_research_plan
          description: Create plan tied to riskiest assumptions with explicit timebox and deliverables.
          run:
            write_markdown:
              path: "${artifacts.research_plan_md}"
              title: "Research Plan"
              sections:
                - "Timebox (days): ${parameters.research_timebox_days}"
                - "Objectives: Reduce uncertainty on top assumptions; avoid over-research"
                - "Deliverables: env_scan, segments, interviews, empathy/JTBD, insights, competitor canvases"
                - "Progress Demos: mid-sprint & end-of-sprint"
          gate:
            must_exist:
              - "${artifacts.research_plan_md}"

        # ---- Step 2.2: Research Questions & Hypotheses ----
        - id: step_22_questions
          depends_on: [step_21_research_plan]
          description: Define key questions mapped to assumptions and evidence types.
          run:
            write_markdown:
              path: "${artifacts.questions_md}"
              title: "Research Questions & Hypotheses"
              sections:
                - "Questions: market size, willingness to pay, adoption barriers, channel economics"
                - "Hypotheses: H1-Hn with pass/fail thresholds"
                - "Evidence Types: secondary, expert, customer, pilot signals"
          gate:
            must_contain:
              path: "${artifacts.questions_md}"
              substrings: ["Hypotheses", "Evidence Types"]

        # ---- Step 2.3: Environment Scan (PESTLE + Value Chain + Reg/Standards) ----
        - id: step_23_env_scan
          depends_on: [step_22_questions]
          description: Summarize macro forces, value chain actors, and key regulations/standards.
          run:
            write_markdown:
              path: "${artifacts.env_scan_md}"
              title: "Environment Scan"
              sections:
                - "PESTLE: Political, Economic, Social, Technological, Legal, Environmental"
                - "Value Chain: suppliers → producers → distributors → customers"
                - "Reg/Standards: certifications, quality, safety; emerging trends"
          gate:
            must_exist:
              - "${artifacts.env_scan_md}"

        # ---- Step 2.4: Secondary Research Summary & Evidence Ledger Entries ----
        - id: step_24_secondary
          depends_on: [step_23_env_scan]
          description: Capture top sources; append to evidence ledger.
          run:
            write_markdown:
              path: "${artifacts.secondary_md}"
              title: "Secondary Research Summary"
              sections:
                - "Top Sources: (list 5–10 credible market/tech/reg sources)"
                - "Key Data Points: prices, volumes, growth, benchmarks"
            append_csv:
              path: "${artifacts.evidence_csv}"
              rows:
                - ["secondary","market growth estimate","TBD datum","medium","","sizes TAM/SAM/SOM","Analyst","today"]
                - ["secondary","pricing corridor","TBD datum","high","","sets WTP prior","Analyst","today"]
          gate:
            must_exist:
              - "${artifacts.secondary_md}"

        # ---- Step 2.5: Competitor Mapping & Mini-Canvases ----
        - id: step_25_competitors
          depends_on: [step_24_secondary]
          description: List competitors and sketch their business model patterns.
          run:
            write_csv:
              path: "${artifacts.competitors_csv}"
              header: ["name","region","segment","notes"]
              rows:
                - ["TBD_1","TBD","TBD",""]
            write_markdown:
              path: "${artifacts.competitors_md}"
              title: "Competitor Canvases (Mini)"
              sections:
                - "Competitor 1 Canvas (mini): Segments, VP, Channels, Rev, Costs, Partners, Activities, Resources"
          gate:
            must_exist:
              - "${artifacts.competitors_csv}"
              - "${artifacts.competitors_md}"

        # ---- Step 2.6: Customer Segmentation Hypotheses ----
        - id: step_26_segments
          depends_on: [step_25_competitors]
          description: Propose initial segments + selection criteria.
          run:
            write_markdown:
              path: "${artifacts.segments_md}"
              title: "Customer Segmentation (Hypotheses)"
              sections:
                - "Segments: primary, secondary, exploratory"
                - "Selection Criteria: size, pain intensity, access, WTP"
          gate:
            must_exist:
              - "${artifacts.segments_md}"

        # ---- Step 2.7: Interview Toolkit (Guide + Screener) ----
        - id: step_27_interview_assets
          depends_on: [step_26_segments]
          description: Create interview guide and screener aligned to JTBD.
          run:
            write_markdown:
              path: "${artifacts.interview_guide}"
              title: "Interview Guide"
              sections:
                - "JTBD framing, past-behavior prompts, pricing probes"
            write_markdown:
              path: "${artifacts.screener_md}"
              title: "Interview Screener"
              sections:
                - "Inclusion/exclusion criteria; sample questions"
          gate:
            must_exist:
              - "${artifacts.interview_guide}"
              - "${artifacts.screener_md}"

        # ---- Step 2.8: Interviews Log ----
        - id: step_28_interviews_log
          depends_on: [step_27_interview_assets]
          description: Initialize interview log and capture early calls.
          run:
            write_csv:
              path: "${artifacts.interviews_csv}"
              header: ["date","segment","role","company","key_insights","quotes","followups"]
              rows:
                - ["TBD","TBD","TBD","TBD","pain point X","\"quote\"","next step"]
            append_csv:
              path: "${artifacts.evidence_csv}"
              rows:
                - ["customer","pain point X","interview note","medium","","refines VP","Research","today"]
          gate:
            must_exist:
              - "${artifacts.interviews_csv}"

        # ---- Step 2.9: Empathy Maps & JTBD ----
        - id: step_29_empathy_jtbd
          depends_on: [step_28_interviews_log]
          description: Convert interviews to empathy maps and JTBD statements.
          run:
            write_markdown:
              path: "${artifacts.empathy_md}"
              title: "Empathy Maps"
              sections:
                - "Segment A: Says/Thinks/Does/Feels"
            write_markdown:
              path: "${artifacts.jobs_md}"
              title: "Jobs To Be Done"
              sections:
                - "Functional, Social, Emotional jobs; pains; gains"
          gate:
            must_exist:
              - "${artifacts.empathy_md}"
              - "${artifacts.jobs_md}"

        # ---- Step 2.10: Insights Synthesis ----
        - id: step_210_insights
          depends_on: [step_29_empathy_jtbd]
          description: Synthesize patterns; produce top insights and contradictions.
          run:
            write_markdown:
              path: "${artifacts.insights_md}"
              title: "Insights Synthesis"
              sections:
                - "Top Themes (3–7)"
                - "Contradictions & Open Questions"
                - "Implications for Design"
          gate:
            must_contain:
              path: "${artifacts.insights_md}"
              substrings: ["Top Themes", "Implications for Design"]

        # ---- Step 2.11: Assumption Backlog & Prioritization (RICE/ICE) ----
        - id: step_211_assumptions
          depends_on: [step_210_insights]
          description: Create assumption backlog and prioritize by impact & evidence.
          run:
            write_csv:
              path: "${artifacts.assumptions_csv}"
              header: ["assumption","evidence","confidence","impact","priority_method","priority_score"]
              rows:
                - ["Customers pay X","weak","low","high","ICE","0.3"]
            append_csv:
              path: "${artifacts.evidence_csv}"
              rows:
                - ["synthesis","top assumptions identified","list","medium","","sets test focus","PM","today"]
          gate:
            must_exist:
              - "${artifacts.assumptions_csv}"

        # ---- Step 2.12: Early Prototypes (Concept Cards) & Test Cards ----
        - id: step_212_prototypes_tests
          depends_on: [step_211_assumptions]
          description: Create early concept cards and map top-3 assumptions to lean tests.
          run:
            write_markdown:
              path: "${artifacts.concepts_md}"
              title: "Concept Cards"
              sections:
                - "Concept A: proposition, who, channel, pricing hypothesis"
                - "Concept B: proposition, who, channel, pricing hypothesis"
            write_json:
              path: "${artifacts.testcards_json}"
              content:
                tests:
                  - assumption: "WTP >= $X"
                    test: "price interviews (n=5)"
                    metric: "≥3 accept"
                    stop_condition: "timebox or 2 fails"
                  - assumption: "Channel partner interest"
                    test: "2 partner calls"
                    metric: "≥1 LOI"
                    stop_condition: "timebox"
          gate: