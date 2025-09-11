#!/usr/bin/env python3
"""
BMDP Workflow Checkpoint System
Provides automated validation checkpoints during AI workflow execution
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import argparse

class WorkflowCheckpoint:
    """Manages workflow execution checkpoints with automated validation"""
    
    def __init__(self, business: str):
        self.business = business
        self.business_path = Path(f"businesses/{business}")
        self.checkpoint_file = self.business_path / ".workflow_checkpoints.json"
        
    def load_checkpoints(self) -> Dict:
        """Load existing checkpoint data"""
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return {
            "business": self.business,
            "checkpoints": {},
            "current_phase": None,
            "last_validation": None
        }
    
    def save_checkpoints(self, data: Dict):
        """Save checkpoint data"""
        self.business_path.mkdir(parents=True, exist_ok=True)
        with open(self.checkpoint_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def validate_phase_completion(self, phase: str) -> Dict:
        """Validate that a phase is complete before proceeding"""
        print(f"\n🔍 CHECKPOINT: Validating {phase} completion for {self.business}")
        
        # Run validation
        result = subprocess.run([
            'python', 'tools/workflow_validator.py', 
            '--business', self.business,
            '--format', 'json'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Validation failed for {self.business}")
            return {"status": "failed", "compliance": 0}
        
        try:
            report = json.loads(result.stdout)
            phase_compliance = report["phases"].get(phase, {}).get("compliance_pct", 0)
            
            if phase_compliance < 100:
                print(f"⚠️  Phase {phase} incomplete: {phase_compliance:.1f}% compliant")
                
                # Auto-fix if possible
                print(f"🔧 Attempting auto-fix...")
                fix_result = subprocess.run([
                    'python', 'tools/workflow_enforcer.py',
                    '--business', self.business
                ], capture_output=True, text=True)
                
                if fix_result.returncode == 0:
                    print("✅ Auto-fix completed")
                    # Re-validate after fix
                    return self.validate_phase_completion(phase)
                else:
                    print("❌ Auto-fix failed")
                    return {"status": "incomplete", "compliance": phase_compliance}
            
            print(f"✅ Phase {phase} validation passed: {phase_compliance:.1f}% compliant")
            return {"status": "complete", "compliance": phase_compliance}
            
        except json.JSONDecodeError:
            print("❌ Failed to parse validation results")
            return {"status": "error", "compliance": 0}
    
    def record_checkpoint(self, phase: str, status: str, notes: str = ""):
        """Record a checkpoint completion"""
        data = self.load_checkpoints()
        
        data["checkpoints"][phase] = {
            "status": status,
            "timestamp": "2025-09-10T14:26:42-03:00",
            "notes": notes
        }
        data["current_phase"] = phase
        data["last_validation"] = "2025-09-10T14:26:42-03:00"
        
        self.save_checkpoints(data)
        print(f"📝 Checkpoint recorded: {phase} - {status}")
    
    def can_proceed_to_phase(self, target_phase: str) -> bool:
        """Check if we can proceed to target phase"""
        phase_order = ["00_initiation", "10_mobilize", "20_understand", "30_design"]
        
        if target_phase not in phase_order:
            return False
        
        target_index = phase_order.index(target_phase)
        
        # Check all previous phases are complete
        for i in range(target_index):
            prev_phase = phase_order[i]
            validation = self.validate_phase_completion(prev_phase)
            
            if validation["status"] != "complete":
                print(f"🚫 Cannot proceed to {target_phase}: {prev_phase} incomplete")
                return False
        
        return True
    
    def execute_phase_with_validation(self, phase: str, workflow_file: str) -> bool:
        """Execute a phase workflow with validation checkpoints"""
        print(f"\n🚀 EXECUTING: Phase {phase} for {self.business}")
        
        # Pre-execution validation
        if not self.can_proceed_to_phase(phase):
            return False
        
        # Record start
        self.record_checkpoint(phase, "started", f"Beginning {phase} execution")
        
        # Execute workflow (this would be called by AI)
        print(f"📋 Ready to execute workflow: {workflow_file}")
        print(f"⚠️  AI should now execute the workflow with parameter substitution:")
        print(f"   - Replace {{business_slug}} with '{self.business}'")
        print(f"   - Follow all deliverable requirements exactly")
        print(f"   - Create all files with exact naming conventions")
        
        # Post-execution validation will be called separately
        return True
    
    def post_execution_validation(self, phase: str) -> bool:
        """Validate phase after AI execution"""
        print(f"\n🔍 POST-EXECUTION: Validating {phase} for {self.business}")
        
        validation = self.validate_phase_completion(phase)
        
        if validation["status"] == "complete":
            self.record_checkpoint(phase, "completed", f"Phase {phase} successfully completed")
            return True
        else:
            self.record_checkpoint(phase, "failed", f"Phase {phase} validation failed: {validation['compliance']:.1f}% compliant")
            return False
    
    def get_status_report(self) -> Dict:
        """Get current workflow status"""
        data = self.load_checkpoints()
        
        # Get current compliance
        result = subprocess.run([
            'python', 'tools/workflow_validator.py',
            '--business', self.business,
            '--format', 'json'
        ], capture_output=True, text=True)
        
        current_compliance = 0
        if result.returncode == 0:
            try:
                report = json.loads(result.stdout)
                current_compliance = report.get("overall_compliance", 0)
            except:
                pass
        
        return {
            "business": self.business,
            "current_compliance": current_compliance,
            "checkpoints": data.get("checkpoints", {}),
            "current_phase": data.get("current_phase"),
            "last_validation": data.get("last_validation")
        }

def main():
    parser = argparse.ArgumentParser(description="BMDP Workflow Checkpoint Management")
    parser.add_argument("--business", required=True, help="Business name")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate phase completion")
    validate_parser.add_argument("--phase", required=True, help="Phase to validate")
    
    # Execute command
    execute_parser = subparsers.add_parser("execute", help="Execute phase with validation")
    execute_parser.add_argument("--phase", required=True, help="Phase to execute")
    execute_parser.add_argument("--workflow", required=True, help="Workflow file to execute")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Get workflow status")
    
    # Post-validate command
    post_parser = subparsers.add_parser("post-validate", help="Post-execution validation")
    post_parser.add_argument("--phase", required=True, help="Phase to validate")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    checkpoint = WorkflowCheckpoint(args.business)
    
    if args.command == "validate":
        result = checkpoint.validate_phase_completion(args.phase)
        return 0 if result["status"] == "complete" else 1
    
    elif args.command == "execute":
        success = checkpoint.execute_phase_with_validation(args.phase, args.workflow)
        return 0 if success else 1
    
    elif args.command == "post-validate":
        success = checkpoint.post_execution_validation(args.phase)
        return 0 if success else 1
    
    elif args.command == "status":
        status = checkpoint.get_status_report()
        print(json.dumps(status, indent=2))
        return 0
    
    return 1

if __name__ == "__main__":
    exit(main())
