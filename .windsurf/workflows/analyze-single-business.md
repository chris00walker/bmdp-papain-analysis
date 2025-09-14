---
description: Analyze single business with financial automation and validation
---

# Analyze Single Business

Runs complete validation, financial computation, and manifest update for a specific business. Use this workflow after completing Phase 0-3 for a business.

**IMPORTANT**: Replace `$1` with actual business name (grower, processor, distributor, or marketplace) before running commands.

## Prerequisites

- Business slug (grower, processor, distributor, marketplace)
- Phase 3 completed with `financials_cashflow.csv` created
- Business manifest exists

## Steps

### 1. Validate business structure and data

```bash
# Replace $1 with: grower, processor, distributor, or marketplace
python tools/validators/validate.py --business $1
```

**Expected output**: VALIDATION PASSED

### 2. Compute financial metrics

```bash
# Replace $1 with: grower, processor, distributor, or marketplace
python tools/calculators/compute_financials.py --business $1 --capital-min 300000 --capital-max 1000000 --discount-rate 0.15
```

**Expected output**:

- IRR, NPV, ROI calculations
- Results saved to `businesses/$1/30_design/financials_summary.csv`

### 3. Methodology compliance assessment (VPD/BMG/TBI)

```bash
# VPD/BMG/TBI methodology compliance scoring (summary)
python tools/validators/osterwalder_pigneur_scorer.py --business $1 --format summary

# Content-level methodology checks (VPD/BMG/TBI heuristics)
python tools/validators/content_validator.py --business $1 --analysis semantic --mode all --format summary
```

**Expected output**:

- VPD/BMG/TBI sub-scores and overall methodology score
- Content validation messages for VPD/BMG/TBI artifacts

### 4. Update business manifest

```bash
# Replace $1 with: grower, processor, distributor, or marketplace
python tools/core/update_manifest.py --business $1 --validation-status passed
```

### 5. Generate business summary report

```bash
# Replace $1 with: grower, processor, distributor, or marketplace
python tools/generators/generate_summary_report.py --business $1
```

**Expected output**: Formatted analysis summary with financial metrics, validation status, and key insights

## Success Criteria

- [ ] Validation passes without errors
- [ ] Financial metrics computed and saved
- [ ] Methodology compliance assessment executed (VPD/BMG/TBI)
- [ ] Business manifest updated
- [ ] Summary report generated

## Troubleshooting

**Validation fails**: Check that all required files exist and have correct schemas
**Financial computation fails**: Verify `financials_cashflow.csv` exists and has valid numeric data
**Capital bounds error**: Ensure total CAPEX is between 300,000 and 1,000,000 BBD
