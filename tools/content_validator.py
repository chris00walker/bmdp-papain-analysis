#!/usr/bin/env python3
"""
Advanced Content Validator - Semantic analysis and quality validation for BMDP deliverables
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
import argparse
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    BASIC = "basic"
    SEMANTIC = "semantic" 
    COMPREHENSIVE = "comprehensive"

class ContentQuality(Enum):
    EXCELLENT = "A"
    GOOD = "B"
    SATISFACTORY = "C"
    NEEDS_IMPROVEMENT = "D"
    POOR = "F"

@dataclass
class ValidationResult:
    deliverable: str
    score: float
    quality_grade: ContentQuality
    issues: List[str]
    recommendations: List[str]
    metrics: Dict[str, Any]

class ContentValidator:
    """Advanced content validation with business rule checking"""
    
    def __init__(self, business_path: str):
        self.business_path = Path(business_path)
        self.business_slug = self.business_path.name
        
        # Content quality thresholds
        self.thresholds = {
            "min_word_count": {
                "brief": 200, "charter": 300, "plan": 250, "canvas": 400,
                "analysis": 500, "insights": 600, "recommendation": 800
            },
            "min_sections": {
                "brief": 3, "charter": 5, "plan": 4, "canvas": 9,
                "analysis": 4, "insights": 5, "recommendation": 8
            },
            "placeholder_threshold": 0.1  # Max 10% placeholder content
        }
        
        # Business logic rules
        self.business_rules = self._load_business_rules()
        
    def _load_business_rules(self) -> Dict:
        """Load business validation rules"""
        return {
            "financial_rules": {
                "revenue_growth_max": 300,  # Max 300% YoY growth
                "margin_ranges": {"gross": (0.2, 0.9), "net": (0.05, 0.4)},
                "roi_minimum": 0.15,  # Minimum 15% ROI
                "payback_maximum": 60  # Max 60 months payback
            },
            "market_rules": {
                "market_share_realistic": 0.05,  # Max 5% market share claim
                "cac_ltv_ratio_min": 3.0,  # LTV:CAC ratio minimum 3:1
                "churn_rate_max": 0.15  # Max 15% monthly churn
            },
            "content_rules": {
                "required_keywords": {
                    "value_proposition": ["customer", "problem", "solution", "benefit"],
                    "market_analysis": ["size", "growth", "competition", "opportunity"],
                    "financial_projection": ["revenue", "cost", "profit", "cash flow"]
                }
            }
        }
    
    def validate_deliverable(self, deliverable_path: Path, validation_level: ValidationLevel) -> ValidationResult:
        """Validate individual deliverable content quality"""
        
        if not deliverable_path.exists():
            return ValidationResult(
                deliverable=deliverable_path.name,
                score=0.0,
                quality_grade=ContentQuality.POOR,
                issues=[f"File does not exist: {deliverable_path}"],
                recommendations=["Create the required deliverable"],
                metrics={}
            )
        
        content = self._read_file_content(deliverable_path)
        deliverable_type = self._classify_deliverable(deliverable_path.name)
        
        # Run validation checks based on level
        issues = []
        recommendations = []
        metrics = {}
        
        # Basic validation
        basic_score, basic_issues, basic_metrics = self._validate_basic_content(content, deliverable_type)
        issues.extend(basic_issues)
        metrics.update(basic_metrics)
        
        if validation_level in [ValidationLevel.SEMANTIC, ValidationLevel.COMPREHENSIVE]:
            # Semantic validation
            semantic_score, semantic_issues = self._validate_semantic_content(content, deliverable_type)
            issues.extend(semantic_issues)
            basic_score = (basic_score + semantic_score) / 2
        
        if validation_level == ValidationLevel.COMPREHENSIVE:
            # Business rule validation
            business_score, business_issues = self._validate_business_rules(content, deliverable_type)
            issues.extend(business_issues)
            basic_score = (basic_score + business_score) / 2
        
        # Generate recommendations
        recommendations = self._generate_recommendations(issues, deliverable_type)
        
        # Calculate final score and grade
        final_score = max(0, min(100, basic_score))
        quality_grade = self._calculate_quality_grade(final_score)
        
        return ValidationResult(
            deliverable=deliverable_path.name,
            score=final_score,
            quality_grade=quality_grade,
            issues=issues,
            recommendations=recommendations,
            metrics=metrics
        )
    
    def _read_file_content(self, file_path: Path) -> str:
        """Read file content with encoding handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def _classify_deliverable(self, filename: str) -> str:
        """Classify deliverable type for targeted validation"""
        if "brief" in filename:
            return "brief"
        elif "charter" in filename:
            return "charter"
        elif "plan" in filename or "roadmap" in filename:
            return "plan"
        elif "canvas" in filename:
            return "canvas"
        elif "analysis" in filename or "scan" in filename:
            return "analysis"
        elif "insights" in filename or "summary" in filename:
            return "insights"
        elif "recommendation" in filename:
            return "recommendation"
        else:
            return "general"
    
    def _validate_basic_content(self, content: str, deliverable_type: str) -> Tuple[float, List[str], Dict]:
        """Basic content validation - structure and completeness"""
        issues = []
        metrics = {}
        score = 100.0
        
        # Word count validation
        word_count = len(content.split())
        min_words = self.thresholds["min_word_count"].get(deliverable_type, 150)
        metrics["word_count"] = word_count
        
        if word_count < min_words:
            issues.append(f"Content too short: {word_count} words (minimum: {min_words})")
            score -= 20
        
        # Section count validation (for markdown files)
        if content.startswith('#'):
            section_count = len(re.findall(r'^#+\s', content, re.MULTILINE))
            min_sections = self.thresholds["min_sections"].get(deliverable_type, 2)
            metrics["section_count"] = section_count
            
            if section_count < min_sections:
                issues.append(f"Insufficient sections: {section_count} (minimum: {min_sections})")
                score -= 15
        
        # Placeholder content detection
        placeholder_patterns = [
            r'\[.*?\]', r'TBD', r'TODO', r'PLACEHOLDER', r'XXX', r'FIXME',
            r'Lorem ipsum', r'Sample text', r'Example content'
        ]
        
        placeholder_count = 0
        for pattern in placeholder_patterns:
            placeholder_count += len(re.findall(pattern, content, re.IGNORECASE))
        
        placeholder_ratio = placeholder_count / max(1, word_count)
        metrics["placeholder_ratio"] = placeholder_ratio
        
        if placeholder_ratio > self.thresholds["placeholder_threshold"]:
            issues.append(f"Too much placeholder content: {placeholder_ratio:.1%}")
            score -= 25
        
        # Empty or minimal sections
        if deliverable_type in ["canvas", "analysis", "recommendation"]:
            empty_sections = len(re.findall(r'#+\s+[^\n]*\n\s*\n', content))
            if empty_sections > 2:
                issues.append(f"Multiple empty sections detected: {empty_sections}")
                score -= 10
        
        return score, issues, metrics
    
    def _validate_semantic_content(self, content: str, deliverable_type: str) -> Tuple[float, List[str]]:
        """Semantic content validation - meaning and context"""
        issues = []
        score = 100.0
        
        # Required keywords validation
        required_keywords = self.business_rules["content_rules"]["required_keywords"]
        
        if deliverable_type in required_keywords:
            keywords = required_keywords[deliverable_type]
            missing_keywords = []
            
            for keyword in keywords:
                if keyword.lower() not in content.lower():
                    missing_keywords.append(keyword)
            
            if missing_keywords:
                issues.append(f"Missing key concepts: {', '.join(missing_keywords)}")
                score -= len(missing_keywords) * 5
        
        # Business context validation
        business_terms = ["customer", "market", "revenue", "value", "competitive"]
        found_terms = sum(1 for term in business_terms if term.lower() in content.lower())
        
        if found_terms < 3:
            issues.append("Insufficient business context and terminology")
            score -= 15
        
        # Quantitative data validation
        numbers = re.findall(r'\$[\d,]+|\d+%|\d+\.\d+%|\d+[KMB]', content)
        if deliverable_type in ["analysis", "recommendation", "plan"] and len(numbers) < 3:
            issues.append("Lacks quantitative data and metrics")
            score -= 10
        
        return score, issues
    
    def _validate_business_rules(self, content: str, deliverable_type: str) -> Tuple[float, List[str]]:
        """Business rule validation - logic and feasibility"""
        issues = []
        score = 100.0
        
        # Financial validation
        if "financial" in deliverable_type or "recommendation" in deliverable_type:
            # Extract financial numbers
            revenue_matches = re.findall(r'revenue.*?\$?([\d,]+)', content, re.IGNORECASE)
            roi_matches = re.findall(r'roi.*?(\d+)%', content, re.IGNORECASE)
            
            # Validate ROI claims
            for roi_str in roi_matches:
                roi = float(roi_str) / 100
                if roi > 1.0:  # >100% ROI
                    issues.append(f"Unrealistic ROI claim: {roi_str}%")
                    score -= 10
                elif roi < self.business_rules["financial_rules"]["roi_minimum"]:
                    issues.append(f"ROI below minimum threshold: {roi_str}%")
                    score -= 5
        
        # Market validation
        if "market" in content.lower() or deliverable_type == "analysis":
            market_share_matches = re.findall(r'market share.*?(\d+)%', content, re.IGNORECASE)
            for share_str in market_share_matches:
                share = float(share_str) / 100
                max_realistic = self.business_rules["market_rules"]["market_share_realistic"]
                if share > max_realistic:
                    issues.append(f"Unrealistic market share claim: {share_str}%")
                    score -= 15
        
        return score, issues
    
    def _generate_recommendations(self, issues: List[str], deliverable_type: str) -> List[str]:
        """Generate specific improvement recommendations"""
        recommendations = []
        
        for issue in issues:
            if "too short" in issue.lower():
                recommendations.append("Expand content with more detailed analysis and examples")
            elif "placeholder" in issue.lower():
                recommendations.append("Replace placeholder content with actual business-specific data")
            elif "empty sections" in issue.lower():
                recommendations.append("Complete all sections with substantive content")
            elif "missing key concepts" in issue.lower():
                recommendations.append("Include essential business concepts and terminology")
            elif "unrealistic" in issue.lower():
                recommendations.append("Review and adjust financial/market projections for realism")
            elif "insufficient" in issue.lower():
                recommendations.append("Add more business context and supporting data")
        
        # General recommendations by deliverable type
        if deliverable_type == "recommendation":
            recommendations.append("Ensure recommendations are actionable and well-justified")
        elif deliverable_type == "analysis":
            recommendations.append("Include data sources and analytical methodology")
        elif deliverable_type == "canvas":
            recommendations.append("Validate business model component alignment")
        
        return recommendations
    
    def _calculate_quality_grade(self, score: float) -> ContentQuality:
        """Calculate quality grade from score"""
        if score >= 95:
            return ContentQuality.EXCELLENT
        elif score >= 85:
            return ContentQuality.GOOD
        elif score >= 75:
            return ContentQuality.SATISFACTORY
        elif score >= 65:
            return ContentQuality.NEEDS_IMPROVEMENT
        else:
            return ContentQuality.POOR
    
    def validate_phase(self, phase: str, validation_level: ValidationLevel) -> Dict[str, ValidationResult]:
        """Validate all deliverables in a phase"""
        phase_path = self.business_path / phase
        results = {}
        
        if not phase_path.exists():
            return results
        
        for file_path in phase_path.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                result = self.validate_deliverable(file_path, validation_level)
                results[file_path.name] = result
        
        return results
    
    def generate_quality_report(self, validation_level: ValidationLevel) -> Dict:
        """Generate comprehensive quality report for business"""
        
        phases = ["00_initiation", "10_mobilize", "20_understand", "30_design"]
        all_results = {}
        
        for phase in phases:
            phase_results = self.validate_phase(phase, validation_level)
            if phase_results:
                all_results[phase] = phase_results
        
        # Calculate overall metrics
        all_scores = []
        all_issues = []
        grade_counts = {grade: 0 for grade in ContentQuality}
        
        for phase_results in all_results.values():
            for result in phase_results.values():
                all_scores.append(result.score)
                all_issues.extend(result.issues)
                grade_counts[result.quality_grade] += 1
        
        overall_score = sum(all_scores) / len(all_scores) if all_scores else 0
        overall_grade = self._calculate_quality_grade(overall_score)
        
        return {
            "business": self.business_slug,
            "validation_level": validation_level.value,
            "overall_score": round(overall_score, 1),
            "overall_grade": overall_grade.value,
            "total_deliverables": len(all_scores),
            "grade_distribution": {grade.value: count for grade, count in grade_counts.items()},
            "total_issues": len(all_issues),
            "phase_results": all_results,
            "summary": {
                "excellent": grade_counts[ContentQuality.EXCELLENT],
                "good": grade_counts[ContentQuality.GOOD], 
                "needs_work": grade_counts[ContentQuality.NEEDS_IMPROVEMENT] + grade_counts[ContentQuality.POOR]
            }
        }

