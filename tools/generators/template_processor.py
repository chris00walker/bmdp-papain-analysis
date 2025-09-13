#!/usr/bin/env python3
"""
Template Format Processor - Standardizes template formats and removes inconsistencies
Enhanced with hybrid variable support for seamless integration
"""

import os
import re
import json
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set
import argparse
from jinja2 import Environment, FileSystemLoader, meta

# Add project root to path for imports
sys.path.append('/home/chris/bmdp')


class TemplateProcessor:
    """Process and standardize template formats"""
    
    def __init__(self, templates_dir='/home/chris/bmdp/templates'):
        self.templates_dir = Path(templates_dir)
        
    def remove_yaml_frontmatter_from_json(self, template_path: Path) -> Tuple[bool, str]:
        """Remove YAML frontmatter from JSON templates"""
        try:
            with open(template_path, 'r') as f:
                content = f.read()
            
            # Check if JSON template has YAML frontmatter
            if not content.strip().startswith('---'):
                return False, "No YAML frontmatter found"
            
            # Split frontmatter and content
            parts = content.split('---', 2)
            if len(parts) < 3:
                return False, "Invalid YAML frontmatter format"
            
            # Extract JSON content (skip frontmatter)
            json_content = parts[2].strip()
            
            # Validate JSON format
            try:
                json.loads(json_content)
            except json.JSONDecodeError as e:
                return False, f"Invalid JSON content: {e}"
            
            # Write cleaned content back
            with open(template_path, 'w') as f:
                f.write(json_content)
            
            return True, "YAML frontmatter removed successfully"
            
        except Exception as e:
            return False, f"Error processing template: {e}"
    
    def validate_template_format(self, template_path: Path) -> Tuple[bool, str]:
        """Validate template format consistency"""
        try:
            with open(template_path, 'r') as f:
                content = f.read()
            
            # Check file extension matches content
            if template_path.suffix == '.json.j2':
                # Should be valid JSON after Jinja processing
                # Check for common JSON structure indicators
                if not ('{' in content and '}' in content):
                    return False, "JSON template missing JSON structure"
                    
            elif template_path.suffix == '.csv.j2':
                # Should have CSV structure
                lines = content.strip().split('\n')
                if len(lines) < 2:
                    return False, "CSV template should have header and data rows"
                    
            elif template_path.suffix == '.md.j2':
                # Should have markdown structure
                if not content.strip():
                    return False, "Markdown template is empty"
            
            return True, "Template format is valid"
            
        except Exception as e:
            return False, f"Error validating template: {e}"
    
    def standardize_variable_syntax(self, template_path: Path) -> Tuple[bool, str]:
        """Standardize Jinja2 variable syntax"""
        try:
            with open(template_path, 'r') as f:
                content = f.read()
            
            original_content = content
            
            # Standardize variable syntax patterns
            # Fix common spacing issues in Jinja variables
            content = re.sub(r'\{\{\s*([^}]+?)\s*\}\}', r'{{ \1 }}', content)
            
            # Fix common spacing issues in Jinja statements
            content = re.sub(r'\{\%\s*([^%]+?)\s*\%\}', r'{% \1 %}', content)
            
            # Ensure consistent variable naming (no changes to actual names)
            # This is just formatting consistency
            
            if content != original_content:
                with open(template_path, 'w') as f:
                    f.write(content)
                return True, "Variable syntax standardized"
            else:
                return False, "No syntax changes needed"
                
        except Exception as e:
            return False, f"Error standardizing syntax: {e}"
    
    def process_all_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """Process all templates in the directory"""
        results = {
            'json_frontmatter_removed': [],
            'format_validated': [],
            'syntax_standardized': [],
            'errors': []
        }
        
        for template_file in self.templates_dir.rglob('*.j2'):
            try:
                # Remove YAML frontmatter from JSON templates
                if template_file.suffix == '.j2' and '.json' in template_file.name:
                    success, message = self.remove_yaml_frontmatter_from_json(template_file)
                    if success:
                        results['json_frontmatter_removed'].append({
                            'file': str(template_file),
                            'message': message
                        })
                    elif "No YAML frontmatter found" not in message:
                        results['errors'].append({
                            'file': str(template_file),
                            'error': message,
                            'operation': 'frontmatter_removal'
                        })
                
                # Validate template format
                success, message = self.validate_template_format(template_file)
                if success:
                    results['format_validated'].append({
                        'file': str(template_file),
                        'message': message
                    })
                else:
                    results['errors'].append({
                        'file': str(template_file),
                        'error': message,
                        'operation': 'format_validation'
                    })
                
                # Standardize variable syntax
                success, message = self.standardize_variable_syntax(template_file)
                if success:
                    results['syntax_standardized'].append({
                        'file': str(template_file),
                        'message': message
                    })
                elif "No syntax changes needed" not in message:
                    results['errors'].append({
                        'file': str(template_file),
                        'error': message,
                        'operation': 'syntax_standardization'
                    })
                    
            except Exception as e:
                results['errors'].append({
                    'file': str(template_file),
                    'error': str(e),
                    'operation': 'general_processing'
                })
        
        return results
    
    def generate_report(self, results: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate processing report"""
        report = []
        report.append("# Template Processing Report")
        report.append("")
        
        # Summary
        total_processed = (len(results['json_frontmatter_removed']) + 
                          len(results['format_validated']) + 
                          len(results['syntax_standardized']))
        total_errors = len(results['errors'])
        
        report.append(f"## Summary")
        report.append(f"- **Templates Processed**: {total_processed}")
        report.append(f"- **Errors**: {total_errors}")
        report.append("")
        
        # JSON Frontmatter Removal
        if results['json_frontmatter_removed']:
            report.append("## JSON Frontmatter Removed")
            for item in results['json_frontmatter_removed']:
                report.append(f"- `{item['file']}`: {item['message']}")
            report.append("")
        
        # Format Validation
        if results['format_validated']:
            report.append("## Format Validation")
            report.append(f"✅ {len(results['format_validated'])} templates validated successfully")
            report.append("")
        
        # Syntax Standardization
        if results['syntax_standardized']:
            report.append("## Syntax Standardized")
            for item in results['syntax_standardized']:
                report.append(f"- `{item['file']}`: {item['message']}")
            report.append("")
        
        # Errors
        if results['errors']:
            report.append("## Errors")
            for item in results['errors']:
                report.append(f"- `{item['file']}`: {item['message']}")
            report.append("")
        
        return '\n'.join(report)
    
    def extract_template_variables(self, template_path: Path) -> Set[str]:
        """Extract all variables from a template"""
        env = Environment(loader=FileSystemLoader(template_path.parent))
        with open(template_path, 'r') as f:
            content = f.read()
        ast = env.parse(content)
        return meta.find_undeclared_variables(ast)
    
    def render_template_with_hybrid_variables(self, template_path: Path, business_data: Dict[str, Any], 
                                            business_slug: str) -> Tuple[str, Dict[str, Any]]:
        """Render template using hybrid variable generation"""
        # Import hybrid parser functions
        import sys
        sys.path.append('/home/chris/bmdp')
        try:
            from tools.parsers.parse_business_brief import parse_file, generate_missing_variables_with_hybrid
        except ImportError as e:
            print(f"Error importing hybrid parser: {e}")
            return "", {}
        
        # Extract required variables from template
        required_vars = self.extract_template_variables(template_path)
        
        # Generate hybrid variables (base + missing)
        env_vars_str = generate_missing_variables_with_hybrid(business_data, business_slug, required_vars)
        
        # Parse environment variables into dict
        env_vars = {}
        for line in env_vars_str.split('\n'):
            if line.startswith('export ') and '=' in line:
                var_name = line.split('export ')[1].split('=')[0]
                var_value = line.split('=', 1)[1].strip('"')
                env_vars[var_name] = var_value
        
        # Render template
        env = Environment(loader=FileSystemLoader(template_path.parent))
        template = env.get_template(template_path.name)
        rendered_content = template.render(**env_vars)
        
        # Return rendered content and variable coverage info
        coverage_info = {
            'required_variables': len(required_vars),
            'provided_variables': len(env_vars),
            'coverage_percentage': (len(required_vars.intersection(env_vars.keys())) / len(required_vars)) * 100 if required_vars else 100,
            'missing_variables': list(required_vars - env_vars.keys()),
            'extra_variables': list(env_vars.keys() - required_vars)
        }
        
        return rendered_content, coverage_info


def main():
    """Command-line interface for template processor"""
    parser = argparse.ArgumentParser(description='Process and standardize template formats with hybrid variable support')
    parser.add_argument('--templates-dir', default='/home/chris/bmdp/templates', 
                       help='Directory containing templates')
    parser.add_argument('--report-file', help='Output file for processing report')
    parser.add_argument('--test-hybrid', help='Test hybrid rendering with business slug')
    parser.add_argument('--template-file', help='Specific template file to test')
    
    args = parser.parse_args()
    
    processor = TemplateProcessor(args.templates_dir)
    
    if args.test_hybrid and args.template_file:
        # Test hybrid variable generation
        template_path = Path(args.template_file)
        
        # Sample business data for testing
        business_data = {
            'business_type': 'Agricultural Processing',
            'industry_context': 'Sustainable Agriculture',
            'capital_min': 750000,
            'capital_max': 2500000,
            'sections': {
                'title': f'{args.test_hybrid.title()} Agricultural Processing Business'
            }
        }
        
        try:
            rendered_content, coverage_info = processor.render_template_with_hybrid_variables(
                template_path, business_data, args.test_hybrid
            )
            
            print(f"Hybrid Template Rendering Test")
            print(f"=" * 40)
            print(f"Template: {template_path}")
            print(f"Business: {args.test_hybrid}")
            print(f"Required Variables: {coverage_info['required_variables']}")
            print(f"Provided Variables: {coverage_info['provided_variables']}")
            print(f"Coverage: {coverage_info['coverage_percentage']:.1f}%")
            
            if coverage_info['missing_variables']:
                print(f"Missing Variables: {coverage_info['missing_variables']}")
            
            print(f"\nRendered Content Preview:")
            print("-" * 40)
            print(rendered_content[:500] + "..." if len(rendered_content) > 500 else rendered_content)
            
        except Exception as e:
            print(f"Error testing hybrid rendering: {e}")
    
    else:
        # Standard template processing
        results = processor.process_all_templates()
        report = processor.generate_report(results)
        
        if args.report_file:
            with open(args.report_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {args.report_file}")
        else:
            print(report)


if __name__ == '__main__':
    main()
