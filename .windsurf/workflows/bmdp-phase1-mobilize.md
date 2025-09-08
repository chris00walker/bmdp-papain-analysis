---
description: Establishes legitimacy, frames objectives, assembles team, drafts v0 Canvas, runs kill/thrill, sets sprint plan, maps stakeholders, defines risks, and launches communications. Outputs are required before proceeding to Phase 2.
auto_execution_mode: 1
---

name: bmdp_phase1_mobilize
version: "1.0"
description: >
  

parameters:
  repo_root:
    type: string
    default: "./bmdp"
  sponsor_prompt:
    type: string
    required: true
  org_type:
    type: string
    enum: ["startup", "established"]
    required: true

artifacts:
  brief_md:          "${repo_root}/10_mobilize/10_brief.md"
  team_csv:          "${repo_root}/10_mobilize/11_team_roster.csv"
  access_csv:        "${repo_root}/10_mobilize/12_access_matrix.csv"
  orientation_md:    "${repo_root}/10_mobilize/13_orientation_brief.md"
  charter_md:        "${repo_root}/10_mobilize/14_mobilize_charter.md"
  canvas_main_md:    "${repo_root}/10_mobilize/15_canvas_v0_main.md"
  canvas_alt_md:     "${repo_root}/10_mobilize/15_canvas_v0_alt.md"
  stories_md:        "${repo_root}/10_mobilize/16_idea_stories.md"
  killthrill_csv:    "${repo_root}/10_mobilize/17_kill_thrill.csv"
  microtests_json:   "${repo_root}/10_mobilize/18_microtests.json"
  sprint_md:         "${repo_root}/10_mobilize/19_sprint_plan.md"
  stakeholders_csv:  "${repo_root}/10_mobilize/20_stakeholder_map.csv"
  risks_csv:         "${repo_root}/10_mobilize/21_risk_register.csv"
  comms_md:          "${repo_root}/10_mobilize/22_comms_plan.md"
  announce_md:       "${repo_root}/10_mobilize/23_announcement_onepager.md"
  evidence_csv:      "${repo_root}/common/evidence_ledger.csv"

