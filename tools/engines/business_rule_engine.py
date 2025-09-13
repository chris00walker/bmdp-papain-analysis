#!/usr/bin/env python3
"""
Business Rule Engine - Validates financial calculations and business logic in BMDP deliverables
"""

import os
import json
import re
import csv
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum
import argparse

class RuleViolationSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high" 
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class RuleViolation:
    rule_name: str
    severity: RuleViolationSeverity
    description: str
    expected_value: Any
    actual_value: Any
    deliverable: str
    recommendation: str

class BusinessRuleEngine:
    """Validates business logic and financial calculations across BMDP deliverables"""
    
    def __init__(self, business_path: str):
        self.business_path = Path(business_path)
        self.business_slug = self.business_path.name
        self.business_data = self._load_business_data()
        
        # Define business rules
        self.financial_rules = {
            "revenue_growth_realistic": {
                "max_yoy_growth": 3.0,  # 300% max YoY growth
                "severity": RuleViolationSeverity.HIGH
            },
            "margin_validation": {
                "gross_margin_range": (0.15, 0.95),
                "net_margin_range": (0.02, 0.40),
                "severity": RuleViolationSeverity.MEDIUM
            },
            "roi_validation": {
                "minimum_roi": 0.12,  # 12% minimum ROI
                "maximum_roi": 2.0,   # 200% maximum realistic ROI
                "severity": RuleViolationSeverity.HIGH
            },
            "payback_period": {
                "maximum_months": 72,  # 6 years max payback
                "severity": RuleViolationSeverity.MEDIUM
            },
            "ltv_cac_ratio": {
                "minimum_ratio": 3.0,
                "optimal_ratio": 5.0,
                "severity": RuleViolationSeverity.HIGH
            },
            "cash_flow_consistency": {
                "negative_periods_max": 24,  # Max 2 years negative cash flow
                "severity": RuleViolationSeverity.CRITICAL
            }
        }
        
        self.market_rules = {
            "market_share_realistic": {
                "max_initial_share": 0.05,  # 5% max initial market share
                "max_mature_share": 0.25,   # 25% max mature market share
                "severity": RuleViolationSeverity.HIGH
            },
            "customer_acquisition": {
                "cac_percentage_of_ltv": 0.33,  # CAC should be <33% of LTV
                "severity": RuleViolationSeverity.MEDIUM
            },
            "pricing_validation": {
                "cost_plus_minimum": 1.2,  # Minimum 20% markup
                "value_based_maximum": 10.0,  # Maximum 10x cost
                "severity": RuleViolationSeverity.MEDIUM
            }
        }
        
        self.consistency_rules = {
            "cross_deliverable_alignment": {
                "value_prop_consistency": True,
                "financial_assumption_consistency": True,
                "customer_segment_consistency": True,
                "severity": RuleViolationSeverity.HIGH
            }
        }
    
    def _load_business_data(self) -> Dict:
        """Load business data from brief and manifest"""
        try:
            # Try to load from manifest first
            manifest_path = self.business_path / "manifest.json"
            if manifest_path.exists():
                with open(manifest_path, 'r') as f:
                    return json.load(f)
            
            # Fallback to parsing brief
            brief_files = list(Path('.').glob(f"brief-*{self.business_slug}*.md"))
            if brief_files:
                return self._parse_brief_file(brief_files[0])
            
            return {}
        except Exception as e:
            print(f"Warning: Could not load business data: {e}")
            return {}
    
    def _parse_brief_file(self, brief_path: Path) -> Dict:
        """Parse business brief for key financial data"""
        try:
            with open(brief_path, 'r') as f:
                content = f.read()
            
            # Extract key financial metrics
            data = {}
            
            # Capital bounds
            capital_match = re.search(r'capital.*?(\$[\d,]+).*?(\$[\d,]+)', content, re.IGNORECASE)
            if capital_match:
                data['capital_min'] = self._parse_currency(capital_match.group(1))
                data['capital_max'] = self._parse_currency(capital_match.group(2))
            
            # ROI target
            roi_match = re.search(r'roi.*?(\d+)%', content, re.IGNORECASE)
            if roi_match:
                data['roi_target'] = float(roi_match.group(1)) / 100
            
            return data
        except Exception:
            return {}
    
    def _parse_currency(self, currency_str: str) -> float:
        """Parse currency string to float"""
        # Remove currency symbols and convert K/M/B suffixes
        clean_str = re.sub(r'[$,]', '', currency_str)
        
        if 'K' in clean_str.upper():
            return float(clean_str.upper().replace('K', '')) * 1000
        elif 'M' in clean_str.upper():
            return float(clean_str.upper().replace('M', '')) * 1000000
        elif 'B' in clean_str.upper():
            return float(clean_str.upper().replace('B', '')) * 1000000000
        else:
            return float(clean_str)
    
    def validate_financial_projections(self, projections_file: Path) -> List[RuleViolation]:
        """Validate financial projections against business rules"""
        violations = []
        
        if not projections_file.exists():
            return violations
        
        try:
            content = projections_file.read_text()
            
            # Extract financial metrics
            revenues = self._extract_revenue_projections(content)
            margins = self._extract_margin_data(content)
            roi_values = self._extract_roi_data(content)
            
            # Validate revenue growth
            violations.extend(self._validate_revenue_growth(revenues, projections_file.name))
            
            # Validate margins
            violations.extend(self._validate_margins(margins, projections_file.name))
            
            # Validate ROI
            violations.extend(self._validate_roi(roi_values, projections_file.name))
            
        except Exception as e:
            violations.append(RuleViolation(
                rule_name="file_parsing_error",
                severity=RuleViolationSeverity.MEDIUM,
                description=f"Could not parse financial projections: {e}",
                expected_value="Valid financial data",
                actual_value="Unparseable content",
                deliverable=projections_file.name,
                recommendation="Ensure financial data is properly formatted"
            ))
        
        return violations
    
    def _extract_revenue_projections(self, content: str) -> List[float]:
        """Extract revenue projections from content"""
        # Look for revenue patterns in tables or text
        revenue_patterns = [
            r'revenue.*?(\$[\d,]+(?:\.\d+)?[KMB]?)',
            r'(\$[\d,]+(?:\.\d+)?[KMB]?).*?revenue',
            r'Year \d+.*?(\$[\d,]+(?:\.\d+)?[KMB]?)'
        ]
        
        revenues = []
        for pattern in revenue_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    revenues.append(self._parse_currency(match))
                except:
                    continue
        
        return sorted(set(revenues))  # Remove duplicates and sort
    
    def _extract_margin_data(self, content: str) -> Dict[str, List[float]]:
        """Extract margin data from content"""
        margins = {"gross": [], "net": []}
        
        # Gross margin patterns
        gross_patterns = [
            r'gross margin.*?(\d+(?:\.\d+)?)%',
            r'(\d+(?:\.\d+)?)%.*?gross margin'
        ]
        
        for pattern in gross_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    margins["gross"].append(float(match) / 100)
                except:
                    continue
        
        # Net margin patterns
        net_patterns = [
            r'net margin.*?(\d+(?:\.\d+)?)%',
            r'profit margin.*?(\d+(?:\.\d+)?)%'
        ]
        
        for pattern in net_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    margins["net"].append(float(match) / 100)
                except:
                    continue
        
        return margins
    
    def _extract_roi_data(self, content: str) -> List[float]:
        """Extract ROI data from content"""
        roi_patterns = [
            r'roi.*?(\d+(?:\.\d+)?)%',
            r'return.*?(\d+(?:\.\d+)?)%',
            r'(\d+(?:\.\d+)?)%.*?return'
        ]
        
        roi_values = []
        for pattern in roi_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    roi_values.append(float(match) / 100)
                except:
                    continue
        
        return roi_values
    
    def _validate_revenue_growth(self, revenues: List[float], deliverable: str) -> List[RuleViolation]:
        """Validate revenue growth rates"""
        violations = []
        
        if len(revenues) < 2:
            return violations
        
        for i in range(1, len(revenues)):
            if revenues[i-1] > 0:  # Avoid division by zero
                growth_rate = (revenues[i] - revenues[i-1]) / revenues[i-1]
                max_growth = self.financial_rules["revenue_growth_realistic"]["max_yoy_growth"]
                
                if growth_rate > max_growth:
                    violations.append(RuleViolation(
                        rule_name="revenue_growth_realistic",
                        severity=self.financial_rules["revenue_growth_realistic"]["severity"],
                        description=f"Revenue growth rate exceeds realistic threshold",
                        expected_value=f"≤{max_growth*100:.0f}% YoY growth",
                        actual_value=f"{growth_rate*100:.1f}% YoY growth",
                        deliverable=deliverable,
                        recommendation="Revise revenue projections to more realistic growth rates"
                    ))
        
        return violations
    
    def _validate_margins(self, margins: Dict[str, List[float]], deliverable: str) -> List[RuleViolation]:
        """Validate margin ranges"""
        violations = []
        
        for margin_type, values in margins.items():
            if not values:
                continue
            
            rule_key = "margin_validation"
            range_key = f"{margin_type}_margin_range"
            
            if range_key in self.financial_rules[rule_key]:
                min_margin, max_margin = self.financial_rules[rule_key][range_key]
                
                for value in values:
                    if value < min_margin or value > max_margin:
                        violations.append(RuleViolation(
                            rule_name=f"{margin_type}_margin_validation",
                            severity=self.financial_rules[rule_key]["severity"],
                            description=f"{margin_type.title()} margin outside realistic range",
                            expected_value=f"{min_margin*100:.0f}%-{max_margin*100:.0f}%",
                            actual_value=f"{value*100:.1f}%",
                            deliverable=deliverable,
                            recommendation=f"Adjust {margin_type} margin to realistic industry range"
                        ))
        
        return violations
    
    def _validate_roi(self, roi_values: List[float], deliverable: str) -> List[RuleViolation]:
        """Validate ROI values"""
        violations = []
        
        rule = self.financial_rules["roi_validation"]
        min_roi = rule["minimum_roi"]
        max_roi = rule["maximum_roi"]
        
        for roi in roi_values:
            if roi < min_roi:
                violations.append(RuleViolation(
                    rule_name="roi_too_low",
                    severity=rule["severity"],
                    description="ROI below minimum viable threshold",
                    expected_value=f"≥{min_roi*100:.0f}%",
                    actual_value=f"{roi*100:.1f}%",
                    deliverable=deliverable,
                    recommendation="Improve business model to achieve minimum ROI threshold"
                ))
            elif roi > max_roi:
                violations.append(RuleViolation(
                    rule_name="roi_too_high",
                    severity=rule["severity"],
                    description="ROI exceeds realistic expectations",
                    expected_value=f"≤{max_roi*100:.0f}%",
                    actual_value=f"{roi*100:.1f}%",
                    deliverable=deliverable,
                    recommendation="Validate ROI calculations and assumptions"
                ))
        
        return violations
    
    def validate_cashflow_file(self, cashflow_file: Path) -> List[RuleViolation]:
        """Validate cash flow projections from CSV file"""
        violations = []
        
        if not cashflow_file.exists():
            return violations
        
        try:
            with open(cashflow_file, 'r') as f:
                reader = csv.DictReader(f)
                cash_flows = []
                
                for row in reader:
                    # Look for cash flow columns
                    for key, value in row.items():
                        if 'cash' in key.lower() and 'flow' in key.lower():
                            try:
                                cash_flows.append(float(value.replace('$', '').replace(',', '')))
                            except:
                                continue
                
                # Validate cash flow patterns
                if cash_flows:
                    negative_periods = sum(1 for cf in cash_flows if cf < 0)
                    max_negative = self.financial_rules["cash_flow_consistency"]["negative_periods_max"]
                    
                    if negative_periods > max_negative:
                        violations.append(RuleViolation(
                            rule_name="excessive_negative_cashflow",
                            severity=self.financial_rules["cash_flow_consistency"]["severity"],
                            description="Too many periods of negative cash flow",
                            expected_value=f"≤{max_negative} negative periods",
                            actual_value=f"{negative_periods} negative periods",
                            deliverable=cashflow_file.name,
                            recommendation="Revise business model to achieve positive cash flow sooner"
                        ))
        
        except Exception as e:
            violations.append(RuleViolation(
                rule_name="cashflow_parsing_error",
                severity=RuleViolationSeverity.MEDIUM,
                description=f"Could not parse cash flow file: {e}",
                expected_value="Valid CSV with cash flow data",
                actual_value="Unparseable file",
                deliverable=cashflow_file.name,
                recommendation="Ensure cash flow file is properly formatted CSV"
            ))
        
        return violations
    
    def validate_business_consistency(self) -> List[RuleViolation]:
        """Validate consistency across all business deliverables"""
        violations = []
        
        # Load key deliverables for consistency checking
        deliverables = {}
        
        # Load canvas files
        canvas_files = list(self.business_path.rglob("*canvas*.md"))
        for canvas_file in canvas_files:
            deliverables[f"canvas_{canvas_file.stem}"] = canvas_file.read_text()
        
        # Load insights and recommendations
        insight_files = list(self.business_path.rglob("*insights*.md"))
        for insight_file in insight_files:
            deliverables[f"insights_{insight_file.stem}"] = insight_file.read_text()
        
        recommendation_files = list(self.business_path.rglob("*recommendation*.md"))
        for rec_file in recommendation_files:
            deliverables[f"recommendation_{rec_file.stem}"] = rec_file.read_text()
        
        # Check value proposition consistency
        value_props = []
        for name, content in deliverables.items():
            vp_matches = re.findall(r'value proposition[:\s]+([^.\n]+)', content, re.IGNORECASE)
            value_props.extend([(name, vp.strip()) for vp in vp_matches])
        
        if len(set(vp for _, vp in value_props)) > 2:  # Allow some variation
            violations.append(RuleViolation(
                rule_name="value_proposition_inconsistency",
                severity=RuleViolationSeverity.HIGH,
                description="Value propositions vary significantly across deliverables",
                expected_value="Consistent value proposition",
                actual_value=f"{len(set(vp for _, vp in value_props))} different value propositions",
                deliverable="Multiple deliverables",
                recommendation="Align value propositions across all business model components"
            ))
        
        return violations
    
    def validate_all_rules(self) -> Dict[str, List[RuleViolation]]:
        """Run all business rule validations"""
        all_violations = {}
        
        # Financial projections validation
        financial_files = list(self.business_path.rglob("*financial*.md")) + \
                         list(self.business_path.rglob("*projection*.md"))
        
        for file in financial_files:
            violations = self.validate_financial_projections(file)
            if violations:
                all_violations[f"financial_{file.name}"] = violations
        
        # Cash flow validation
        cashflow_files = list(self.business_path.rglob("*cashflow*.csv"))
        for file in cashflow_files:
            violations = self.validate_cashflow_file(file)
            if violations:
                all_violations[f"cashflow_{file.name}"] = violations
        
        # Consistency validation
        consistency_violations = self.validate_business_consistency()
        if consistency_violations:
            all_violations["consistency"] = consistency_violations
        
        return all_violations
    
    def generate_rule_report(self) -> Dict:
        """Generate comprehensive business rule validation report"""
        all_violations = self.validate_all_rules()
        
        # Categorize violations by severity
        severity_counts = {severity: 0 for severity in RuleViolationSeverity}
        total_violations = 0
        
        for violations in all_violations.values():
            for violation in violations:
                severity_counts[violation.severity] += 1
                total_violations += 1
        
        # Calculate compliance score
        critical_weight = 25
        high_weight = 10
        medium_weight = 5
        low_weight = 1
        
        penalty_score = (
            severity_counts[RuleViolationSeverity.CRITICAL] * critical_weight +
            severity_counts[RuleViolationSeverity.HIGH] * high_weight +
            severity_counts[RuleViolationSeverity.MEDIUM] * medium_weight +
            severity_counts[RuleViolationSeverity.LOW] * low_weight
        )
        
        compliance_score = max(0, 100 - penalty_score)
        
        return {
            "business": self.business_slug,
            "compliance_score": compliance_score,
            "total_violations": total_violations,
            "severity_breakdown": {sev.value: count for sev, count in severity_counts.items()},
            "violations_by_category": {
                category: [v.__dict__ for v in violations] 
                for category, violations in all_violations.items()
            },
            "recommendations": self._generate_priority_recommendations(all_violations)
        }
    
    def _generate_priority_recommendations(self, all_violations: Dict[str, List[RuleViolation]]) -> List[str]:
        """Generate prioritized recommendations based on violations"""
        recommendations = []
        
        # Critical issues first
        critical_violations = []
        for violations in all_violations.values():
            critical_violations.extend([v for v in violations if v.severity == RuleViolationSeverity.CRITICAL])
        
        if critical_violations:
            recommendations.append("CRITICAL: Address cash flow and fundamental business model issues immediately")
        
        # High priority issues
        high_violations = []
        for violations in all_violations.values():
            high_violations.extend([v for v in violations if v.severity == RuleViolationSeverity.HIGH])
        
        if high_violations:
            recommendations.append("HIGH: Validate financial projections and market assumptions")
        
        # Specific recommendations
        financial_issues = sum(1 for category in all_violations.keys() if 'financial' in category)
        if financial_issues > 0:
            recommendations.append("Review and validate all financial calculations and assumptions")
        
        consistency_issues = 'consistency' in all_violations
        if consistency_issues:
            recommendations.append("Align business model components for consistency across deliverables")
        
        return recommendations

