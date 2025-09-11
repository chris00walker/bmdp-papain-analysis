#!/usr/bin/env python3
"""
Quality Scorer - Comprehensive quality assessment and reporting for BMDP deliverables
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
import argparse
from dataclasses import dataclass
from datetime import datetime

# Import our validation modules
try:
    from content_validator import ContentValidator, ValidationLevel
    from business_rule_engine import BusinessRuleEngine
except ImportError:
    print("Warning: Could not import validation modules. Ensure content_validator.py and business_rule_engine.py are available.")

@dataclass
class QualityMetrics:
    content_score: float
    business_rules_score: float
    consistency_score: float
    overall_score: float
    grade: str
    total_issues: int
    critical_issues: int

class QualityScorer:
    """Comprehensive quality scoring system for BMDP deliverables"""
    
    def __init__(self, business_path: str):
        self.business_path = Path(business_path)
        self.business_slug = self.business_path.name
        
        # Initialize validators
        try:
            self.content_validator = ContentValidator(str(self.business_path))
            self.rule_engine = BusinessRuleEngine(str(self.business_path))
        except:
            self.content_validator = None
            self.rule_engine = None
            print("Warning: Could not initialize validators")
        
        # Quality weights
        self.weights = {
            "content_quality": 0.4,
            "business_rules": 0.35,
            "consistency": 0.25
        }
    
    def calculate_comprehensive_score(self) -> QualityMetrics:
        """Calculate comprehensive quality score across all dimensions"""
        
        # Content quality assessment
        content_score = 0.0
        if self.content_validator:
            try:
                content_report = self.content_validator.generate_quality_report(ValidationLevel.COMPREHENSIVE)
                content_score = content_report.get('overall_score', 0)
            except Exception as e:
                print(f"Content validation error: {e}")
        
        # Business rules assessment
        business_rules_score = 0.0
        critical_issues = 0
        if self.rule_engine:
            try:
                rules_report = self.rule_engine.generate_rule_report()
                business_rules_score = rules_report.get('compliance_score', 0)
                critical_issues = rules_report.get('severity_breakdown', {}).get('critical', 0)
            except Exception as e:
                print(f"Business rules validation error: {e}")
        
        # Consistency assessment (simplified for now)
        consistency_score = self._assess_consistency()
        
        # Calculate weighted overall score
        overall_score = (
            content_score * self.weights["content_quality"] +
            business_rules_score * self.weights["business_rules"] +
            consistency_score * self.weights["consistency"]
        )
        
        # Calculate grade
        grade = self._calculate_grade(overall_score)
        
        # Count total issues
        total_issues = self._count_total_issues()
        
        return QualityMetrics(
            content_score=round(content_score, 1),
            business_rules_score=round(business_rules_score, 1),
            consistency_score=round(consistency_score, 1),
            overall_score=round(overall_score, 1),
            grade=grade,
            total_issues=total_issues,
            critical_issues=critical_issues
        )
    
    def _assess_consistency(self) -> float:
        """Assess consistency across deliverables (simplified implementation)"""
        try:
            # Check for key files existence
            key_files = [
                "00_initiation/00_sponsor_brief.md",
                "00_initiation/01_project_charter.md",
                "20_understand/31_insights.md",
                "30_design/41_final_recommendation.md"
            ]
            
            existing_files = 0
            for file_path in key_files:
                if (self.business_path / file_path).exists():
                    existing_files += 1
            
            # Basic consistency score based on file completeness
            base_score = (existing_files / len(key_files)) * 100
            
            # Check for manifest.json consistency
            manifest_path = self.business_path / "manifest.json"
            if manifest_path.exists():
                base_score = min(100, base_score + 10)
            
            return base_score
            
        except Exception:
            return 50.0  # Default moderate score if assessment fails
    
    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from numeric score"""
        if score >= 95:
            return "A+"
        elif score >= 90:
            return "A"
        elif score >= 85:
            return "B+"
        elif score >= 80:
            return "B"
        elif score >= 75:
            return "C+"
        elif score >= 70:
            return "C"
        elif score >= 65:
            return "D+"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _count_total_issues(self) -> int:
        """Count total issues across all validation dimensions"""
        total_issues = 0
        
        try:
            if self.content_validator:
                content_report = self.content_validator.generate_quality_report(ValidationLevel.SEMANTIC)
                total_issues += content_report.get('total_issues', 0)
            
            if self.rule_engine:
                rules_report = self.rule_engine.generate_rule_report()
                total_issues += rules_report.get('total_violations', 0)
        except Exception:
            pass
        
        return total_issues
    
    def generate_quality_dashboard(self) -> Dict:
        """Generate comprehensive quality dashboard"""
        metrics = self.calculate_comprehensive_score()
        
        # Get detailed breakdowns
        content_breakdown = {}
        rules_breakdown = {}
        
        try:
            if self.content_validator:
                content_report = self.content_validator.generate_quality_report(ValidationLevel.SEMANTIC)
                content_breakdown = {
                    "grade_distribution": content_report.get('grade_distribution', {}),
                    "total_deliverables": content_report.get('total_deliverables', 0),
                    "summary": content_report.get('summary', {})
                }
        except Exception:
            pass
        
        try:
            if self.rule_engine:
                rules_report = self.rule_engine.generate_rule_report()
                rules_breakdown = {
                    "severity_breakdown": rules_report.get('severity_breakdown', {}),
                    "recommendations": rules_report.get('recommendations', [])
                }
        except Exception:
            pass
        
        # Generate improvement priorities
        priorities = self._generate_improvement_priorities(metrics)
        
        return {
            "business": self.business_slug,
            "timestamp": datetime.now().isoformat(),
            "overall_metrics": {
                "score": metrics.overall_score,
                "grade": metrics.grade,
                "total_issues": metrics.total_issues,
                "critical_issues": metrics.critical_issues
            },
            "dimension_scores": {
                "content_quality": metrics.content_score,
                "business_rules": metrics.business_rules_score,
                "consistency": metrics.consistency_score
            },
            "detailed_breakdowns": {
                "content": content_breakdown,
                "business_rules": rules_breakdown
            },
            "improvement_priorities": priorities,
            "quality_status": self._determine_quality_status(metrics),
            "recommendations": self._generate_quality_recommendations(metrics)
        }
    
    def _generate_improvement_priorities(self, metrics: QualityMetrics) -> List[Dict]:
        """Generate prioritized improvement recommendations"""
        priorities = []
        
        # Critical issues first
        if metrics.critical_issues > 0:
            priorities.append({
                "priority": "CRITICAL",
                "area": "Business Rules",
                "description": f"{metrics.critical_issues} critical business rule violations",
                "impact": "Blocks business viability",
                "action": "Address fundamental business model issues immediately"
            })
        
        # Low scores by dimension
        if metrics.content_score < 70:
            priorities.append({
                "priority": "HIGH",
                "area": "Content Quality",
                "description": f"Content quality score: {metrics.content_score}",
                "impact": "Poor deliverable quality",
                "action": "Improve content depth and completeness"
            })
        
        if metrics.business_rules_score < 70:
            priorities.append({
                "priority": "HIGH", 
                "area": "Business Logic",
                "description": f"Business rules score: {metrics.business_rules_score}",
                "impact": "Unrealistic business assumptions",
                "action": "Validate financial projections and market assumptions"
            })
        
        if metrics.consistency_score < 70:
            priorities.append({
                "priority": "MEDIUM",
                "area": "Consistency",
                "description": f"Consistency score: {metrics.consistency_score}",
                "impact": "Conflicting information across deliverables",
                "action": "Align business model components and assumptions"
            })
        
        return priorities
    
    def _determine_quality_status(self, metrics: QualityMetrics) -> str:
        """Determine overall quality status"""
        if metrics.critical_issues > 0:
            return "CRITICAL_ISSUES"
        elif metrics.overall_score >= 90:
            return "EXCELLENT"
        elif metrics.overall_score >= 80:
            return "GOOD"
        elif metrics.overall_score >= 70:
            return "ACCEPTABLE"
        elif metrics.overall_score >= 60:
            return "NEEDS_IMPROVEMENT"
        else:
            return "POOR"
    
    def _generate_quality_recommendations(self, metrics: QualityMetrics) -> List[str]:
        """Generate specific quality improvement recommendations"""
        recommendations = []
        
        if metrics.overall_score < 80:
            recommendations.append("Overall quality below target - comprehensive review needed")
        
        if metrics.content_score < 75:
            recommendations.append("Enhance content depth with more detailed analysis and examples")
        
        if metrics.business_rules_score < 80:
            recommendations.append("Validate all financial calculations and market assumptions")
        
        if metrics.consistency_score < 75:
            recommendations.append("Ensure consistency across all business model components")
        
        if metrics.total_issues > 10:
            recommendations.append("Address high number of quality issues systematically")
        
        # Positive recommendations for good scores
        if metrics.overall_score >= 90:
            recommendations.append("Excellent quality - ready for stakeholder presentation")
        elif metrics.overall_score >= 80:
            recommendations.append("Good quality - minor improvements recommended")
        
        return recommendations

