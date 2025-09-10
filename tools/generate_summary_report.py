#!/usr/bin/env python3
"""
Generate comprehensive business summary report
"""

import argparse
import json
import csv
from pathlib import Path

def generate_summary_report(business_slug: str):
    """Generate formatted business analysis summary"""
    business_path = Path(f"businesses/{business_slug}")
    
    # Read financial summary
    financials_path = business_path / "30_design" / "financials_summary.csv"
    manifest_path = business_path / "manifest.json"
    
    # Read data
    financials = {}
    if financials_path.exists():
        with open(financials_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                financials[row['metric']] = row['value']
    
    manifest = {}
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    
    # Generate report
    report_path = business_path / "analysis_summary.md"
    
    with open(report_path, 'w') as f:
        f.write(f"# Business Analysis Summary - {manifest.get('business_name', business_slug.title())}\n\n")
        
        # Executive Summary
        f.write("## Executive Summary\n\n")
        f.write(f"**Business**: {manifest.get('description', 'N/A')}\n")
        f.write(f"**Industry**: {manifest.get('industry', 'N/A')}\n")
        f.write(f"**Location**: {manifest.get('location', 'N/A')}\n")
        f.write(f"**Validation Status**: {manifest.get('validation_status', 'N/A')}\n\n")
        
        # Financial Metrics
        f.write("## Financial Performance\n\n")
        if 'irr_pct' in financials:
            irr_pct = float(financials['irr_pct']) * 100
            f.write(f"- **IRR**: {irr_pct:.1f}%\n")
        if 'npv_bbd' in financials:
            npv = float(financials['npv_bbd'])
            f.write(f"- **NPV**: {npv:,.0f} BBD\n")
        if 'roi_pct' in financials:
            roi_pct = float(financials['roi_pct']) * 100
            f.write(f"- **ROI**: {roi_pct:.1f}%\n")
        if 'discount_rate_pct' in financials:
            discount = float(financials['discount_rate_pct']) * 100
            f.write(f"- **Discount Rate**: {discount:.1f}%\n")
        if 'capex_y0_bbd' in financials:
            capex = float(financials['capex_y0_bbd'])
            f.write(f"- **Initial Investment**: {capex:,.0f} BBD\n")
        
        f.write("\n")
        
        # Key Metrics
        if 'key_metrics' in manifest:
            f.write("## Key Business Metrics\n\n")
            metrics = manifest['key_metrics']
            f.write(f"- **Target Customers**: {metrics.get('target_customers', 'N/A')}\n")
            f.write(f"- **Value Proposition**: {metrics.get('value_proposition', 'N/A')}\n")
            f.write(f"- **Competitive Advantage**: {metrics.get('competitive_advantage', 'N/A')}\n")
            f.write(f"- **Revenue Model**: {metrics.get('revenue_model', 'N/A')}\n\n")
        
        # Phase Completion
        if 'phases_completed' in manifest:
            f.write("## BMDP Phase Completion\n\n")
            phases = manifest['phases_completed']
            for phase in phases:
                f.write(f"- ✅ {phase.replace('_', ' ').title()}\n")
            f.write("\n")
        
        # Investment Analysis
        f.write("## Investment Analysis\n\n")
        if 'financial_summary' in manifest:
            fs = manifest['financial_summary']
            f.write(f"- **Break-even Timeline**: {fs.get('break_even_months', 'N/A')} months\n")
            f.write(f"- **Year 5 Revenue**: {fs.get('year_5_revenue', 0):,.0f} BBD\n")
            f.write(f"- **Year 5 Net Income**: {fs.get('year_5_net_income', 0):,.0f} BBD\n\n")
        
        f.write("## Recommendation\n\n")
        if float(financials.get('irr_pct', 0)) > 0.15:
            f.write("✅ **PROCEED** - Strong financial returns exceed hurdle rate\n")
        else:
            f.write("⚠️ **REVIEW** - Financial returns below expected threshold\n")
    
    print(f"✅ Business summary report generated: {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate business summary report")
    parser.add_argument("--business", required=True, help="Business slug")
    
    args = parser.parse_args()
    generate_summary_report(args.business)