def main():
    parser = argparse.ArgumentParser(description="Business rule validation for BMDP deliverables")
    parser.add_argument("--business", required=True, help="Business slug")
    parser.add_argument("--validate-all", action="store_true", help="Run all validations")
    parser.add_argument("--financial-only", action="store_true", help="Validate financial rules only")
    parser.add_argument("--format", choices=["json", "summary"], default="summary")
    
    args = parser.parse_args()
    
    business_path = Path(f"businesses/{args.business}")
    if not business_path.exists():
        print(f"ERROR: Business path not found: {business_path}")
        return 1
    
    engine = BusinessRuleEngine(str(business_path))
    
    if args.validate_all:
        report = engine.generate_rule_report()
        
        if args.format == "json":
            print(json.dumps(report, indent=2, default=str))
        else:
            print(f"\n=== BUSINESS RULE VALIDATION: {args.business.upper()} ===")
            print(f"Compliance Score: {report['compliance_score']:.1f}/100")
            print(f"Total Violations: {report['total_violations']}")
            
            if report['total_violations'] > 0:
                print(f"\nSeverity Breakdown:")
                for severity, count in report['severity_breakdown'].items():
                    if count > 0:
                        print(f"  {severity.upper()}: {count}")
                
                print(f"\nPriority Recommendations:")
                for rec in report['recommendations']:
                    print(f"  • {rec}")
            else:
                print("\n✅ All business rules validated successfully!")
    
    return 0

if __name__ == "__main__":
    exit(main())