def main():
    parser = argparse.ArgumentParser(description="Advanced content validation for BMDP deliverables")
    parser.add_argument("--business", required=True, help="Business slug (grower, processor, etc.)")
    parser.add_argument("--phase", help="Specific phase to validate")
    parser.add_argument("--analysis", choices=["basic", "semantic", "comprehensive"],
                        default="semantic", help="Validation depth")
    parser.add_argument("--deliverable", help="Specific deliverable to validate")
    parser.add_argument("--mode", choices=["all", "vpd", "bmg", "tbi"], default="all",
                        help="Run methodology checks for VPD/BMG/TBI in addition to content checks")
    parser.add_argument("--format", choices=["json", "summary"], default="summary")
    
    args = parser.parse_args()
    
    business_path = Path(f"businesses/{args.business}")
    if not business_path.exists():
        print(f"ERROR: Business path not found: {business_path}")
        return 1

    validator = ContentValidator(str(business_path))
    validation_level = ValidationLevel(args.analysis)

    # Container to aggregate optional methodology checks
    methodology_checks = {}

    if args.deliverable:
        # Validate specific deliverable
        deliverable_path = business_path / args.phase / args.deliverable if args.phase else business_path / args.deliverable
        result = validator.validate_deliverable(deliverable_path, validation_level)

        # Optional domain checks
        methodology_checks = _run_methodology_checks(validator, args.mode)

        if args.format == "json":
            out = {"deliverable": result.__dict__, "methodology_checks": methodology_checks}
            print(json.dumps(out, indent=2, default=str))
        else:
            print(f"\n=== CONTENT VALIDATION: {args.deliverable} ===")
            print(f"Score: {result.score:.1f} (Grade: {result.quality_grade.value})")
            if result.issues:
                print(f"Issues ({len(result.issues)}):")
                for issue in result.issues:
                    print(f"  - {issue}")
            if result.recommendations:
                print(f"Recommendations:")
                for rec in result.recommendations:
                    print(f"  + {rec}")
            _print_methodology_checks(methodology_checks)

    elif args.phase:
        # Validate specific phase
        results = validator.validate_phase(args.phase, validation_level)

        # Optional domain checks
        methodology_checks = _run_methodology_checks(validator, args.mode)

        if args.format == "json":
            out = {
                "phase": args.phase,
                "results": {k: v.__dict__ for k, v in results.items()},
                "methodology_checks": methodology_checks,
            }
            print(json.dumps(out, indent=2, default=str))
        else:
            print(f"\n=== PHASE VALIDATION: {args.phase} ===")
            for deliverable, result in results.items():
                print(f"{deliverable}: {result.score:.1f} ({result.quality_grade.value}) - {len(result.issues)} issues")
            _print_methodology_checks(methodology_checks)

    else:
        # Full business validation
        report = validator.generate_quality_report(validation_level)

        # Optional domain checks
        methodology_checks = _run_methodology_checks(validator, args.mode)

        if args.format == "json":
            out = {"report": report, "methodology_checks": methodology_checks}
            print(json.dumps(out, indent=2, default=str))
        else:
            print(f"\n=== QUALITY REPORT: {args.business.upper()} ===")
            print(f"Overall Score: {report['overall_score']} (Grade: {report['overall_grade']})")
            print(f"Total Deliverables: {report['total_deliverables']}")
            print(f"Total Issues: {report['total_issues']}")
            print(f"\nGrade Distribution:")
            for grade, count in report['grade_distribution'].items():
                if count > 0:
                    print(f"  {grade}: {count}")

            print(f"\nSummary:")
            print(f"  Excellent (A): {report['summary']['excellent']}")
            print(f"  Good (B): {report['summary']['good']}")
            print(f"  Needs Work (C-F): {report['summary']['needs_work']}")
            _print_methodology_checks(methodology_checks)

    return 0

