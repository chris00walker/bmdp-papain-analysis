#!/usr/bin/env python3
"""
Value Proposition Design Validator - Implements Osterwalder & Pigneur VPD methodology validation
Based on "Value Proposition Design" by Alexander Osterwalder and Yves Pigneur
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
import argparse
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VPDValidationResult:
    component: str
    score: float
    issues: List[str]
    recommendations: List[str]
    evidence_quality: str

class VPDValidator:
    """Value Proposition Design methodology validator following Osterwalder & Pigneur principles"""
    
    def __init__(self, business_path: str):
        self.business_path = Path(business_path)
        self.business_slug = self.business_path.name
        
        # VPD Quality Standards from Osterwalder & Pigneur
        self.job_types = ["functional", "emotional", "social"]
        self.pain_severity_levels = ["extreme", "moderate", "mild"]
        self.gain_types = ["required", "expected", "desired", "unexpected"]
        
    def validate_jobs_to_be_done(self) -> VPDValidationResult:
        """Validate customer jobs identification following VPD methodology"""
        issues = []
        recommendations = []
        score = 0.0
        
        # Look for customer jobs in relevant deliverables
        jobs_content = self._extract_jobs_content()
        
        if not jobs_content:
            issues.append("No customer jobs content found in deliverables")
            return VPDValidationResult("jobs_to_be_done", 0.0, issues, 
                                     ["Create detailed customer jobs analysis"], "MISSING")
        
        # Validate functional jobs
        functional_score = self._validate_functional_jobs(jobs_content)
        emotional_score = self._validate_emotional_jobs(jobs_content)
        social_score = self._validate_social_jobs(jobs_content)
        context_score = self._validate_job_context(jobs_content)
        importance_score = self._validate_job_importance(jobs_content)
        
        # Calculate weighted score
        score = (functional_score * 0.4 + emotional_score * 0.2 + 
                social_score * 0.2 + context_score * 0.1 + importance_score * 0.1)
        
        # Generate issues and recommendations
        if functional_score < 80:
            issues.append("Functional jobs insufficiently detailed or missing")
            recommendations.append("Identify specific tasks customers are trying to accomplish")
        
        if emotional_score < 60:
            issues.append("Emotional jobs not adequately captured")
            recommendations.append("Understand how customers want to feel or avoid feeling")
        
        if social_score < 60:
            issues.append("Social jobs dimension missing or weak")
            recommendations.append("Identify how customers want to be perceived by others")
        
        if importance_score < 70:
            issues.append("Job importance ranking missing or unclear")
            recommendations.append("Rank jobs by significance to customer success")
        
        evidence_quality = self._assess_evidence_quality(jobs_content)
        
        return VPDValidationResult("jobs_to_be_done", score, issues, recommendations, evidence_quality)
    
    def validate_pain_gain_alignment(self) -> VPDValidationResult:
        """Validate pain points and gain creators following VPD methodology"""
        issues = []
        recommendations = []
        score = 0.0
        
        pain_gain_content = self._extract_pain_gain_content()
        
        if not pain_gain_content:
            issues.append("No pain/gain analysis found in deliverables")
            return VPDValidationResult("pain_gain_alignment", 0.0, issues,
                                     ["Create comprehensive pain/gain analysis"], "MISSING")
        
        # Validate pain analysis
        pain_score = self._validate_pain_analysis(pain_gain_content)
        gain_score = self._validate_gain_analysis(pain_gain_content)
        severity_score = self._validate_pain_severity(pain_gain_content)
        frequency_score = self._validate_pain_frequency(pain_gain_content)
        relevance_score = self._validate_gain_relevance(pain_gain_content)
        
        score = (pain_score * 0.25 + gain_score * 0.25 + severity_score * 0.2 + 
                frequency_score * 0.15 + relevance_score * 0.15)
        
        # Generate specific feedback
        if pain_score < 75:
            issues.append("Pain points analysis lacks depth or specificity")
            recommendations.append("Identify specific obstacles, frustrations, and risks customers face")
        
        if gain_score < 75:
            issues.append("Gain creators insufficiently developed")
            recommendations.append("Define outcomes and benefits customers want to achieve")
        
        if severity_score < 70:
            issues.append("Pain severity classification missing or inadequate")
            recommendations.append("Classify pains as extreme, moderate, or mild based on customer impact")
        
        if frequency_score < 70:
            issues.append("Pain frequency analysis missing")
            recommendations.append("Identify how often customers experience each pain point")
        
        evidence_quality = self._assess_evidence_quality(pain_gain_content)
        
        return VPDValidationResult("pain_gain_alignment", score, issues, recommendations, evidence_quality)
    
    def validate_canvas_coherence(self) -> VPDValidationResult:
        """Validate Value Proposition Canvas internal coherence"""
        issues = []
        recommendations = []
        score = 0.0
        
        canvas_content = self._extract_canvas_content()
        
        if not canvas_content:
            issues.append("Value Proposition Canvas not found or incomplete")
            return VPDValidationResult("canvas_coherence", 0.0, issues,
                                     ["Create complete Value Proposition Canvas"], "MISSING")
        
        # Validate canvas components alignment
        pain_reliever_match = self._validate_pain_reliever_match(canvas_content)
        gain_creator_alignment = self._validate_gain_creator_alignment(canvas_content)
        product_service_fit = self._validate_product_service_fit(canvas_content)
        value_prop_clarity = self._validate_value_proposition_clarity(canvas_content)
        differentiation = self._validate_differentiation_evidence(canvas_content)
        
        score = (pain_reliever_match * 0.25 + gain_creator_alignment * 0.25 + 
                product_service_fit * 0.2 + value_prop_clarity * 0.15 + differentiation * 0.15)
        
        # Generate coherence feedback
        if pain_reliever_match < 80:
            issues.append("Pain relievers don't adequately match identified pains")
            recommendations.append("Ensure each significant pain has corresponding pain reliever")
        
        if gain_creator_alignment < 80:
            issues.append("Gain creators misaligned with customer gains")
            recommendations.append("Align gain creators with identified customer gains and expectations")
        
        if product_service_fit < 75:
            issues.append("Products/services don't enable pain relievers and gain creators")
            recommendations.append("Ensure products/services directly enable value proposition delivery")
        
        if value_prop_clarity < 70:
            issues.append("Value proposition lacks clarity or measurability")
            recommendations.append("Make value propositions clear, specific, and measurable")
        
        if differentiation < 70:
            issues.append("Differentiation evidence insufficient")
            recommendations.append("Demonstrate unique value compared to alternatives")
        
        evidence_quality = self._assess_evidence_quality(canvas_content)
        
        return VPDValidationResult("canvas_coherence", score, issues, recommendations, evidence_quality)
    
    def _extract_jobs_content(self) -> str:
        """Extract customer jobs content from deliverables"""
        content = ""
        
        # Look in customer research and persona files
        job_files = [
            "20_understand/24_personas.md",
            "20_understand/25_customer_interviews.md", 
            "20_understand/31_insights.md",
            "30_design/35_canvas_v1_main.md"
        ]
        
        for file_path in job_files:
            full_path = self.business_path / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r') as f:
                        content += f.read() + "\n"
                except:
                    pass
        
        return content
    
    def _extract_pain_gain_content(self) -> str:
        """Extract pain/gain content from deliverables"""
        content = ""
        
        pain_gain_files = [
            "20_understand/31_insights.md",
            "30_design/35_canvas_v1_main.md",
            "30_design/36_value_prop_canvas.md"
        ]
        
        for file_path in pain_gain_files:
            full_path = self.business_path / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r') as f:
                        content += f.read() + "\n"
                except:
                    pass
        
        return content
    
    def _extract_canvas_content(self) -> str:
        """Extract Value Proposition Canvas content"""
        canvas_files = [
            "30_design/35_canvas_v1_main.md",
            "30_design/36_value_prop_canvas.md",
            "30_design/37_business_model_canvas.md"
        ]
        
        content = ""
        for file_path in canvas_files:
            full_path = self.business_path / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r') as f:
                        content += f.read() + "\n"
                except:
                    pass
        
        return content
    
    def _validate_functional_jobs(self, content: str) -> float:
        """Validate functional jobs identification"""
        functional_indicators = [
            "task", "accomplish", "complete", "achieve", "perform", "execute",
            "process", "workflow", "operation", "activity", "function"
        ]
        
        score = 0.0
        found_indicators = 0
        
        content_lower = content.lower()
        for indicator in functional_indicators:
            if indicator in content_lower:
                found_indicators += 1
        
        # Basic presence score
        if found_indicators >= 3:
            score += 40
        elif found_indicators >= 1:
            score += 20
        
        # Depth assessment
        if len(content) > 500:  # Substantial content
            score += 30
        elif len(content) > 200:
            score += 15
        
        # Specificity check
        if "customer" in content_lower and ("job" in content_lower or "task" in content_lower):
            score += 30
        
        return min(100, score)
    
    def _validate_emotional_jobs(self, content: str) -> float:
        """Validate emotional jobs identification"""
        emotional_indicators = [
            "feel", "emotion", "confident", "secure", "frustrated", "anxious",
            "satisfied", "happy", "worried", "stressed", "comfortable", "peace of mind"
        ]
        
        score = 0.0
        found_indicators = 0
        
        content_lower = content.lower()
        for indicator in emotional_indicators:
            if indicator in content_lower:
                found_indicators += 1
        
        if found_indicators >= 3:
            score += 60
        elif found_indicators >= 1:
            score += 30
        
        # Check for emotional context
        if "want to feel" in content_lower or "avoid feeling" in content_lower:
            score += 40
        
        return min(100, score)
    
    def _validate_social_jobs(self, content: str) -> float:
        """Validate social jobs identification"""
        social_indicators = [
            "perceived", "status", "reputation", "image", "appear", "look",
            "others think", "social", "peer", "community", "recognition"
        ]
        
        score = 0.0
        found_indicators = 0
        
        content_lower = content.lower()
        for indicator in social_indicators:
            if indicator in content_lower:
                found_indicators += 1
        
        if found_indicators >= 2:
            score += 70
        elif found_indicators >= 1:
            score += 35
        
        return min(100, score)
    
    def _validate_job_context(self, content: str) -> float:
        """Validate job context identification"""
        context_indicators = [
            "when", "where", "situation", "circumstance", "context", "scenario",
            "condition", "environment", "timing", "occasion"
        ]
        
        score = 0.0
        found_indicators = 0
        
        content_lower = content.lower()
        for indicator in context_indicators:
            if indicator in content_lower:
                found_indicators += 1
        
        if found_indicators >= 2:
            score = 80
        elif found_indicators >= 1:
            score = 50
        
        return score
    
    def _validate_job_importance(self, content: str) -> float:
        """Validate job importance ranking"""
        importance_indicators = [
            "important", "priority", "critical", "essential", "ranking",
            "most", "least", "high priority", "low priority", "significance"
        ]
        
        score = 0.0
        found_indicators = 0
        
        content_lower = content.lower()
        for indicator in importance_indicators:
            if indicator in content_lower:
                found_indicators += 1
        
        if found_indicators >= 3:
            score = 85
        elif found_indicators >= 1:
            score = 50
        
        return score
    
    def _validate_pain_analysis(self, content: str) -> float:
        """Validate pain points analysis quality"""
        pain_indicators = [
            "pain", "problem", "frustration", "obstacle", "barrier", "difficulty",
            "challenge", "issue", "concern", "risk", "fear", "annoyance"
        ]
        
        score = 0.0
        found_indicators = 0
        
        content_lower = content.lower()
        for indicator in pain_indicators:
            if indicator in content_lower:
                found_indicators += 1
        
        if found_indicators >= 4:
            score += 50
        elif found_indicators >= 2:
            score += 25
        
        # Check for pain specificity
        if len(content) > 300:
            score += 30
        
        # Check for customer-centric language
        if "customer" in content_lower and found_indicators >= 2:
            score += 20
        
        return min(100, score)
    
    def _validate_gain_analysis(self, content: str) -> float:
        """Validate gain creators analysis quality"""
        gain_indicators = [
            "gain", "benefit", "outcome", "result", "value", "advantage",
            "improvement", "solution", "success", "achievement", "reward"
        ]
        
        score = 0.0
        found_indicators = 0
        
        content_lower = content.lower()
        for indicator in gain_indicators:
            if indicator in content_lower:
                found_indicators += 1
        
        if found_indicators >= 4:
            score += 50
        elif found_indicators >= 2:
            score += 25
        
        if len(content) > 300:
            score += 30
        
        if "customer" in content_lower and found_indicators >= 2:
            score += 20
        
        return min(100, score)
    
    def _validate_pain_severity(self, content: str) -> float:
        """Validate pain severity classification"""
        severity_indicators = ["extreme", "moderate", "mild", "severe", "critical", "minor"]
        
        found_severity = 0
        content_lower = content.lower()
        
        for indicator in severity_indicators:
            if indicator in content_lower:
                found_severity += 1
        
        if found_severity >= 2:
            return 80
        elif found_severity >= 1:
            return 50
        else:
            return 0
    
    def _validate_pain_frequency(self, content: str) -> float:
        """Validate pain frequency analysis"""
        frequency_indicators = [
            "often", "frequent", "always", "sometimes", "rarely", "daily",
            "weekly", "monthly", "occasionally", "regularly"
        ]
        
        found_frequency = 0
        content_lower = content.lower()
        
        for indicator in frequency_indicators:
            if indicator in content_lower:
                found_frequency += 1
        
        if found_frequency >= 2:
            return 75
        elif found_frequency >= 1:
            return 45
        else:
            return 0
    
    def _validate_gain_relevance(self, content: str) -> float:
        """Validate gain relevance assessment"""
        relevance_indicators = [
            "required", "expected", "desired", "unexpected", "nice to have",
            "must have", "important", "essential", "critical"
        ]
        
        found_relevance = 0
        content_lower = content.lower()
        
        for indicator in relevance_indicators:
            if indicator in content_lower:
                found_relevance += 1
        
        if found_relevance >= 3:
            return 80
        elif found_relevance >= 1:
            return 50
        else:
            return 0
    
    def _validate_pain_reliever_match(self, content: str) -> float:
        """Validate pain reliever matching"""
        # Look for explicit connections between pains and relievers
        match_indicators = [
            "reliever", "solve", "address", "eliminate", "reduce", "mitigate",
            "alleviate", "prevent", "avoid", "overcome"
        ]
        
        score = 0.0
        content_lower = content.lower()
        
        # Check for pain-reliever connections
        if "pain" in content_lower:
            for indicator in match_indicators:
                if indicator in content_lower:
                    score += 20
        
        return min(100, score)
    
    def _validate_gain_creator_alignment(self, content: str) -> float:
        """Validate gain creator alignment"""
        alignment_indicators = [
            "create", "deliver", "provide", "enable", "generate", "produce",
            "achieve", "realize", "fulfill", "satisfy"
        ]
        
        score = 0.0
        content_lower = content.lower()
        
        if "gain" in content_lower:
            for indicator in alignment_indicators:
                if indicator in content_lower:
                    score += 20
        
        return min(100, score)
    
    def _validate_product_service_fit(self, content: str) -> float:
        """Validate product/service fit with value proposition"""
        fit_indicators = [
            "product", "service", "feature", "capability", "offering",
            "solution", "tool", "platform", "system"
        ]
        
        score = 0.0
        found_products = 0
        content_lower = content.lower()
        
        for indicator in fit_indicators:
            if indicator in content_lower:
                found_products += 1
        
        if found_products >= 3:
            score = 75
        elif found_products >= 1:
            score = 45
        
        return score
    
    def _validate_value_proposition_clarity(self, content: str) -> float:
        """Validate value proposition clarity"""
        clarity_indicators = [
            "value proposition", "unique value", "benefit", "advantage",
            "differentiation", "why choose", "better than"
        ]
        
        score = 0.0
        found_clarity = 0
        content_lower = content.lower()
        
        for indicator in clarity_indicators:
            if indicator in content_lower:
                found_clarity += 1
        
        if found_clarity >= 2:
            score = 80
        elif found_clarity >= 1:
            score = 50
        
        return score
    
    def _validate_differentiation_evidence(self, content: str) -> float:
        """Validate differentiation evidence"""
        diff_indicators = [
            "unique", "different", "competitive advantage", "better than",
            "unlike", "superior", "distinctive", "exclusive"
        ]
        
        score = 0.0
        found_diff = 0
        content_lower = content.lower()
        
        for indicator in diff_indicators:
            if indicator in content_lower:
                found_diff += 1
        
        if found_diff >= 2:
            score = 75
        elif found_diff >= 1:
            score = 40
        
        return score
    
    def _assess_evidence_quality(self, content: str) -> str:
        """Assess quality of evidence supporting VPD analysis"""
        evidence_indicators = [
            "interview", "survey", "research", "data", "study", "analysis",
            "customer feedback", "observation", "test", "validation"
        ]
        
        found_evidence = 0
        content_lower = content.lower()
        
        for indicator in evidence_indicators:
            if indicator in content_lower:
                found_evidence += 1
        
        if found_evidence >= 4:
            return "STRONG"
        elif found_evidence >= 2:
            return "MODERATE"
        elif found_evidence >= 1:
            return "WEAK"
        else:
            return "MISSING"
    
    def generate_vpd_report(self) -> Dict:
        """Generate comprehensive VPD validation report"""
        jobs_result = self.validate_jobs_to_be_done()
        pain_gain_result = self.validate_pain_gain_alignment()
        canvas_result = self.validate_canvas_coherence()
        
        # Calculate overall VPD score
        overall_score = (jobs_result.score * 0.4 + pain_gain_result.score * 0.35 + 
                        canvas_result.score * 0.25)
        
        # Determine VPD grade
        if overall_score >= 90:
            grade = "A+"
        elif overall_score >= 85:
            grade = "A"
        elif overall_score >= 80:
            grade = "B+"
        elif overall_score >= 75:
            grade = "B"
        elif overall_score >= 70:
            grade = "C+"
        elif overall_score >= 65:
            grade = "C"
        else:
            grade = "F"
        
        return {
            "business": self.business_slug,
            "timestamp": datetime.now().isoformat(),
            "vpd_methodology_compliance": {
                "overall_score": round(overall_score, 1),
                "grade": grade,
                "osterwalder_pigneur_standard": "Value Proposition Design"
            },
            "component_scores": {
                "jobs_to_be_done": {
                    "score": jobs_result.score,
                    "evidence_quality": jobs_result.evidence_quality,
                    "issues": jobs_result.issues,
                    "recommendations": jobs_result.recommendations
                },
                "pain_gain_alignment": {
                    "score": pain_gain_result.score,
                    "evidence_quality": pain_gain_result.evidence_quality,
                    "issues": pain_gain_result.issues,
                    "recommendations": pain_gain_result.recommendations
                },
                "canvas_coherence": {
                    "score": canvas_result.score,
                    "evidence_quality": canvas_result.evidence_quality,
                    "issues": canvas_result.issues,
                    "recommendations": canvas_result.recommendations
                }
            },
            "methodology_assessment": {
                "customer_job_fit": "STRONG" if jobs_result.score >= 80 else "NEEDS_IMPROVEMENT",
                "value_proposition_market_fit": "STRONG" if canvas_result.score >= 80 else "NEEDS_IMPROVEMENT",
                "evidence_based_validation": "STRONG" if all(r.evidence_quality in ["STRONG", "MODERATE"] 
                                                           for r in [jobs_result, pain_gain_result, canvas_result]) else "WEAK"
            }
        }

def main():
    parser = argparse.ArgumentParser(description="Value Proposition Design methodology validator")
    parser.add_argument("--business", required=True, help="Business slug")
    parser.add_argument("--validate", choices=["jobs-to-be-done", "pain-gain-alignment", "canvas-coherence", "all"], 
                       default="all", help="Validation component")
    parser.add_argument("--format", choices=["json", "summary"], default="summary")
    
    args = parser.parse_args()
    
    business_path = Path(f"businesses/{args.business}")
    if not business_path.exists():
        print(f"ERROR: Business path not found: {business_path}")
        return 1
    
    validator = VPDValidator(str(business_path))
    
    if args.validate == "all":
        report = validator.generate_vpd_report()
        
        if args.format == "json":
            print(json.dumps(report, indent=2))
        else:
            print(f"\n=== VALUE PROPOSITION DESIGN VALIDATION: {args.business.upper()} ===")
            print(f"Overall VPD Score: {report['vpd_methodology_compliance']['overall_score']}/100 "
                  f"(Grade: {report['vpd_methodology_compliance']['grade']})")
            
            for component, data in report['component_scores'].items():
                print(f"\n{component.replace('_', ' ').title()}: {data['score']}/100 "
                      f"(Evidence: {data['evidence_quality']})")
                if data['issues']:
                    for issue in data['issues']:
                        print(f"  ⚠️  {issue}")
                if data['recommendations']:
                    for rec in data['recommendations']:
                        print(f"  💡 {rec}")
    else:
        # Single component validation
        if args.validate == "jobs-to-be-done":
            result = validator.validate_jobs_to_be_done()
        elif args.validate == "pain-gain-alignment":
            result = validator.validate_pain_gain_alignment()
        elif args.validate == "canvas-coherence":
            result = validator.validate_canvas_coherence()
        
        print(f"\n{result.component.replace('_', ' ').title()}: {result.score}/100")
        print(f"Evidence Quality: {result.evidence_quality}")
        
        if result.issues:
            print("\nIssues:")
            for issue in result.issues:
                print(f"  - {issue}")
        
        if result.recommendations:
            print("\nRecommendations:")
            for rec in result.recommendations:
                print(f"  - {rec}")
    
    return 0

if __name__ == "__main__":
    exit(main())
