---
business_slug: distributor
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

# **Brief 3: Distributor (Import/Export & Regional Distribution, Barbados)**

## Value Proposition

* One-stop Caribbean distributor offering crude, food-grade, and pharma-grade papain.  
* Lower transaction costs for local/regional buyers.  
* Provide CoA, quality assurance, and logistics support.

## Customer Segments

* Caribbean and Latin American food & beverage companies.  
* Cosmetics manufacturers.  
* Regional pharma distributors.

## Key Activities

* Source papain globally (India, China, Africa).  
* Quality verification and repackaging.  
* Sales, marketing, logistics.

## Key Resources

* Warehousing in Barbados.  
* QA lab for testing.  
* Supply contracts with multiple producers.

## Channels

* Direct B2B sales to processors.  
* Distribution partnerships.  
* Regional trade shows.

## Revenue Streams

* Mark-up on papain sales (15–25%).  
* Premium for guaranteed specs / smaller lot sizes.

## Cost Structure

* Working capital for inventory.  
* Freight, duties, warehousing.  
* Sales & admin overhead.

## Critical Risks

* Supplier reliability (quality, consistency).  
* Regulatory compliance across markets.  
* Competition from established distributors.

---

## Glossary

**BMDP Budget**: Operational expenses for executing the Business Model Design Process - money spent on market research, customer interviews, prototype development, and validation activities.

**Business Capital**: Total funding available to operate the actual business - money for equipment, inventory, facilities, staff, and day-to-day operations.
