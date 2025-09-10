#!/usr/bin/env python3
"""
BMDP Business Analysis Runner
Automates execution of analyze-single-business workflow
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Business mappings
BUSINESS_MAP = {
    'grower': {'number': '1', 'brief': 'brief-1-grower.md'},
    'processor': {'number': '2', 'brief': 'brief-2-processor.md'},
    'distributor': {'number': '3', 'brief': 'brief-3-distributor.md'},
    'marketplace': {'number': '4', 'brief': 'brief-4-b2b-marketplace.md'}
}

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
    parser = argparse.ArgumentParser(description='Run BMDP business analysis')
    parser.add_argument('business', choices=list(BUSINESS_MAP.keys()),
                       help='Business to analyze')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show commands without executing')
    
    args = parser.parse_args()
    
    business_slug = args.business
    business_info = BUSINESS_MAP[business_slug]
    
    print(f"🎯 Running analysis for: {business_slug}")
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No commands will be executed")
    
    # Analysis steps with parameter substitution
    steps = [
        {
            'cmd': f'python tools/validate.py --business {business_slug}',
            'desc': 'Validating business structure and data'
        },
        {
            'cmd': f'python tools/compute_financials.py --business {business_slug} --capital-min 300000 --capital-max 1000000 --discount-rate 0.15',
            'desc': 'Computing financial metrics'
        },
        {
            'cmd': f'python tools/update_manifest.py --business {business_slug} --validation-status passed',
            'desc': 'Updating business manifest'
        },
        {
            'cmd': f'echo "# Business Analysis Summary for {business_slug}" > businesses/{business_slug}/analysis_summary.md',
            'desc': 'Creating summary report header'
        },
        {
            'cmd': f'echo "" >> businesses/{business_slug}/analysis_summary.md',
            'desc': 'Adding blank line'
        },
        {
            'cmd': f'echo "## Financial Metrics" >> businesses/{business_slug}/analysis_summary.md',
            'desc': 'Adding financial metrics section'
        },
        {
            'cmd': f'cat businesses/{business_slug}/30_design/financials_summary.csv >> businesses/{business_slug}/analysis_summary.md',
            'desc': 'Adding financial data to summary'
        },
        {
            'cmd': f'echo "" >> businesses/{business_slug}/analysis_summary.md',
            'desc': 'Adding blank line'
        },
        {
            'cmd': f'echo "## Validation Status" >> businesses/{business_slug}/analysis_summary.md',
            'desc': 'Adding validation section'
        },
        {
            'cmd': f'echo "All validation checks passed ✅" >> businesses/{business_slug}/analysis_summary.md',
            'desc': 'Adding validation status'
        }
    ]
    
    # Execute all steps
    success = True
    for step in steps:
        if args.dry_run:
            print(f"DRY RUN: {step['desc']}")
            print(f"  Command: {step['cmd']}")
        else:
            if not run_command(step['cmd'], step['desc']):
                success = False
                break
    
    if success:
        print(f"\n🎉 Analysis completed successfully for {business_slug}!")
        print(f"📄 Summary report: businesses/{business_slug}/analysis_summary.md")
        print(f"📊 Financial metrics: businesses/{business_slug}/30_design/financials_summary.csv")
    else:
        print(f"\n❌ Analysis failed for {business_slug}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
