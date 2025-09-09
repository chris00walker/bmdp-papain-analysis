---
description: Analyze single business with financial automation and validation
---

# Analyze Single Business

Runs complete validation and financial analysis for one business. Replace `{business_slug}` with target business (grower, processor, distributor, marketplace).

## Prerequisites

- Business brief file exists with YAML frontmatter
- Business directory structure created
- Python tools available in `tools/` directory

## Steps

### 1. Validate business structure and data

```bash
python tools/validate.py --business {business_slug}
```

**Expected output**: ✅ VALIDATION PASSED

### 2. Compute financial metrics

```bash
python tools/compute_financials.py --business {business_slug} --capital-min 300000 --capital-max 1000000 --discount-rate 0.15
```

**Expected output**: 
- IRR, NPV, ROI calculations
- Results saved to `businesses/{business_slug}/30_design/financials_summary.csv`

### 3. Update business manifest

```bash
python -c "
import json
from pathlib import Path
from datetime import datetime

manifest_path = Path('businesses/{business_slug}/manifest.json')
if manifest_path.exists():
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    manifest['last_updated'] = datetime.now().isoformat() + 'Z'
    manifest['validation_status'] = 'passed'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f'✅ Manifest updated for {business_slug}')
"
```

### 4. Generate business summary report

```bash
echo '# Business Analysis Summary for {business_slug}' > businesses/{business_slug}/analysis_summary.md
echo '' >> businesses/{business_slug}/analysis_summary.md
echo '## Financial Metrics' >> businesses/{business_slug}/analysis_summary.md
cat businesses/{business_slug}/30_design/financials_summary.csv >> businesses/{business_slug}/analysis_summary.md
echo '' >> businesses/{business_slug}/analysis_summary.md
echo '## Validation Status' >> businesses/{business_slug}/analysis_summary.md
echo 'All validation checks passed ✅' >> businesses/{business_slug}/analysis_summary.md
```

## Success Criteria

- [ ] Validation passes without errors
- [ ] Financial metrics computed and saved
- [ ] Business manifest updated
- [ ] Summary report generated

## Troubleshooting

**Validation fails**: Check that all required files exist and have correct schemas
**Financial computation fails**: Verify `financials_cashflow.csv` exists and has valid numeric data
**Capital bounds error**: Ensure total CAPEX is between 300,000 and 1,000,000 BBD
