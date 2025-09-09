#!/usr/bin/env python3
"""
BMDP Portfolio Rollup Tool
Aggregates financial metrics across all businesses
"""

import argparse
import csv
import json
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(description='Generate portfolio rollup from business financials')
    parser.add_argument('--repo-root', default='.', help='Repository root path')
    parser.add_argument('--businesses', nargs='+', default=['grower', 'processor', 'distributor', 'marketplace'], 
                       help='Business slugs to include')
    
    args = parser.parse_args()
    
    repo_root = Path(args.repo_root)
    portfolio_data = []
    
    # Collect data from each business
    for business in args.businesses:
        summary_path = repo_root / "businesses" / business / "30_design" / "financials_summary.csv"
        
        if not summary_path.exists():
            print(f"⚠️  WARNING: Missing financial summary for {business}: {summary_path}")
            continue
            
        try:
            with open(summary_path, 'r') as f:
                reader = csv.DictReader(f)
                metrics = {row['metric']: row['value'] for row in reader}
                
            portfolio_data.append({
                'business_slug': business,
                'irr_pct': float(metrics.get('irr_pct', 0)),
                'npv_bbd': float(metrics.get('npv_bbd', 0)),
                'roi_pct': float(metrics.get('roi_pct', 0)),
                'capex_y0_bbd': float(metrics.get('capex_y0_bbd', 0))
            })
            
        except Exception as e:
            print(f"❌ ERROR: Cannot read financial summary for {business}: {e}")
            continue
    
    if not portfolio_data:
        print("❌ ERROR: No valid financial data found for any business")
        sys.exit(1)
    
    # Create output directory
    output_dir = repo_root / "90_portfolio_comparison"
    output_dir.mkdir(exist_ok=True)
    
    # Write portfolio CSV
    portfolio_csv = output_dir / "financials_portfolio.csv"
    with open(portfolio_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['business_slug', 'irr_pct', 'npv_bbd', 'roi_pct', 'capex_y0_bbd'])
        writer.writeheader()
        writer.writerows(portfolio_data)
    
    # Generate analysis markdown
    portfolio_data.sort(key=lambda x: x['irr_pct'], reverse=True)
    
    analysis_md = output_dir / "portfolio_analysis.md"
    with open(analysis_md, 'w') as f:
        f.write("---\n")
        f.write("title: Portfolio Financial Analysis\n")
        f.write("generated_by: portfolio_rollup.py\n")
        f.write("date: auto-generated\n")
        f.write("---\n\n")
        
        f.write("# Portfolio Financial Analysis\n\n")
        
        f.write("## Financial Metrics Summary\n\n")
        f.write("| Business | IRR | NPV (BBD) | ROI | CAPEX (BBD) |\n")
        f.write("|----------|-----|-----------|-----|-------------|\n")
        
        total_npv = 0
        total_capex = 0
        
        for data in portfolio_data:
            f.write(f"| {data['business_slug'].title()} | {data['irr_pct']:.1%} | {data['npv_bbd']:,.0f} | {data['roi_pct']:.1%} | {data['capex_y0_bbd']:,.0f} |\n")
            total_npv += data['npv_bbd']
            total_capex += data['capex_y0_bbd']
        
        f.write(f"| **TOTAL** | - | **{total_npv:,.0f}** | - | **{total_capex:,.0f}** |\n\n")
        
        f.write("## Ranking by IRR\n\n")
        for i, data in enumerate(portfolio_data, 1):
            f.write(f"{i}. **{data['business_slug'].title()}**: {data['irr_pct']:.1%} IRR, {data['npv_bbd']:,.0f} BBD NPV\n")
        
        f.write(f"\n## Portfolio Totals\n\n")
        f.write(f"- **Total Investment Required**: {total_capex:,.0f} BBD\n")
        f.write(f"- **Total Portfolio NPV**: {total_npv:,.0f} BBD\n")
        f.write(f"- **Number of Businesses**: {len(portfolio_data)}\n")
        
        # Investment efficiency
        if total_capex > 0:
            npv_per_bbd = total_npv / total_capex
            f.write(f"- **NPV per BBD Invested**: {npv_per_bbd:.2f}\n")
    
    print(f"✅ Portfolio rollup completed")
    print(f"   Businesses analyzed: {len(portfolio_data)}")
    print(f"   Total portfolio NPV: {total_npv:,.0f} BBD")
    print(f"   Total investment: {total_capex:,.0f} BBD")
    print(f"   Results saved to: {output_dir}")

if __name__ == '__main__':
    main()