def main():
    parser = argparse.ArgumentParser(description="Comprehensive quality scoring for BMDP deliverables")
    parser.add_argument("--business", required=True, help="Business slug")
    parser.add_argument("--generate-report", action="store_true", help="Generate full quality report")
    parser.add_argument("--format", choices=["json", "summary", "dashboard"], default="summary")
    
    args = parser.parse_args()
    
    business_path = Path(f"businesses/{args.business}")
    if not business_path.exists():
        print(f"ERROR: Business path not found: {business_path}")
        return 1
    
    scorer = QualityScorer(str(business_path))
    
    if args.generate_report:
        dashboard = scorer.generate_quality_dashboard()
        
        if args.format == "json":
            print(json.dumps(dashboard, indent=2))
        elif args.format == "dashboard":
            # Rich dashboard format
            print(f"\n{'='*60}")
            print(f"QUALITY DASHBOARD: {args.business.upper()}")
            print(f"{'='*60}")
            
            metrics = dashboard["overall_metrics"]
            print(f"Overall Score: {metrics['score']}/100 (Grade: {metrics['grade']})")
            print(f"Quality Status: {dashboard['quality_status']}")
            print(f"Total Issues: {metrics['total_issues']}")
            if metrics['critical_issues'] > 0:
                print(f"🚨 Critical Issues: {metrics['critical_issues']}")
            
            print(f"\nDimension Scores:")
            for dim, score in dashboard["dimension_scores"].items():
                print(f"  {dim.replace('_', ' ').title()}: {score}/100")
            
            if dashboard["improvement_priorities"]:
                print(f"\nImprovement Priorities:")
                for priority in dashboard["improvement_priorities"]:
                    print(f"  {priority['priority']}: {priority['description']}")
                    print(f"    → {priority['action']}")
            
            if dashboard["recommendations"]:
                print(f"\nRecommendations:")
                for rec in dashboard["recommendations"]:
                    print(f"  • {rec}")
        else:
            # Summary format
            metrics = scorer.calculate_comprehensive_score()
            print(f"\n=== QUALITY SUMMARY: {args.business.upper()} ===")
            print(f"Overall Score: {metrics.overall_score}/100 (Grade: {metrics.grade})")
            print(f"Content Quality: {metrics.content_score}/100")
            print(f"Business Rules: {metrics.business_rules_score}/100") 
            print(f"Consistency: {metrics.consistency_score}/100")
            print(f"Total Issues: {metrics.total_issues}")
            if metrics.critical_issues > 0:
                print(f"🚨 Critical Issues: {metrics.critical_issues}")
    else:
        # Quick score only
        metrics = scorer.calculate_comprehensive_score()
        print(f"{args.business}: {metrics.overall_score}/100 ({metrics.grade}) - {metrics.total_issues} issues")
    
    return 0

if __name__ == "__main__":
    exit(main())
