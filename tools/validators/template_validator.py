#!/usr/bin/env python3
"""
Template validation tool to identify missing variables and format issues.
"""

import os
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, meta, UndefinedError
import json
import yaml

class TemplateValidator:
    """Validate templates for missing variables and format consistency"""
    
    def __init__(self, templates_dir='/home/chris/bmdp/templates'):
        self.templates_dir = Path(templates_dir)
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
    def extract_template_variables(self, template_path):
        """Extract all variables used in a template"""
        try:
            with open(template_path, 'r') as f:
                content = f.read()
            
            # Parse template to find variables
            ast = self.env.parse(content)
            variables = meta.find_undeclared_variables(ast)
            return variables, None
        except Exception as e:
            return set(), str(e)
    
    def validate_json_templates(self):
        """Validate JSON templates don't have YAML frontmatter"""
        issues = []
        
        for json_template in self.templates_dir.rglob('*.json.j2'):
            with open(json_template, 'r') as f:
                content = f.read()
            
            if content.strip().startswith('---'):
                issues.append({
                    'file': str(json_template),
                    'issue': 'JSON template contains YAML frontmatter',
                    'severity': 'error'
                })
        
        return issues
    
    def check_variable_coverage(self, available_vars):
        """Check which templates use undefined variables"""
        issues = []
        
        for template_file in self.templates_dir.rglob('*.j2'):
            variables, error = self.extract_template_variables(template_file)
            
            if error:
                issues.append({
                    'file': str(template_file),
                    'issue': f'Template parsing error: {error}',
                    'severity': 'error'
                })
                continue
            
            undefined_vars = variables - available_vars
            if undefined_vars:
                issues.append({
                    'file': str(template_file),
                    'issue': f'Undefined variables: {", ".join(undefined_vars)}',
                    'severity': 'error',
                    'undefined_vars': list(undefined_vars)
                })
        
        return issues
    
    def validate_all(self, available_vars=None):
        """Run all validation checks"""
        if available_vars is None:
            # Default set of available variables from brief_parser.py
            available_vars = {
                'BUSINESS_SLUG', 'BUSINESS_TITLE', 'BUSINESS_NUMBER', 'BUSINESS_TYPE',
                'INDUSTRY_CONTEXT', 'DEFAULT_BUSINESS_LEAD', 'DEFAULT_PM',
                'CAPITAL_MIN', 'CAPITAL_MAX', 'HORIZON_YEARS', 'DISCOUNT_RATE',
                'CUSTOMER_SEGMENTS', 'VALUE_PROPOSITION', 'KEY_ACTIVITIES',
                'KEY_RESOURCES', 'REVENUE_STREAMS', 'CRITICAL_RISKS'
            }
        
        all_issues = []
        
        # Check JSON template format issues
        all_issues.extend(self.validate_json_templates())
        
        # Check variable coverage
        all_issues.extend(self.check_variable_coverage(available_vars))
        
        return all_issues

def main():
    validator = TemplateValidator()
    issues = validator.validate_all()
    
    if not issues:
        print("✅ All templates validated successfully")
        return
    
    print(f"❌ Found {len(issues)} template issues:")
    
    for issue in issues:
        severity_icon = "🔴" if issue['severity'] == 'error' else "🟡"
        print(f"{severity_icon} {issue['file']}")
        print(f"   Issue: {issue['issue']}")
        if 'undefined_vars' in issue:
            print(f"   Missing: {', '.join(issue['undefined_vars'])}")
        print()

if __name__ == '__main__':
    main()