# Methodology Check Helpers #
#############################

def _run_methodology_checks(validator: ContentValidator, mode: str) -> dict:
    """Run VPD/BMG/TBI methodology checks based on selected mode."""
    results: dict = {}
    modes = [mode] if mode != "all" else ["vpd", "bmg", "tbi"]

    if "vpd" in modes:
        results["vpd"] = _check_vpd(validator)
    if "bmg" in modes:
        results["bmg"] = _check_bmg(validator)
    if "tbi" in modes:
        results["tbi"] = _check_tbi(validator)

    return results


def _print_methodology_checks(methodology_checks: dict) -> None:
    if not methodology_checks:
        return
    print("\n--- Methodology Checks ---")
    for domain, res in methodology_checks.items():
        status = res.get("status", "unknown")
        print(f"[{domain.upper()}] status={status}")
        for msg in res.get("messages", []):
            print(f" - {msg}")


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _check_vpd(validator: ContentValidator) -> dict:
    base = validator.business_path
    required = [
        base / "10_mobilize" / "value_proposition_canvas.md",
        base / "10_mobilize" / "customer_jobs_analysis.md",
        base / "20_understand" / "pain_gain_mapping.md",
    ]
    messages = []
    status = "ok"

    # Existence
    missing = [str(p.relative_to(base)) for p in required if not p.exists()]
    if missing:
        status = "warn"
        messages.append(f"Missing VPD artifacts: {', '.join(missing)}")

    # Simple content heuristics
    jobs = _read_text(base / "10_mobilize" / "customer_jobs_analysis.md")
    if jobs:
        for bucket in ["Functional", "Emotional", "Social"]:
            if bucket.lower() not in jobs.lower():
                status = "warn"
                messages.append(f"Customer jobs missing category: {bucket}")

    pain_gain = _read_text(base / "20_understand" / "pain_gain_mapping.md")
    if pain_gain and ("severity" not in pain_gain.lower() or "importance" not in pain_gain.lower()):
        status = "warn"
        messages.append("Pain/Gain mapping should include severity and importance classification")

    vpc = _read_text(base / "10_mobilize" / "value_proposition_canvas.md")
    if vpc and ("Pain Relievers" not in vpc and "Gain Creators" not in vpc):
        status = "warn"
        messages.append("VPC value map sections (Pain Relievers, Gain Creators) not clearly present")

    return {"status": status, "messages": messages}