workflow:
  setup:
    - create_directories:
        paths:
          - "${repo_root}/10_mobilize"

  phases:
    - id: phase1_mobilize
      name: "Phase 1 — Mobilize"
      tasks:

        # ---- Step 1.1: Confirm Legitimacy & Scope ----
        - id: step_11_brief
          description: Summarize sponsor, scope, decision cadence.
          inputs:
            sponsor_prompt: "${parameters.sponsor_prompt}"
          run:
            write_markdown:
              path: "${artifacts.brief_md}"
              title: "Mobilize Brief"
              sections:
                - "Sponsor Prompt: ${parameters.sponsor_prompt}"
                - "Scope: TBD"
                - "Decision Cadence: weekly | biweekly"
                - "Constraints: TBD"
          gate:
            must_exist:
              - "${artifacts.brief_md}"

        # ---- Step 1.2: Assemble Cross-Functional Team ----
        - id: step_12_team
          depends_on: [step_11_brief]
          description: Create roster and access matrix.
          run:
            write_csv:
              path: "${artifacts.team_csv}"
              header: ["name","role","function","allocation_pct","email"]
              rows:
                - ["TBD","Leader","Strategy","50%",""]
            write_csv:
              path: "${artifacts.access_csv}"
              header: ["data_source","owner","permission_status","ETA"]
              rows:
                - ["Customer interviews","TBD","pending","TBD"]
          gate:
            must_exist:
              - "${artifacts.team_csv}"
              - "${artifacts.access_csv}"

        # ---- Step 1.3: Orient Decision Makers ----
        - id: step_13_orientation
          depends_on: [step_12_team]
          description: Produce BMC primer with example + storytelling.
          run:
            write_markdown:
              path: "${artifacts.orientation_md}"
              title: "Orientation Brief"
              sections:
                - "Business Model Canvas 101"
                - "Example Canvas: TBD"
                - "Storytelling Template: Problem → Solution → Who → Why Now"
          gate:
            must_contain:
              path: "${artifacts.orientation_md}"
              substrings: ["Business Model Canvas"]

        # ---- Step 1.4: Frame Project Objectives ----
        - id: step_14_charter
          depends_on: [step_13_orientation]
          description: Translate objectives into measurable KPIs.
          run:
            write_markdown:
              path: "${artifacts.charter_md}"
              title: "Mobilize Charter"
              sections:
                - "Objectives: (list 3–5 SMART objectives)"
                - "KPIs: (measurable targets for Phases 1–3)"
                - "Constraints: (budget, time, resources)"
          gate:
            must_exist:
              - "${artifacts.charter_md}"

        # ---- Step 1.5: Draft v0 Business Model Canvas + Narrative ----
        - id: step_15_canvas
          depends_on: [step_14_charter]
          description: Create initial Canvas and narratives.
          run:
            write_markdown:
              path: "${artifacts.canvas_main_md}"
              title: "Business Model Canvas v0 (Main)"
              sections:
                - "Customer Segments: TBD"
                - "Value Proposition: TBD"
                - "Channels: TBD"
                - "Revenue Streams: TBD"
            write_markdown:
              path: "${artifacts.stories_md}"
              title: "Idea Stories"
              sections:
                - "Story 1: (problem, solution, who, why now, mechanics)"
          gate:
            must_exist:
              - "${artifacts.canvas_main_md}"
              - "${artifacts.stories_md}"

        # ---- Step 1.6: Kill/Thrill Session ----
        - id: step_16_killthrill
          depends_on: [step_15_canvas]
          description: Capture kill vs thrill reasons.
          run:
            write_csv:
              path: "${artifacts.killthrill_csv}"
              header: ["reason","polarity","theme","severity","evidence_link"]
              rows:
                - ["Customers may not pay","kill","market","high",""]
                - ["Scales globally","thrill","growth","medium",""]
          gate:
            must_exist:
              - "${artifacts.killthrill_csv}"

        # ---- Step 1.7: Preliminary Micro-tests ----
        - id: step_17_microtests
          depends_on: [step_16_killthrill]
          description: Define ≤2 light tests.
          run:
            write_json:
              path: "${artifacts.microtests_json}"
              content:
                microtests:
                  - assumption: "Customers will sign LOIs"
                    test: "Collect 5 LOIs"
                    metric: "≥5 LOIs"
                    owner: "BD Lead"
                  - assumption: "Target price acceptable"
                    test: "5 price interviews"
                    metric: "≥3 positive responses"
                    owner: "CFO"
            append_csv:
              path: "${artifacts.evidence_csv}"
              rows:
                - ["microtest","customers sign LOIs","assumption test","pending","","decision impact: go/no-go","BD Lead","today"]
          gate:
            must_exist:
              - "${artifacts.microtests_json}"

        # ---- Step 1.8: Sprint Plan ----
        - id: step_18_sprint
          depends_on: [step_17_microtests]
          description: Plan Understand and Design sprints.
          run:
            write_markdown:
              path: "${artifacts.sprint_md}"
              title: "Sprint Plan"
              sections:
                - "Duration: 4 weeks"
                - "Cadence: weekly standup, biweekly review"
                - "Deliverables: insights.md, alt canvases, tests, scorecard"
          gate:
            must_exist:
              - "${artifacts.sprint_md}"

        # ---- Step 1.9: Stakeholder Map ----
        - id: step_19_stakeholders
          depends_on: [step_18_sprint]
          description: Map vested interests and mitigations.
          run:
            write_csv:
              path: "${artifacts.stakeholders_csv}"
              header: ["stakeholder","interest","influence","stance","mitigation","owner"]
              rows:
                - ["BU Head","protect revenue","high","opposed","separate entity","Sponsor"]
          gate:
            must_exist:
              - "${artifacts.stakeholders_csv}"

        # ---- Step 1.10: Risk Register ----
        - id: step_110_risks
          depends_on: [step_19_stakeholders]
          description: Capture top-10 risks.
          run:
            write_csv:
              path: "${artifacts.risks_csv}"
              header: ["risk","likelihood","impact","trigger","mitigation","owner"]
              rows:
                - ["Overestimating idea","high","high","early excitement","kill/thrill checks","PMO"]
          gate:
            must_exist:
              - "${artifacts.risks_csv}"

        # ---- Step 1.11: Communications Plan ----
        - id: step_111_comms
          depends_on: [step_110_risks]
          description: Define internal comms plan and announcement.
          run:
            write_markdown:
              path: "${artifacts.comms_md}"
              title: "Comms Plan"
              sections:
                - "Audience: Execs, BU heads, team"
                - "Message: rationale + next steps"
                - "Channels: email, Slack, all-hands"
                - "Cadence: biweekly updates"
            write_markdown:
              path: "${artifacts.announce_md}"
              title: "Announcement One-Pager"
              sections:
                - "New Business Model Project: Why, What, How"
          gate:
            must_exist:
              - "${artifacts.comms_md}"
              - "${artifacts.announce_md}"

  acceptance:
    all_of:
      - exists: "${artifacts.brief_md}"
      - exists: "${artifacts.team_csv}"
      - exists: "${artifacts.access_csv}"
      - exists: "${artifacts.orientation_md}"
      - exists: "${artifacts.charter_md}"
      - exists: "${artifacts.canvas_main_md}"
      - exists: "${artifacts.stories_md}"
      - exists: "${artifacts.killthrill_csv}"
      - exists: "${artifacts.sprint_md}"
      - exists: "${artifacts.stakeholders_csv}"
      - exists: "${artifacts.risks_csv}"
      - exists: "${artifacts.comms_md}"
      - exists: "${artifacts.announce_md}"
      - csv_min_rows:
          path: "${artifacts.evidence_csv}"
          min_rows: 3
