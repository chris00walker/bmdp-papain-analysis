---
business_slug: grower
capital_bounds_bbd:
  min: 250000
  max: 1000000
financial_method:
  horizon_years: 3
  discount_rate_pct: 15
  roi_target_pct: 20
  metrics: [IRR, NPV, ROI]
project_execution:
  team_size: 4
  timeline_weeks: 52
  phase_ratios:
    discovery_pct: 50  # 3 parts of 6 total (3:2:1)
    validation_pct: 33  # 2 parts of 6 total
    scaling_pct: 17     # 1 part of 6 total
  budget_ratios:
    # Parser uses investor-realistic allocation (risk-inverse funding):
    # Discovery: 30% of initial capital (min $150K) - lean validation
    # Validation: 40% of unlocked capital (min $300K) - prove model  
    # Scaling: 50% of unlocked capital (min $400K) - aggressive growth
    # Actual percentages vary based on minimum thresholds and capital progression
  milestone_budget_unlocks:
    # Progressive capital unlocking based on validation milestones
    # Parser will calculate actual amounts using capital bounds and risk progression
  milestone_criteria:
    discovery_complete: "Customer desirability validated through interviews and market research"
    validation_complete: "Business feasibility proven through prototype testing and early sales"
    scaling_complete: "Business viability demonstrated through sustainable operations and growth"
assumptions_version: 1.0
updated_at: 2025-09-09
---

# **Brief 1: Grower (Papaya Cultivation & Crude Papain Production, Barbados)**

**Value Proposition**

* Supply reliable, traceable crude papain (dried latex) from Barbados.  
* Meet food-grade or feed-grade specifications at competitive cost.  
* Differentiate on transparency, local quality, and consistent potency.

**Customer Segments**

* International enzyme processors (India, US, EU).  
* Regional food processors seeking local papain.

**Key Activities**

* Orchard establishment (10–25 ha).  
* Latex tapping, drying, packaging.  
* Quality control (potency, microbial).

**Key Resources**

* Arable land (≥10 ha).  
* Skilled labor for tapping/drying.  
* Drying equipment & basic QA lab.

**Channels**

* Direct export contracts.  
* Regional distributors.  
* B2B platforms (as supplier).

**Revenue Streams**

* Crude papain sales: \~US $10–20/kg.  
* By-products (papaya fruit, seeds).

**Cost Structure**

* Land prep, irrigation, fertilizers.  
* Labor-intensive tapping.  
* Dryers, packaging, QC.

**Critical Risks**

* Weather dependency (drought, hurricanes).  
* Market price volatility.  
* Regulatory changes affecting organic certification.

---

## Glossary

**BMDP Budget**: Operational expenses for executing the Business Model Design Process - money spent on market research, customer interviews, prototype development, and validation activities.

**Business Capital**: Total funding available to operate the actual business - money for equipment, inventory, facilities, staff, and day-to-day operations.