def _check_bmg(validator: ContentValidator) -> dict:
    base = validator.business_path
    proto_dir = base / "30_design" / "32_prototypes"
    messages = []
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
        text = _read_text(cv)
        for block in required_blocks:
            if block.lower() not in text.lower():
                status = "warn"
                messages.append(f"{cv.name}: Missing BMG block: {block}")

    # Financial alignment presence check
    fin = base / "30_design" / "36_financial_projections.md"
    if not fin.exists():
        status = "warn"
        messages.append("Missing 30_design/36_financial_projections.md for viability alignment")

    return {"status": status, "messages": messages}


def _check_tbi(validator: ContentValidator) -> dict:
    base = validator.business_path
    files = [
        base / "20_understand" / "34_test_cards.json",
        base / "30_design" / "39_test_cards.json",
    ]
    messages = []
    status = "ok"

    for f in files:
        if not f.exists():
            status = "warn"
            messages.append(f"Missing test cards file: {f.relative_to(base)}")
            continue
        try:
            data = json.loads(_read_text(f) or "{}")
        except json.JSONDecodeError:
            status = "warn"
            messages.append(f"Invalid JSON in {f.relative_to(base)}")
            continue
        tests = data.get("tests")
        if not isinstance(tests, list) or not tests:
            status = "warn"
            messages.append(f"{f.name}: 'tests' array missing or empty")
            continue
        # Basic schema checks for each test
        for idx, t in enumerate(tests):
            for key in ("assumption", "test", "metric", "stop_condition"):
                if key not in t or not str(t[key]).strip():
                    status = "warn"
                    messages.append(f"{f.name}[{idx}]: missing field '{key}'")

    return {"status": status, "messages": messages}
