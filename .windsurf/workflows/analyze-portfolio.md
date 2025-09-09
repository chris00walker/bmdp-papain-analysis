---
description: Analyze all businesses and generate portfolio comparison with automated rollup
---

# Analyze Portfolio

Runs complete analysis across all businesses and generates automated portfolio comparison. Executes validation, financial computation, and rollup for systematic decision-making.

## Prerequisites

- All business brief files exist with YAML frontmatter
- Business directory structures created
- Python automation tools available

## Steps

### 1. Validate all businesses

```bash
echo "Validating all businesses..."
for business in grower processor distributor marketplace; do
  echo "Validating $business..."
  python tools/validate.py --business $business
  if [ $? -ne 0 ]; then
    echo "❌ Validation failed for $business"
    exit 1
  fi
done
echo "✅ All businesses validated"
```

### 2. Compute financial metrics for all businesses

```bash
echo "Computing financial metrics..."
for business in grower processor distributor marketplace; do
  echo "Computing financials for $business..."
  python tools/compute_financials.py --business $business --capital-min 300000 --capital-max 1000000 --discount-rate 0.15
  if [ $? -ne 0 ]; then
    echo "❌ Financial computation failed for $business"
    exit 1
  fi
done
echo "✅ All financial metrics computed"
```

### 3. Generate portfolio rollup

```bash
python tools/portfolio_rollup.py --businesses grower processor distributor marketplace
```

**Expected output**:
- `90_portfolio_comparison/financials_portfolio.csv`
- `90_portfolio_comparison/portfolio_analysis.md`

### 4. Display portfolio summary

```bash
echo ""
echo "=== PORTFOLIO ANALYSIS SUMMARY ==="
echo ""
cat 90_portfolio_comparison/portfolio_analysis.md
echo ""
echo "=== DETAILED METRICS ==="
echo ""
column -t -s',' 90_portfolio_comparison/financials_portfolio.csv
```

### 5. Update portfolio manifest

```bash
python -c "
import json
from datetime import datetime
from pathlib import Path

portfolio_manifest = {
    'analysis_type': 'portfolio_comparison',
    'businesses_analyzed': ['grower', 'processor', 'distributor', 'marketplace'],
    'total_businesses': 4,
    'analysis_date': datetime.now().isoformat() + 'Z',
    'validation_status': 'all_passed',
    'financial_computation': 'completed',
    'portfolio_rollup': 'completed',
    'output_files': [
        '90_portfolio_comparison/financials_portfolio.csv',
        '90_portfolio_comparison/portfolio_analysis.md'
    ]
}

Path('90_portfolio_comparison').mkdir(exist_ok=True)
with open('90_portfolio_comparison/portfolio_manifest.json', 'w') as f:
    json.dump(portfolio_manifest, f, indent=2)

print('✅ Portfolio manifest created')
"
```

## Success Criteria

- [ ] All 4 businesses validate successfully
- [ ] Financial metrics computed for all businesses
- [ ] Portfolio rollup generated with rankings
- [ ] Portfolio analysis markdown created
- [ ] Portfolio manifest updated

## Expected Outputs

1. **Individual Business Outputs**:
   - `businesses/{slug}/30_design/financials_summary.csv`
   - Updated `businesses/{slug}/manifest.json`

2. **Portfolio Outputs**:
   - `90_portfolio_comparison/financials_portfolio.csv`
   - `90_portfolio_comparison/portfolio_analysis.md`
   - `90_portfolio_comparison/portfolio_manifest.json`

## Troubleshooting

**Business validation fails**: Check individual business with `/analyze-single-business`
**Missing financial data**: Ensure `financials_cashflow.csv` exists for each business
**Portfolio rollup fails**: Verify all `financials_summary.csv` files were generated
**Capital bounds violations**: Check that all businesses stay within 300K-1M BBD range
