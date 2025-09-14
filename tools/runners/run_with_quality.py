#!/usr/bin/env python3
"""
Run workflows with integrated quality assurance
Implements the Hybrid Parser-LLM Pipeline from the Solution Implementation Plan
"""

import subprocess
import sys
import json
from pathlib import Path
import argparse

def ensure_prerequisites(business):
    """Ensure all prerequisites exist for workflow execution"""
    business_path = Path(f'/home/chris/bmdp/businesses/{business}')
    business_path.mkdir(parents=True, exist_ok=True)
    
    # Create manifest if missing
    manifest_path = business_path / 'manifest.json'
    if not manifest_path.exists():
        manifest = {
            "business": business,
            "phase": 0,
            "status": "in_progress",
            "created": "2024-01-01",
            "validation": {}
        }
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"✅ Created manifest.json for {business}")
    
    return True

def run_workflow_phases(business, phases):
    """Run workflow phases for a business"""
    cmd = [
        'python', 'tools/runners/run_business_phases.py',
        business, '--phases'
    ] + [str(p) for p in phases]
    
    print(f"🚀 Running phases {phases} for {business}...")
    result = subprocess.run(cmd, cwd='/home/chris/bmdp')
    return result.returncode == 0

def fix_quality_issues(business):
    """Fix quality issues in workflow outputs"""
    cmd = [
        'python', 'tools/processors/workflow_output_fixer.py',
        '--business', business
    ]
    
    print(f"🔧 Fixing quality issues for {business}...")
    result = subprocess.run(cmd, cwd='/home/chris/bmdp', capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    return result.returncode == 0

def validate_quality(business):
    """Validate workflow output quality"""
    cmd = [
        'python', 'tools/validators/workflow_quality_assurance.py',
        '--business', business
    ]
    
    print(f"✅ Validating quality for {business}...")
    result = subprocess.run(cmd, cwd='/home/chris/bmdp', capture_output=True, text=True)
    print(result.stdout)
    return result.returncode == 0

def run_with_quality(business, phases):
    """Run workflow with integrated quality assurance"""
    print(f"\n{'='*60}")
    print(f"RUNNING {business.upper()} WITH QUALITY ASSURANCE")
    print(f"{'='*60}\n")
    
    # Step 1: Ensure prerequisites
    if not ensure_prerequisites(business):
        print(f"❌ Failed to set up prerequisites for {business}")
        return False
    
    # Step 2: Run workflow phases
    if not run_workflow_phases(business, phases):
        print(f"❌ Workflow execution failed for {business}")
        return False
    
    # Step 3: Fix quality issues
    if not fix_quality_issues(business):
        print(f"⚠️  Could not fix all quality issues for {business}")
    
    # Step 4: Validate final quality
    passed = validate_quality(business)
    
    if passed:
        print(f"\n✅ {business} completed with quality standards met")
    else:
        print(f"\n⚠️  {business} completed but has remaining quality issues")
    
    return passed

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Run BMDP workflows with quality assurance')
    parser.add_argument('--business', 
                       choices=['grower', 'processor', 'distributor', 'marketplace', 'all'],
                       default='all',
                       help='Business to process')
    parser.add_argument('--phases', nargs='+', type=int, 
                       default=[0, 1, 2, 3],
                       help='Phases to run (default: all)')
    
    args = parser.parse_args()
    
    if args.business == 'all':
        businesses = ['grower', 'processor', 'distributor', 'marketplace']
    else:
        businesses = [args.business]
    
    results = {}
    for business in businesses:
        success = run_with_quality(business, args.phases)
        results[business] = success
    
    # Summary
    print(f"\n{'='*60}")
    print("QUALITY ASSURANCE SUMMARY")
    print(f"{'='*60}")
    
    for business, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{business:15} {status}")
    
    # Overall status
    all_passed = all(results.values())
    if all_passed:
        print(f"\n🎉 All businesses meet quality standards!")
    else:
        print(f"\n⚠️  Some businesses have quality issues")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
