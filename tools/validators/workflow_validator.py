#!/usr/bin/env python3
"""
BMDP Workflow Compliance Validator
Ensures automated compliance for AI workflow execution
"""

import os
import json
import csv
from pathlib import Path
from typing import Dict, List, Set, Tuple
import argparse

class WorkflowValidator:
    """Validates BMDP workflow deliverable compliance"""
    
    def __init__(self, business_path: str):
        self.business_path = Path(business_path)
        self.business_name = self.business_path.name
        
        # Define required deliverables per phase
        self.phase_requirements = {
            "00_initiation": [
                "00_sponsor_brief.md",
                "01_project_charter.md", 
                "02_resource_plan.md",
                "03_readiness_assessment.md"
            ],
            "10_mobilize": [
                "10_brief.md", "11_team_roster.csv", "12_access_matrix.csv",
                "13_orientation_brief.md", "14_mobilize_charter.md", 
                "15_canvas_v0_main.md", "16_idea_stories.md", "17_kill_thrill.csv",
                "18_microtests.json", "19_sprint_plan.md", "20_stakeholder_map.csv",
                "21_risk_register.csv", "22_comms_plan.md", "23_announcement_onepager.md"
            ],
            "20_understand": [
                "20_research_plan.md", "21_research_questions.md", "22_environment_scan.md",
                "23_secondary_summary.md", "24_competitor_list.csv", "24_competitor_canvases.md",
                "25_customer_segments.md", "26_interview_guide.md", "27_screener.md",
                "28_interviews_log.csv", "29_empathy_maps.md", "30_jobs_to_be_done.md",
                "31_insights.md", "32_assumption_backlog.csv", "33_concept_cards.md",
                "34_test_cards.json", "35_failure_analysis.md", "36_expert_panel_summary.md",
                "37_bias_check.md", "38_progress_demo.md"
            ],
            "30_design": [
                "30_design_brief.md", "31_ideation.md", "33_feedback_log.csv",
                "34_selection_criteria.md", "35_selection_scorecard.csv",
                "36_financial_projections.md", "37_implementation_roadmap.md",
                "38_risk_mitigation.md", "39_test_cards.json", "40_integration_decision.md",
                "41_final_recommendation.md", "financials_cashflow.csv"
            ]
        }
        
        # Required prototype files in 32_prototypes/
        self.prototype_requirements = [
            "prototype_A_canvas.md",
            "prototype_B_canvas.md", 
            "prototype_C_canvas.md"
        ]
        
        # Business-level requirements
        self.business_requirements = [
            "evidence_ledger.csv",
            "manifest.json"
        ]

    # ------------------------------
    # Helpers
    # ------------------------------
    def _read_text(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except Exception:
            return ""

    def validate_phase(self, phase: str) -> Tuple[List[str], List[str], List[str]]:
        """Validate deliverables for a specific phase"""
        phase_path = self.business_path / phase
        required_files = self.phase_requirements.get(phase, [])
        
        missing_files = []
        present_files = []
        extra_files = []
        
        if not phase_path.exists():
            return required_files, [], []
            
        actual_files = {f.name for f in phase_path.iterdir() if f.is_file()}
        required_set = set(required_files)
        
        # Check for missing files
        missing_files = list(required_set - actual_files)
        
        # Check for present files
        present_files = list(required_set & actual_files)
        
        # Check for extra files (excluding prototypes directory)
        extra_files = list(actual_files - required_set - {"32_prototypes"})
        
        return missing_files, present_files, extra_files

    def validate_prototypes(self) -> Tuple[List[str], List[str]]:
        """Validate prototype deliverables"""
        prototype_path = self.business_path / "30_design" / "32_prototypes"
        
        if not prototype_path.exists():
            return self.prototype_requirements, []
            
        actual_files = {f.name for f in prototype_path.iterdir() if f.is_file()}
        required_set = set(self.prototype_requirements)
        
        missing_files = list(required_set - actual_files)
        present_files = list(required_set & actual_files)
        
        return missing_files, present_files

    def validate_business_level(self) -> Tuple[List[str], List[str]]:
        """Validate business-level deliverables"""
        actual_files = {f.name for f in self.business_path.iterdir() if f.is_file()}
        required_set = set(self.business_requirements)
        
        missing_files = list(required_set - actual_files)
        present_files = list(required_set & actual_files)
        
        return missing_files, present_files

    def generate_compliance_report(self) -> Dict:
        """Generate comprehensive compliance report"""
        report = {
            "business": self.business_name,
            "timestamp": "2025-09-10T14:26:42-03:00",
            "phases": {},
            "prototypes": {},
            "business_level": {},
            "methodology": {},
            "overall_compliance": 0
        }
        
        total_required = 0
        total_present = 0
        
        # Validate each phase
        for phase in self.phase_requirements.keys():
            missing, present, extra = self.validate_phase(phase)
            report["phases"][phase] = {
                "missing": missing,
                "present": present,
                "extra": extra,
                "compliance_pct": len(present) / len(self.phase_requirements[phase]) * 100 if self.phase_requirements[phase] else 100
            }
            total_required += len(self.phase_requirements[phase])
            total_present += len(present)
        
        # Validate prototypes
        missing_proto, present_proto = self.validate_prototypes()
        report["prototypes"] = {
            "missing": missing_proto,
            "present": present_proto,
            "compliance_pct": len(present_proto) / len(self.prototype_requirements) * 100
        }
        total_required += len(self.prototype_requirements)
        total_present += len(present_proto)
        
        # Validate business level
        missing_biz, present_biz = self.validate_business_level()
        report["business_level"] = {
            "missing": missing_biz,
            "present": present_biz,
            "compliance_pct": len(present_biz) / len(self.business_requirements) * 100
        }
        total_required += len(self.business_requirements)
        total_present += len(present_biz)
        
        # Calculate overall compliance
        report["overall_compliance"] = (total_present / total_required * 100) if total_required > 0 else 0

        # Methodology adherence checks (lightweight heuristics)
        report["methodology"] = {
            "vpd": self._check_vpd(),
            "bmg": self._check_bmg(),
            "tbi": self._check_tbi(),
        }

        return report

    # ------------------------------
    # Methodology checks (heuristics)
    # ------------------------------
    def _check_vpd(self) -> Dict:
        base = self.business_path
        missing: List[str] = []
        messages: List[str] = []
        status = "ok"

        vpc = base / "10_mobilize" / "value_proposition_canvas.md"
        jobs = base / "10_mobilize" / "customer_jobs_analysis.md"
        pain_gain = base / "20_understand" / "pain_gain_mapping.md"

        for p in [vpc, jobs, pain_gain]:
            if not p.exists():
                missing.append(str(p.relative_to(base)))

        if missing:
            status = "warn"
            messages.append(f"Missing VPD artifacts: {', '.join(missing)}")

        # Content heuristics
        jobs_text = self._read_text(jobs)
        if jobs_text:
            for bucket in ["Functional", "Emotional", "Social"]:
                if bucket.lower() not in jobs_text.lower():
                    status = "warn"
                    messages.append(f"Customer jobs missing category: {bucket}")

        pain_gain_text = self._read_text(pain_gain)
        if pain_gain_text and ("severity" not in pain_gain_text.lower() or "importance" not in pain_gain_text.lower()):
            status = "warn"
            messages.append("Pain/Gain mapping should include severity and importance classification")

        vpc_text = self._read_text(vpc)
        if vpc_text and ("Pain Relievers" not in vpc_text and "Gain Creators" not in vpc_text):
            status = "warn"
            messages.append("VPC value map sections (Pain Relievers, Gain Creators) not clearly present")

        return {"status": status, "messages": messages}

    def _check_bmg(self) -> Dict:
        base = self.business_path
        proto_dir = base / "30_design" / "32_prototypes"
        messages: List[str] = []
        status = "ok"

        canvases = list(proto_dir.glob("prototype_*_canvas.md")) if proto_dir.exists() else []
        if not canvases:
            status = "warn"
            messages.append("No prototype canvases found under 30_design/32_prototypes/")
            return {"status": status, "messages": messages}

        required_blocks = [
            "Customer Segments", "Value Propositions", "Channels", "Customer Relationships",
            "Revenue Streams", "Key Resources", "Key Activities", "Key Partnerships", "Cost Structure",
        ]
        for cv in canvases:
            text = self._read_text(cv)
            for block in required_blocks:
                if block.lower() not in text.lower():
                    status = "warn"
                    messages.append(f"{cv.name}: Missing BMG block: {block}")

        fin = base / "30_design" / "36_financial_projections.md"
        if not fin.exists():
            status = "warn"
            messages.append("Missing 30_design/36_financial_projections.md for viability alignment")

        return {"status": status, "messages": messages}

    def _check_tbi(self) -> Dict:
        base = self.business_path
        files = [
            base / "20_understand" / "34_test_cards.json",
            base / "30_design" / "39_test_cards.json",
        ]
        messages: List[str] = []
        status = "ok"

        for f in files:
            if not f.exists():
                status = "warn"
                messages.append(f"Missing test cards file: {f.relative_to(base)}")
                continue
            # Light JSON validation
            try:
                data = json.loads(self._read_text(f) or "{}")
            except json.JSONDecodeError:
                status = "warn"
                messages.append(f"Invalid JSON in {f.relative_to(base)}")
                continue
            tests = data.get("tests")
            if not isinstance(tests, list) or not tests:
                status = "warn"
                messages.append(f"{f.name}: 'tests' array missing or empty")
                continue
            for idx, t in enumerate(tests):
                for key in ("assumption", "test", "metric", "stop_condition"):
                    if key not in t or not str(t[key]).strip():
                        status = "warn"
                        messages.append(f"{f.name}[{idx}]: missing field '{key}'")

        return {"status": status, "messages": messages}

    def validate_file_naming(self) -> List[str]:
        """Check for file naming violations"""
        violations = []
        
        for phase in self.phase_requirements.keys():
            phase_path = self.business_path / phase
            if not phase_path.exists():
                continue
                
            for file_path in phase_path.iterdir():
                if file_path.is_file():
                    filename = file_path.name
                    # Check if filename matches expected pattern
                    if filename not in self.phase_requirements[phase]:
                        # Check if it's a similar but incorrectly named file
                        if any(req in filename for req in self.phase_requirements[phase]):
                            violations.append(f"{phase}/{filename} - Similar to required file but incorrect naming")
        
        return violations

def main():
    parser = argparse.ArgumentParser(description="Validate BMDP workflow compliance")
    parser.add_argument("--business", required=True, help="Business name (grower, processor, distributor, marketplace)")
    parser.add_argument("--format", choices=["json", "summary"], default="summary", help="Output format")
    parser.add_argument("--fix", action="store_true", help="Generate fix commands for missing files")
    
    args = parser.parse_args()
    
    business_path = f"businesses/{args.business}"
    
    if not os.path.exists(business_path):
        print(f"ERROR: Business path {business_path} does not exist")
        return 1
    
    validator = WorkflowValidator(business_path)
    report = validator.generate_compliance_report()
    naming_violations = validator.validate_file_naming()
    
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        # Summary format
        print(f"\n=== COMPLIANCE REPORT: {args.business.upper()} ===")
        print(f"Overall Compliance: {report['overall_compliance']:.1f}%")
        
        for phase, data in report["phases"].items():
            print(f"\n{phase}: {data['compliance_pct']:.1f}%")
            if data["missing"]:
                print(f"  Missing: {', '.join(data['missing'])}")
            if data["extra"]:
                print(f"  Extra: {', '.join(data['extra'])}")
        
        if report["prototypes"]["missing"]:
            print(f"\nPrototypes Missing: {', '.join(report['prototypes']['missing'])}")
            
        if report["business_level"]["missing"]:
            print(f"\nBusiness Level Missing: {', '.join(report['business_level']['missing'])}")
        
        if naming_violations:
            print(f"\nNaming Violations:")
            for violation in naming_violations:
                print(f"  - {violation}")

        # Methodology summary
        print("\nMethodology Checks:")
        for domain in ("vpd", "bmg", "tbi"):
            dom = report["methodology"].get(domain, {})
            print(f"  {domain.upper()}: status={dom.get('status', 'unknown')}")
            for msg in dom.get("messages", [])[:5]:  # limit output
                print(f"    - {msg}")
    
    # Return non-zero exit code if compliance < 100%
    return 0 if report["overall_compliance"] == 100 else 1

if __name__ == "__main__":
    exit(main())
