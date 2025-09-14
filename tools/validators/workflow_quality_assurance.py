#!/usr/bin/env python3
"""
Workflow Quality Assurance - Ensures all workflow outputs meet quality standards
Follows single responsibility principle: validates and reports on workflow output quality
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse
from dataclasses import dataclass
from datetime import datetime

@dataclass
class QualityIssue:
    """Represents a quality issue found in workflow output"""
    file_path: str
    issue_type: str
    description: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    line_number: Optional[int] = None

class WorkflowQualityAssurance:
    """Validates workflow output quality and ensures proper variable substitution"""
    
    def __init__(self, business: str):
        self.business = business
        self.business_path = Path(f'/home/chris/bmdp/businesses/{business}')
        self.issues: List[QualityIssue] = []
        
        # Quality check patterns
        self.quality_patterns = {
            'placeholder_content': re.compile(r'Template content for|^\[.*\]$|^TBD$', re.MULTILINE),
            'unsubstituted_vars': re.compile(r'\$[A-Z_]+|\$\{[A-Z_]+\}'),
            'broken_substitution': re.compile(r'\\[a-z]+[0-9]?M|\\[a-z]+'),
            'empty_sections': re.compile(r'^#+\s*$', re.MULTILINE),
            'missing_content': re.compile(r'^\s*$', re.MULTILINE)
        }
        
        # Critical variables that must be substituted
        self.critical_variables = [
            'VALUE_PROPOSITION', 'CUSTOMER_SEGMENTS', 'KEY_ACTIVITIES',
            'KEY_RESOURCES', 'REVENUE_STREAMS', 'CAPITAL_MIN', 'CAPITAL_MAX',
            'BUSINESS_TITLE', 'TEAM_SIZE', 'DISCOUNT_RATE'
        ]
    
    def check_parser_variables(self) -> bool:
        """Verify parser exports all required variables"""
        cmd = [
            'python', 'tools/parsers/brief_parser.py',
            '--business', self.business,
            '--output-format', 'env'
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd='/home/chris/bmdp',
                timeout=10
            )
            
            if result.returncode != 0:
                self.issues.append(QualityIssue(
                    file_path='brief_parser.py',
                    issue_type='parser_error',
                    description=f"Parser failed: {result.stderr}",
                    severity='critical'
                ))
                return False
            
            # Check for critical variables
            missing_vars = []
            for var in self.critical_variables:
                if f"{var}=" not in result.stdout:
                    missing_vars.append(var)
            
            if missing_vars:
                self.issues.append(QualityIssue(
                    file_path='brief_parser.py',
                    issue_type='missing_variables',
                    description=f"Parser missing variables: {', '.join(missing_vars)}",
                    severity='critical'
                ))
                return False
                
            return True
            
        except Exception as e:
            self.issues.append(QualityIssue(
                file_path='brief_parser.py',
                issue_type='parser_exception',
                description=str(e),
                severity='critical'
            ))
            return False
    
    def check_file_quality(self, file_path: Path) -> List[QualityIssue]:
        """Check a single file for quality issues"""
        local_issues = []
        
        if not file_path.exists():
            return local_issues
        
        # Skip non-text files
        if file_path.suffix not in ['.md', '.csv', '.json', '.txt']:
            return local_issues
        
        try:
            content = file_path.read_text()
            
            # Check for placeholder content
            if self.quality_patterns['placeholder_content'].search(content):
                local_issues.append(QualityIssue(
                    file_path=str(file_path.relative_to(self.business_path)),
                    issue_type='placeholder_content',
                    description='File contains placeholder/template content',
                    severity='high'
                ))
            
            # Check for unsubstituted variables (only in .md files)
            if file_path.suffix == '.md':
                unsubstituted = self.quality_patterns['unsubstituted_vars'].findall(content)
                # Filter out legitimate uses (like dollar amounts)
                unsubstituted = [v for v in unsubstituted if not re.match(r'\$\d+', v)]
                if unsubstituted:
                    local_issues.append(QualityIssue(
                        file_path=str(file_path.relative_to(self.business_path)),
                        issue_type='unsubstituted_variables',
                        description=f'Unsubstituted variables found: {", ".join(set(unsubstituted[:5]))}',
                        severity='high'
                    ))
            
            # Check for broken substitutions
            if self.quality_patterns['broken_substitution'].search(content):
                local_issues.append(QualityIssue(
                    file_path=str(file_path.relative_to(self.business_path)),
                    issue_type='broken_substitution',
                    description='Broken variable substitutions detected',
                    severity='high'
                ))
            
            # Check for empty content (files under 50 bytes are suspicious)
            if len(content.strip()) < 50:
                local_issues.append(QualityIssue(
                    file_path=str(file_path.relative_to(self.business_path)),
                    issue_type='insufficient_content',
                    description='File has insufficient content',
                    severity='medium'
                ))
                
        except Exception as e:
            local_issues.append(QualityIssue(
                file_path=str(file_path.relative_to(self.business_path)),
                issue_type='read_error',
                description=str(e),
                severity='low'
            ))
        
        return local_issues
    
    def check_phase_quality(self, phase: int) -> List[QualityIssue]:
        """Check quality of all files in a phase"""
        phase_dirs = {
            0: '00_initiation',
            1: '10_mobilize',
            2: '20_understand',
            3: '30_design'
        }
        
        if phase not in phase_dirs:
            return []
        
        phase_path = self.business_path / phase_dirs[phase]
        if not phase_path.exists():
            return [QualityIssue(
                file_path=phase_dirs[phase],
                issue_type='missing_directory',
                description=f'Phase {phase} directory does not exist',
                severity='critical'
            )]
        
        phase_issues = []
        for file_path in phase_path.rglob('*'):
            if file_path.is_file():
                phase_issues.extend(self.check_file_quality(file_path))
        
        return phase_issues
    
    def validate_all_phases(self) -> Tuple[bool, Dict[str, any]]:
        """Validate quality across all phases"""
        # First check parser
        parser_ok = self.check_parser_variables()
        
        # Check each phase
        for phase in range(4):
            phase_issues = self.check_phase_quality(phase)
            self.issues.extend(phase_issues)
        
        # Check manifest
        manifest_path = self.business_path / 'manifest.json'
        if not manifest_path.exists():
            self.issues.append(QualityIssue(
                file_path='manifest.json',
                issue_type='missing_file',
                description='Business manifest not found',
                severity='high'
            ))
        
        # Categorize issues by severity
        critical_issues = [i for i in self.issues if i.severity == 'critical']
        high_issues = [i for i in self.issues if i.severity == 'high']
        medium_issues = [i for i in self.issues if i.severity == 'medium']
        low_issues = [i for i in self.issues if i.severity == 'low']
        
        # Calculate quality score
        total_penalty = (
            len(critical_issues) * 25 +
            len(high_issues) * 10 +
            len(medium_issues) * 5 +
            len(low_issues) * 2
        )
        quality_score = max(0, 100 - total_penalty)
        
        # Determine pass/fail
        passed = len(critical_issues) == 0 and quality_score >= 70
        
        report = {
            'business': self.business,
            'timestamp': datetime.now().isoformat(),
            'passed': passed,
            'quality_score': quality_score,
            'total_issues': len(self.issues),
            'issues_by_severity': {
                'critical': len(critical_issues),
                'high': len(high_issues),
                'medium': len(medium_issues),
                'low': len(low_issues)
            },
            'parser_ok': parser_ok,
            'issues': [
                {
                    'file': i.file_path,
                    'type': i.issue_type,
                    'description': i.description,
                    'severity': i.severity
                }
                for i in self.issues
            ]
        }
        
        return passed, report
    
    def generate_report(self, format: str = 'summary') -> str:
        """Generate quality assurance report"""
        passed, report = self.validate_all_phases()
        
        if format == 'json':
            return json.dumps(report, indent=2)
        
        # Generate summary report
        output = []
        output.append(f"{'='*60}")
        output.append(f"WORKFLOW QUALITY ASSURANCE REPORT")
        output.append(f"Business: {self.business}")
        output.append(f"{'='*60}")
        output.append("")
        
        status = "✅ PASSED" if passed else "❌ FAILED"
        output.append(f"Status: {status}")
        output.append(f"Quality Score: {report['quality_score']}/100")
        output.append(f"Total Issues: {report['total_issues']}")
        output.append("")
        
        if report['total_issues'] > 0:
            output.append("Issues by Severity:")
            for severity in ['critical', 'high', 'medium', 'low']:
                count = report['issues_by_severity'][severity]
                if count > 0:
                    output.append(f"  {severity.upper()}: {count}")
            output.append("")
            
            # Show critical and high issues
            critical_high = [i for i in report['issues'] if i['severity'] in ['critical', 'high']]
            if critical_high:
                output.append("Critical/High Priority Issues:")
                for issue in critical_high[:10]:  # Show first 10
                    output.append(f"  - [{issue['severity'].upper()}] {issue['file']}: {issue['description']}")
                if len(critical_high) > 10:
                    output.append(f"  ... and {len(critical_high) - 10} more")
        
        if passed:
            output.append("\n✅ Workflow output meets quality standards")
        else:
            output.append("\n❌ Workflow output has quality issues that need attention")
            output.append("\nRecommendations:")
            if not report['parser_ok']:
                output.append("  1. Fix parser to export all required variables")
            if report['issues_by_severity']['critical'] > 0:
                output.append("  2. Address critical issues immediately")
            if report['issues_by_severity']['high'] > 0:
                output.append("  3. Fix high priority issues before deployment")
        
        return '\n'.join(output)

def main():
    """CLI interface for workflow quality assurance"""
    parser = argparse.ArgumentParser(description='BMDP Workflow Quality Assurance')
    parser.add_argument('--business', required=True, 
                       choices=['grower', 'processor', 'distributor', 'marketplace'],
                       help='Business to validate')
    parser.add_argument('--format', choices=['summary', 'json'], default='summary',
                       help='Output format')
    parser.add_argument('--fix', action='store_true',
                       help='Attempt to fix issues (not implemented yet)')
    
    args = parser.parse_args()
    
    # Run quality assurance
    qa = WorkflowQualityAssurance(args.business)
    report = qa.generate_report(args.format)
    print(report)
    
    # Exit with appropriate code
    passed, _ = qa.validate_all_phases()
    exit(0 if passed else 1)

if __name__ == '__main__':
    main()
