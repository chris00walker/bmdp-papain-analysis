#!/usr/bin/env python3
"""
BMDP Portfolio Analysis Runner
Automates execution of analyze-portfolio workflow across all businesses
"""

import argparse
import subprocess
import sys
from pathlib import Path

# All businesses
ALL_BUSINESSES = ['grower', 'processor', 'distributor', 'marketplace']

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {description} failed with exit code {e.returncode}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run BMDP portfolio analysis')
    parser.add_argument('--businesses', nargs='+', choices=ALL_BUSINESSES,
                       default=ALL_BUSINESSES, help='Businesses to include in analysis')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show commands without executing')
    
    args = parser.parse_args()
    
    businesses = args.businesses
    
    print(f"🎯 Running portfolio analysis for: {', '.join(businesses)}")
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No commands will be executed")
    
    # Step 1: Validate all businesses
    print("\n=== STEP 1: VALIDATION ===")
    for business in businesses:
        cmd = f'python tools/validate.py --business {business}'
        desc = f'Validating {business}'
        
        if args.dry_run:
            print(f"DRY RUN: {desc}")
            print(f"  Command: {cmd}")
        else:
            if not run_command(cmd, desc):
                print(f"❌ Validation failed for {business}")
                return 1
    
    print("✅ All businesses validated")
    
    # Step 2: Compute financial metrics for all businesses
    print("\n=== STEP 2: FINANCIAL COMPUTATION ===")
    for business in businesses:
        cmd = f'python tools/compute_financials.py --business {business} --capital-min 300000 --capital-max 1000000 --discount-rate 0.15'
        desc = f'Computing financials for {business}'
        
        if args.dry_run:
            print(f"DRY RUN: {desc}")
            print(f"  Command: {cmd}")
        else:
            if not run_command(cmd, desc):
                print(f"❌ Financial computation failed for {business}")
                return 1
    
    print("✅ All financial metrics computed")
    
    # Step 3: Generate portfolio rollup
    print("\n=== STEP 3: PORTFOLIO ROLLUP ===")
    businesses_str = ' '.join(businesses)
    cmd = f'python tools/portfolio_rollup.py --businesses {businesses_str}'
    desc = 'Generating portfolio rollup'
    
    if args.dry_run:
        print(f"DRY RUN: {desc}")
        print(f"  Command: {cmd}")
    else:
        if not run_command(cmd, desc):
            return 1
    
    # Step 4: Display portfolio summary
    print("\n=== STEP 4: PORTFOLIO SUMMARY ===")
    if not args.dry_run:
        print("\n=== PORTFOLIO ANALYSIS SUMMARY ===")
        try:
            with open('90_portfolio_comparison/portfolio_analysis.md', 'r') as f:
                print(f.read())
        except FileNotFoundError:
            print("⚠️  Portfolio analysis file not found")
        
        print("\n=== DETAILED METRICS ===")
        try:
            cmd = "column -t -s',' 90_portfolio_comparison/financials_portfolio.csv"
            subprocess.run(cmd, shell=True, check=False)  # Don't fail if column command fails
        except Exception as e:
            print(f"⚠️  Could not format CSV table: {e}")
            # Fallback: just cat the file
            try:
                with open('90_portfolio_comparison/financials_portfolio.csv', 'r') as f:
                    print(f.read())
            except FileNotFoundError:
                print("⚠️  Portfolio CSV file not found")
    
    # Step 5: Update portfolio manifest
    print("\n=== STEP 5: PORTFOLIO MANIFEST ===")
    manifest_cmd = f'''python -c "
import json
from datetime import datetime
from pathlib import Path

portfolio_manifest = {{
    'analysis_type': 'portfolio_comparison',
    'businesses_analyzed': {businesses},
    'total_businesses': {len(businesses)},
    'analysis_date': datetime.now().isoformat() + 'Z',
    'validation_status': 'all_passed',
    'financial_computation': 'completed',
    'portfolio_rollup': 'completed',
    'output_files': [
        '90_portfolio_comparison/financials_portfolio.csv',
        '90_portfolio_comparison/portfolio_analysis.md'
    ]
}}

Path('90_portfolio_comparison').mkdir(exist_ok=True)
with open('90_portfolio_comparison/portfolio_manifest.json', 'w') as f:
    json.dump(portfolio_manifest, f, indent=2)

print('✅ Portfolio manifest created')
"'''
    
    if args.dry_run:
        print("DRY RUN: Creating portfolio manifest")
        print(f"  Command: {manifest_cmd}")
    else:
        if not run_command(manifest_cmd, 'Creating portfolio manifest'):
            return 1
    
    print(f"\n🎉 Portfolio analysis completed successfully!")
    print(f"📊 Results in: 90_portfolio_comparison/")
    print(f"📄 Analysis: 90_portfolio_comparison/portfolio_analysis.md")
    print(f"📈 Data: 90_portfolio_comparison/financials_portfolio.csv")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
