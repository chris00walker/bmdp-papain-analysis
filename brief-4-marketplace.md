---
business_slug: marketplace
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

# **Brief 4: B2B Marketplace (Digital Platform for Papain Trade, Barbados)**

## Value Proposition

* Neutral digital marketplace connecting papain growers, processors, distributors with buyers worldwide.  
* Reduce search, verification, and transaction costs.  
* Provide escrow, certification badges, and integrated logistics.

## Customer Segments

* Papain buyers (food, pharma, cosmetics, feed industries).  
* Papain suppliers (growers, processors, distributors).  
* Logistics/QA providers who want exposure.

## Key Activities

* Platform development (search, escrow, dashboards).  
* Supplier verification & certification.  
* Marketing to create network liquidity.

## Key Resources

* Web/app platform (MERN \+ marketplace plugins).  
* QA verification partners.  
* Escrow/payment gateway.

## Channels

* Online platform (global).  
* SEO/SEM targeting enzyme buyers.  
* Partnerships with trade associations.

## Revenue Streams

* Transaction fee (5–10%).  
* Premium listings & certification fees.  
* Logistics/finance add-ons.

## Cost Structure

* Platform build (BDS $50k - $75k).  
* Ongoing hosting, dev, marketing (BDS $10k - $20k).  
* Verification & escrow operations.

## Critical Risks

* Network effects (chicken-egg problem).  
* Trust & verification challenges.  
* Competition from established platforms.

---

## Glossary

**BMDP Budget**: Operational expenses for executing the Business Model Design Process - money spent on market research, customer interviews, prototype development, and validation activities.

**Business Capital**: Total funding available to operate the actual business - money for equipment, inventory, facilities, staff, and day-to-day operations.
