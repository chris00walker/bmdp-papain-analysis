---
description: Analyze single business with financial automation and validation
---

# Analyze Single Business

Runs complete validation, financial computation, and manifest update for a specific business. Use this workflow after completing Phase 0-3 for a business.

**IMPORTANT**: Replace `{business_slug}` with actual business name (grower, processor, distributor, or marketplace) before running commands.

## Prerequisites

- Business slug (grower, processor, distributor, marketplace)
- Phase 3 completed with `financials_cashflow.csv` created
- Business manifest exists

## Steps

### 1. Validate business structure and data

```bash
# Replace {business_slug} with: grower, processor, distributor, or marketplace
python tools/validate.py --business {business_slug}
```

**Expected output**: VALIDATION PASSED

### 2. Compute financial metrics

```bash
# Replace {business_slug} with: grower, processor, distributor, or marketplace
python tools/compute_financials.py --business {business_slug} --capital-min 300000 --capital-max 1000000 --discount-rate 0.15
```

**Expected output**:

- IRR, NPV, ROI calculations
- Results saved to `businesses/{business_slug}/30_design/financials_summary.csv`

### 3. Methodology compliance assessment (VPD/BMG/TBI)

```bash
# VPD/BMG/TBI methodology compliance scoring (summary)
python tools/osterwalder_pigneur_scorer.py --business {business_slug} --format summary

# Content-level methodology checks (VPD/BMG/TBI heuristics)
python tools/content_validator.py --business {business_slug} --analysis semantic --mode all --format summary
```

**Expected output**:

- VPD/BMG/TBI sub-scores and overall methodology score
- Content validation messages for VPD/BMG/TBI artifacts

### 4. Update business manifest

```bash
# Replace {business_slug} with: grower, processor, distributor, or marketplace
python tools/update_manifest.py --business {business_slug} --validation-status passed
```

### 5. Generate business summary report

```bash
# Replace {business_slug} with: grower, processor, distributor, or marketplace
python tools/generate_summary_report.py --business {business_slug}
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
