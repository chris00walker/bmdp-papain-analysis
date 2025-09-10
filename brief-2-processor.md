---
business_slug: processor
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

# **Brief 2: Processor (Pharma-Grade Papain Refining, Barbados)**

**Value Proposition**

* Produce ≥6,000 USP U/mg papain powder, sterile and GMP-certified.  
* Offer Caribbean-based, Western-regulated quality alternative to Asian suppliers.  
* Enable pharma & cosmetic buyers to source closer to Western markets.

**Customer Segments**

* Pharmaceutical ingredient distributors (Merck, Mitsubishi, Sigma).  
* Wound care, nutraceutical, cosmetics companies.

**Key Activities**

* Purification: ultrafiltration, chromatography, lyophilisation.  
* Quality & regulatory compliance (GMP, HACCP, CoA).  
* Packaging and sterile handling.

**Key Resources**

* 25+ ha high-latex orchards (or secure crude supply).  
* GMP-compliant facility (≈BDS $1.5–2M CAPEX).  
* Skilled technicians & QA lab.

**Channels**

* Direct to pharma distributors.  
* Partnerships with global traders.  
* Export agents.

**Revenue Streams**

* Pharma-grade papain (US $60–90/kg).  
* Custom grades (sterile, high-activity).

**Cost Structure**

* High CAPEX amortisation.  
* Utilities, skilled labour, QC.  
* Regulatory audits.

**Critical Risks**

* Scale mismatch (10 ha too small; ≥16 ha baseline).  
* High fixed costs vs fluctuating demand.  
* Regulatory hurdles (FDA, EMA).

---

## Glossary

**BMDP Budget**: Operational expenses for executing the Business Model Design Process - money spent on market research, customer interviews, prototype development, and validation activities.

**Business Capital**: Total funding available to operate the actual business - money for equipment, inventory, facilities, staff, and day-to-day operations.
