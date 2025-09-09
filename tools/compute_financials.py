#!/usr/bin/env python3
"""
BMDP Financial Computation Tool
Computes IRR, NPV, ROI from cashflow data
"""

import argparse
import csv
import json
import numpy as np
from pathlib import Path
import sys

def compute_irr(cashflows):
    """Compute Internal Rate of Return using numpy"""
    try:
        return np.irr(cashflows) if hasattr(np, 'irr') else np.irr_fallback(cashflows)
    except:
        # Fallback IRR calculation
        return irr_newton_raphson(cashflows)

def irr_newton_raphson(cashflows, guess=0.1, precision=1e-6, max_iterations=100):
    """Newton-Raphson method for IRR calculation"""
    rate = guess
    for _ in range(max_iterations):
        npv = sum(cf / (1 + rate) ** i for i, cf in enumerate(cashflows))
        npv_derivative = sum(-i * cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cashflows))
        
        if abs(npv_derivative) < precision:
            break
            
        new_rate = rate - npv / npv_derivative
        if abs(new_rate - rate) < precision:
            return new_rate
        rate = new_rate
    return rate

def compute_npv(cashflows, discount_rate):
    """Compute Net Present Value"""
    return sum(cf / (1 + discount_rate) ** i for i, cf in enumerate(cashflows))

def compute_roi(cashflows):
    """Compute Return on Investment"""
    total_investment = sum(cf for cf in cashflows if cf < 0)
    total_returns = sum(cf for cf in cashflows if cf > 0)
    
    if total_investment == 0:
        return 0
    return (total_returns + total_investment) / abs(total_investment)

def main():
    parser = argparse.ArgumentParser(description='Compute financial metrics for BMDP business')
    parser.add_argument('--business', required=True, help='Business slug')
    parser.add_argument('--capital-min', type=float, default=300000, help='Minimum capital (BBD)')
    parser.add_argument('--capital-max', type=float, default=1000000, help='Maximum capital (BBD)')
    parser.add_argument('--discount-rate', type=float, default=0.15, help='Discount rate (decimal)')
    parser.add_argument('--repo-root', default='.', help='Repository root path')
    
    args = parser.parse_args()
    
    business_path = Path(args.repo_root) / "businesses" / args.business
    cashflow_path = business_path / "30_design" / "financials_cashflow.csv"
    
    if not cashflow_path.exists():
        print(f"❌ ERROR: Missing cashflow file: {cashflow_path}")
        sys.exit(1)
    
    # Read cashflow data
    try:
        with open(cashflow_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f"❌ ERROR: Cannot read cashflow file: {e}")
        sys.exit(1)
    
    # Build cashflow vector
    cashflows = []
    total_capex = 0
    
    for row in rows:
        try:
            capex = float(row.get('capex_bbd', 0))
            opex = float(row.get('opex_bbd', 0))
            revenues = float(row.get('revenues_bbd', 0))
            working_cap = float(row.get('working_cap_change_bbd', 0))
            
            # Cash flow = revenues - opex - capex - working_cap_change
            cf = revenues - opex - capex - working_cap
            cashflows.append(cf)
            total_capex += capex
            
        except ValueError as e:
            print(f"❌ ERROR: Invalid numeric data in row: {row}")
            sys.exit(1)
    
    # Validate capital bounds
    if total_capex < args.capital_min:
        print(f"❌ ERROR: Total CAPEX ({total_capex:,.0f} BBD) below minimum {args.capital_min:,.0f} BBD")
        sys.exit(1)
    elif total_capex > args.capital_max:
        print(f"❌ ERROR: Total CAPEX ({total_capex:,.0f} BBD) above maximum {args.capital_max:,.0f} BBD")
        sys.exit(1)
    
    # Compute metrics
    irr = compute_irr(cashflows)
    npv = compute_npv(cashflows, args.discount_rate)
    roi = compute_roi(cashflows)
    
    # Output results
    summary_path = business_path / "30_design" / "financials_summary.csv"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(summary_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['metric', 'value'])
        writer.writerow(['irr_pct', f"{irr:.4f}"])
        writer.writerow(['npv_bbd', f"{npv:.0f}"])
        writer.writerow(['roi_pct', f"{roi:.4f}"])
        writer.writerow(['discount_rate_pct', f"{args.discount_rate:.4f}"])
        writer.writerow(['horizon_years', len(cashflows)])
        writer.writerow(['capex_y0_bbd', f"{total_capex:.0f}"])
    
    print(f"✅ Financial metrics computed for {args.business}")
    print(f"   IRR: {irr:.1%}")
    print(f"   NPV: {npv:,.0f} BBD")
    print(f"   ROI: {roi:.1%}")
    print(f"   Results saved to: {summary_path}")

if __name__ == '__main__':
    main()
