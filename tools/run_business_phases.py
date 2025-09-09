#!/usr/bin/env python3
"""
BMDP Business Phase Runner
Automates execution of Phase 0-3 workflows for a specific business
"""

import argparse
import subprocess
import sys
from pathlib import Path
# import re  # Not used, removing

# Business mappings
BUSINESS_MAP = {
    'grower': {'number': '1', 'brief': 'brief-1-grower.md'},
    'processor': {'number': '2', 'brief': 'brief-2-processor.md'},
    'distributor': {'number': '3', 'brief': 'brief-3-distributor.md'},
    'marketplace': {'number': '4', 'brief': 'brief-4-b2b-marketplace.md'}
}

PHASE_WORKFLOWS = [
    'bmdp-phase0-initiation.md',
    'bmdp-phase1-mobilize.md', 
    'bmdp-phase2-understand.md',
    'bmdp-phase3-design.md'
]

def substitute_parameters(content, business_slug, business_number):
    """Replace parameter placeholders with actual values"""
    content = content.replace('{business_slug}', business_slug)
    content = content.replace('{business_number}', business_number)
    content = content.replace('${business_slug}', business_slug)
    content = content.replace('${business_number}', business_number)
    return content

def extract_bash_commands(workflow_content):
    """Extract bash commands from workflow markdown"""
    commands = []
    in_bash_block = False
    current_command = []
    
    for line in workflow_content.split('\n'):
        if line.strip() == '```bash':
            in_bash_block = True
            current_command = []
        elif line.strip() == '```' and in_bash_block:
            if current_command:
                commands.append('\n'.join(current_command))
            in_bash_block = False
        elif in_bash_block and not line.strip().startswith('#'):
            # Skip comment lines but include actual commands
            if line.strip():
                current_command.append(line)
    
    return commands

def run_phase_workflow(phase_file, business_slug, business_number, dry_run=False):
    """Run a single phase workflow with parameter substitution"""
    workflow_path = Path('.windsurf/workflows') / phase_file
    
    if not workflow_path.exists():
        print(f"❌ ERROR: Workflow not found: {workflow_path}")
        return False
    
    print(f"\n🚀 Running {phase_file} for {business_slug}...")
    
    # Read and substitute parameters
    with open(workflow_path, 'r') as f:
        content = f.read()
    
    substituted_content = substitute_parameters(content, business_slug, business_number)
    
    # Extract bash commands
    commands = extract_bash_commands(substituted_content)
    
    if not commands:
        print(f"⚠️  No executable commands found in {phase_file}")
        return True
    
    # Execute commands
    for i, command in enumerate(commands, 1):
        print(f"\n📋 Step {i}: Executing command block...")
        if dry_run:
            print(f"DRY RUN: Would execute:\n{command}")
        else:
            try:
                result = subprocess.run(command, shell=True, check=True, 
                                      capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"❌ ERROR: Command failed with exit code {e.returncode}")
                if e.stderr:
                    print(f"Error output: {e.stderr}")
                return False
    
    print(f"✅ {phase_file} completed successfully")
    return True

def main():
    parser = argparse.ArgumentParser(description='Run BMDP Phase workflows for a business')
    parser.add_argument('business', choices=list(BUSINESS_MAP.keys()),
                       help='Business to run phases for')
    parser.add_argument('--phases', nargs='+', type=int, choices=[0,1,2,3],
                       default=[0,1,2,3], help='Phases to run (default: all)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show commands without executing')
    
    args = parser.parse_args()
    
    business_slug = args.business
    business_info = BUSINESS_MAP[business_slug]
    business_number = business_info['number']
    
    print(f"🎯 Running BMDP phases for: {business_slug} (#{business_number})")
    print(f"📁 Brief file: {business_info['brief']}")
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No commands will be executed")
    
    # Run selected phases
    success = True
    for phase_num in args.phases:
        workflow_file = PHASE_WORKFLOWS[phase_num]
        if not run_phase_workflow(workflow_file, business_slug, business_number, args.dry_run):
            success = False
            break
    
    if success:
        print(f"\n🎉 All phases completed successfully for {business_slug}!")
        print(f"💡 Next step: Run analysis with:")
        print(f"   python tools/run_business_analysis.py {business_slug}")
    else:
        print(f"\n❌ Phase execution failed for {business_slug}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
