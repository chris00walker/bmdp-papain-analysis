#!/usr/bin/env python3
"""
Fix all BMDP workflows to have proper executable bash commands
"""

import re
from pathlib import Path

def fix_workflow(workflow_path):
    """Fix a single workflow file"""
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    # Fix tool paths
    replacements = [
        # Fix tool paths to use modular structure
        ('python tools/vpd_validator.py', 'python tools/validators/vpd_validator.py'),
        ('python tools/bmg_validator.py', 'python tools/validators/bmg_validator.py'),
        ('python tools/tbi_validator.py', 'python tools/validators/tbi_validator.py'),
        ('python tools/vpd_canvas_creator.py', 'python tools/generators/vpd_canvas_creator.py'),
        ('python tools/osterwalder_pigneur_scorer.py', 'python tools/validators/osterwalder_pigneur_scorer.py'),
        ('python tools/validate.py', 'python tools/validators/validate.py'),
        ('python tools/compute_financials.py', 'python tools/calculators/compute_financials.py'),
        ('python tools/content_validator.py', 'python tools/validators/content_validator.py'),
        ('python tools/update_manifest.py', 'python tools/core/update_manifest.py'),
        ('python tools/generate_summary_report.py', 'python tools/generators/generate_summary_report.py'),
        ('python tools/portfolio_rollup.py', 'python tools/calculators/portfolio_rollup.py'),
        
        # Fix parameter substitution
        ('{business_slug}', '$1'),
        ('${business_slug}', '$1'),
        ('{business_number}', '$2'),
        ('${business_number}', '$2'),
        
        # Fix businesses path
        ('businesses/$1', 'businesses/$1'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Save fixed workflow
    with open(workflow_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed: {workflow_path.name}")

def main():
    """Fix all workflows"""
    workflows_dir = Path('/home/chris/bmdp/.windsurf/workflows')
    
    # Fix all BMDP phase workflows
    for workflow in workflows_dir.glob('*.md'):
        if 'bmdp-phase' in workflow.name or 'analyze' in workflow.name:
            fix_workflow(workflow)
    
    print("\nAll workflows fixed!")
    print("\nNow you can run:")
    print("  python tools/runners/run_business_phases.py grower --phases 0 1 2 3")
    print("  python tools/runners/run_business_phases.py processor --phases 0 1 2 3")
    print("  python tools/runners/run_business_phases.py distributor --phases 0 1 2 3")
    print("  python tools/runners/run_business_phases.py marketplace --phases 0 1 2 3")

if __name__ == '__main__':
    main()
