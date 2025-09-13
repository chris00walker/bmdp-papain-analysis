#!/usr/bin/env python3
"""
Template-Parser Synchronization System - Ensures template variables match parser output
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import argparse
from jinja2 import Environment, FileSystemLoader, meta
import importlib.util


class TemplateSyncValidator:
    """Validate and synchronize template variables with parser output"""
    
    def __init__(self, project_root='/home/chris/bmdp'):
        self.project_root = Path(project_root)
        self.templates_dir = self.project_root / 'templates'
        self.parsers_dir = self.project_root / 'tools' / 'parsers'
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        
        # Quality thresholds for hybrid validation
        self.quality_thresholds = {
            'coverage_minimum': 95.0,  # Minimum variable coverage percentage
            'ai_variable_quality': 80.0,  # Minimum quality score for AI-generated variables
            'context_relevance': 85.0,  # Minimum context relevance score
            'business_alignment': 90.0  # Minimum business model alignment score
        }
        
    def extract_parser_variables(self, parser_path: Path) -> Set[str]:
        """Extract all variables exported by a parser"""
        try:
            # Read parser source code
            with open(parser_path, 'r') as f:
                source = f.read()
            
            # Parse AST to find export statements
            tree = ast.parse(source)
            exported_vars = set()
            
            # Look for export statements in export_environment_variables function
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # Look for env_vars.append(f'export VAR_NAME=...')
                    if (isinstance(node.func, ast.Attribute) and 
                        node.func.attr == 'append' and
                        node.args):
                        
                        arg = node.args[0]
                        if isinstance(arg, ast.JoinedStr):  # f-string
                            for value in arg.values:
                                if isinstance(value, ast.Constant) and value.value:
                                    # Extract variable name from export statement
                                    match = re.search(r'export\s+([A-Z_]+)=', value.value)
                                    if match:
                                        exported_vars.add(match.group(1))
            
            # Also look for direct string patterns in the source
            export_pattern = r'export\s+([A-Z_]+)='
            matches = re.findall(export_pattern, source)
            exported_vars.update(matches)
            
            return exported_vars
            
        except Exception as e:
            print(f"Error parsing {parser_path}: {e}")
            return set()
    
    def extract_template_variables(self, template_path: Path) -> Set[str]:
        """Extract all variables used in a template"""
        try:
            with open(template_path, 'r') as f:
                content = f.read()
            
            # Parse template to find variables
            ast = self.env.parse(content)
            variables = meta.find_undeclared_variables(ast)
            return variables
            
        except Exception as e:
            print(f"Error parsing template {template_path}: {e}")
            return set()
    
    def analyze_variable_coverage(self) -> Dict[str, Any]:
        """Analyze variable coverage across all templates and parsers"""
        # Get parser variables
        brief_parser_path = self.parsers_dir / 'brief_parser.py'
        parser_vars = self.extract_parser_variables(brief_parser_path)
        
        # Get template variables
        template_vars = {}
        all_template_vars = set()
        
        for template_file in self.templates_dir.rglob('*.j2'):
            vars_in_template = self.extract_template_variables(template_file)
            template_vars[str(template_file.relative_to(self.templates_dir))] = vars_in_template
            all_template_vars.update(vars_in_template)
        
        # Analyze coverage
        missing_from_parser = all_template_vars - parser_vars
        unused_in_templates = parser_vars - all_template_vars
        
        # Categorize missing variables
        categorized_missing = self._categorize_missing_variables(missing_from_parser)
        
        return {
            'parser_variables': sorted(parser_vars),
            'template_variables': dict(sorted(template_vars.items())),
            'all_template_variables': sorted(all_template_vars),
            'missing_from_parser': sorted(missing_from_parser),
            'unused_in_templates': sorted(unused_in_templates),
            'categorized_missing': categorized_missing,
            'coverage_stats': {
                'parser_vars_count': len(parser_vars),
                'template_vars_count': len(all_template_vars),
                'missing_count': len(missing_from_parser),
                'unused_count': len(unused_in_templates),
                'coverage_percentage': round((len(all_template_vars - missing_from_parser) / len(all_template_vars)) * 100, 2) if all_template_vars else 100
            }
        }
    
    def _categorize_missing_variables(self, missing_vars: Set[str]) -> Dict[str, List[str]]:
        """Categorize missing variables by type"""
        categories = {
            'dates': [],
            'budgets': [],
            'team': [],
            'risks': [],
            'phases': [],
            'project_meta': [],
            'business_model': [],
            'other': []
        }
        
        for var in missing_vars:
            var_lower = var.lower()
            if any(term in var_lower for term in ['date', 'time']):
                categories['dates'].append(var)
            elif any(term in var_lower for term in ['budget', 'cost', 'capital']):
                categories['budgets'].append(var)
            elif any(term in var_lower for term in ['team', 'lead', 'manager', 'analyst']):
                categories['team'].append(var)
            elif any(term in var_lower for term in ['risk', 'probability', 'impact']):
                categories['risks'].append(var)
            elif any(term in var_lower for term in ['phase', 'week', 'timeline']):
                categories['phases'].append(var)
            elif any(term in var_lower for term in ['project', 'sponsor', 'charter', 'scope']):
                categories['project_meta'].append(var)
            elif any(term in var_lower for term in ['value', 'customer', 'revenue', 'activity', 'resource']):
                categories['business_model'].append(var)
            else:
                categories['other'].append(var)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def generate_parser_extensions(self, missing_vars: Set[str]) -> str:
        """Generate code to extend parser with missing variables"""
        code_lines = []
        code_lines.append("# Additional environment variables to add to brief_parser.py")
        code_lines.append("# Add these to the export_environment_variables function:")
        code_lines.append("")
        
        categorized = self._categorize_missing_variables(missing_vars)
        
        for category, vars_list in categorized.items():
            if not vars_list:
                continue
                
            code_lines.append(f"    # {category.title()} variables")
            
            for var in vars_list:
                # Generate appropriate default values based on variable name
                default_value = self._generate_default_value(var)
                code_lines.append(f'    env_vars.append(f\'export {var}="{default_value}"\')')
            
            code_lines.append("")
        
        return '\n'.join(code_lines)
    
    def _generate_default_value(self, var_name: str) -> str:
        """Generate appropriate default value for a variable"""
        var_lower = var_name.lower()
        
        # Date variables
        if 'date' in var_lower:
            return '{current_date.strftime("%Y-%m-%d")}'
        
        # Numeric variables
        if any(term in var_lower for term in ['budget', 'cost', 'amount', 'weeks', 'days']):
            return '0'
        
        # Percentage variables
        if 'percent' in var_lower or 'pct' in var_lower:
            return '0'
        
        # Boolean-like variables
        if any(term in var_lower for term in ['complete', 'approved', 'valid']):
            return 'false'
        
        # Name/title variables
        if any(term in var_lower for term in ['name', 'title', 'lead', 'manager']):
            return 'TBD'
        
        # Default string value
        return 'TBD'
    
    def validate_template_parser_sync(self) -> Dict[str, Any]:
        """Validate synchronization between templates and parser"""
        analysis = self.analyze_variable_coverage()
        
        # Check for critical issues
        critical_issues = []
        warnings = []
        
        if analysis['missing_from_parser']:
            critical_issues.append(f"{len(analysis['missing_from_parser'])} variables used in templates but not provided by parser")
        
        if analysis['coverage_stats']['coverage_percentage'] < 80:
            critical_issues.append(f"Low variable coverage: {analysis['coverage_stats']['coverage_percentage']}%")
        
        if analysis['unused_in_templates']:
            warnings.append(f"{len(analysis['unused_in_templates'])} variables provided by parser but not used in templates")
        
        return {
            'analysis': analysis,
            'critical_issues': critical_issues,
            'warnings': warnings,
            'is_synchronized': len(critical_issues) == 0,
            'recommendations': self._generate_recommendations(analysis)
        }
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving synchronization"""
        recommendations = []
        
        if analysis['missing_from_parser']:
            recommendations.append("Extend brief_parser.py to export missing template variables")
        
        if analysis['coverage_stats']['coverage_percentage'] < 90:
            recommendations.append("Improve variable coverage to at least 90%")
        
        if len(analysis['unused_in_templates']) > 10:
            recommendations.append("Consider removing unused parser variables to reduce complexity")
        
        if analysis['categorized_missing'].get('other', []):
            recommendations.append("Review 'other' category variables for proper categorization")
        
        return recommendations
    
    def generate_sync_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate comprehensive synchronization report"""
        analysis = validation_results['analysis']
        report = []
        
        report.append("# Template-Parser Synchronization Report")
        report.append("")
        
        # Status
        status = "✅ SYNCHRONIZED" if validation_results['is_synchronized'] else "❌ NOT SYNCHRONIZED"
        report.append(f"## Status: {status}")
        report.append("")
        
        # Statistics
        stats = analysis['coverage_stats']
        report.append("## Coverage Statistics")
        report.append(f"- **Parser Variables**: {stats['parser_vars_count']}")
        report.append(f"- **Template Variables**: {stats['template_vars_count']}")
        report.append(f"- **Missing from Parser**: {stats['missing_count']}")
        report.append(f"- **Unused in Templates**: {stats['unused_count']}")
        report.append(f"- **Coverage Percentage**: {stats['coverage_percentage']}%")
        report.append("")
        
        # Critical Issues
        if validation_results['critical_issues']:
            report.append("## ❌ Critical Issues")
            for issue in validation_results['critical_issues']:
                report.append(f"- {issue}")
            report.append("")
        
        # Warnings
        if validation_results['warnings']:
            report.append("## ⚠️ Warnings")
            for warning in validation_results['warnings']:
                report.append(f"- {warning}")
            report.append("")
        
        # Missing Variables by Category
        if analysis['categorized_missing']:
            report.append("## Missing Variables by Category")
            for category, vars_list in analysis['categorized_missing'].items():
                report.append(f"### {category.title()}")
                for var in vars_list:
                    report.append(f"- `{var}`")
                report.append("")
        
        # Recommendations
        if validation_results['recommendations']:
            report.append("## Recommendations")
            for rec in validation_results['recommendations']:
                report.append(f"- {rec}")
            report.append("")
        
        # Templates with Missing Variables
        report.append("## Templates with Missing Variables")
        for template_name, template_vars in analysis['template_variables'].items():
            missing_in_template = template_vars - set(analysis['parser_variables'])
            if missing_in_template:
                report.append(f"### `{template_name}`")
                for var in sorted(missing_in_template):
                    report.append(f"- `{var}`")
                report.append("")
        
        return '\n'.join(report)
    def validate_hybrid_coverage(self, business_slug: str, template_path: Path) -> Dict[str, Any]:
        """Validate hybrid variable coverage and quality for a specific template and business"""
        try:
            # Import the hybrid parser functionality
            parser_module = importlib.import_module('tools.parsers.brief_parser')
            
            # Load business data - try different naming patterns
            brief_patterns = [
                f'brief-{business_slug}.md',
                f'brief-1-{business_slug}.md',
                f'brief-2-{business_slug}.md',
                f'brief-3-{business_slug}.md',
                f'brief-4-{business_slug}.md'
            ]
            
            brief_file = None
            for pattern in brief_patterns:
                candidate = self.project_root / pattern
                if candidate.exists():
                    brief_file = candidate
                    break
            
            if brief_file is None:
                return {'error': f'Business brief not found for {business_slug}. Tried: {brief_patterns}'}
            
            # Parse business data
            parser = parser_module.BusinessBriefParser()
            business_data = parser.parse_file(str(brief_file))
            
            # Extract template variables
            template_vars = self.extract_template_variables(template_path)
            
            # Generate base environment variables first
            base_vars_str = parser_module.export_environment_variables(business_data, business_slug)
            base_vars = {}
            for line in base_vars_str.split('\n'):
                if line.startswith('export ') and '=' in line:
                    var_def = line[7:]  # Remove 'export '
                    if '=' in var_def:
                        key, value = var_def.split('=', 1)
                        base_vars[key] = value.strip('"')
            
            # Generate hybrid variables
            hybrid_vars = parser_module.generate_missing_variables(business_data, template_vars, base_vars)
            
            # Evaluate quality metrics
            quality_metrics = self._evaluate_variable_quality(hybrid_vars, business_data, template_vars)
            
            # Calculate coverage
            base_vars = set(parser_module.export_environment_variables(business_data, business_slug).split('\n'))
            base_var_names = {line.split('=')[0].replace('export ', '') for line in base_vars if '=' in line}
            
            total_coverage = len(base_var_names.union(set(hybrid_vars.keys()))) / len(template_vars) * 100
            hybrid_coverage = len(hybrid_vars) / len(template_vars) * 100
            
            return {
                'business_slug': business_slug,
                'template_path': str(template_path.relative_to(self.project_root)),
                'total_variables': len(template_vars),
                'base_variables': len(base_var_names),
                'hybrid_variables': len(hybrid_vars),
                'total_coverage_pct': round(total_coverage, 2),
                'hybrid_coverage_pct': round(hybrid_coverage, 2),
                'quality_metrics': quality_metrics,
                'quality_passed': all(score >= threshold for score, threshold in zip(
                    quality_metrics['scores'].values(), 
                    [self.quality_thresholds['ai_variable_quality'], 
                     self.quality_thresholds['context_relevance'],
                     self.quality_thresholds['business_alignment']]
                )),
                'coverage_passed': total_coverage >= self.quality_thresholds['coverage_minimum']
            }
            
        except Exception as e:
            return {'error': f'Hybrid validation failed: {str(e)}'}
    
    def _evaluate_variable_quality(self, hybrid_vars: Dict[str, str], business_data: Dict[str, Any], template_vars: Set[str]) -> Dict[str, Any]:
        """Evaluate quality metrics for AI-generated variables"""
        
        # Extract business context
        business_type = business_data.get('sections', {}).get('business_type', 'Unknown')
        industry = business_data.get('sections', {}).get('industry', 'Unknown')
        
        quality_scores = {
            'content_quality': 0.0,
            'context_relevance': 0.0,
            'business_alignment': 0.0
        }
        
        if not hybrid_vars:
            return {'scores': quality_scores, 'details': {}}
        
        details = {}
        
        # Content Quality: Check for meaningful, non-placeholder values
        placeholder_count = 0
        for var, value in hybrid_vars.items():
            is_placeholder = any(term in str(value).lower() for term in ['tbd', 'todo', 'placeholder', 'xxx'])
            if is_placeholder:
                placeholder_count += 1
            details[var] = {
                'value': value,
                'is_placeholder': is_placeholder,
                'length': len(str(value))
            }
        
        quality_scores['content_quality'] = max(0, (len(hybrid_vars) - placeholder_count) / len(hybrid_vars) * 100)
        
        # Context Relevance: Check if variables match business context
        context_matches = 0
        for var, value in hybrid_vars.items():
            var_lower = var.lower()
            value_lower = str(value).lower()
            
            # Check if variable content relates to business type/industry
            business_terms = [business_type.lower(), industry.lower()]
            context_match = any(term in value_lower for term in business_terms if term != 'unknown')
            
            if context_match:
                context_matches += 1
                
            details[var]['context_relevant'] = context_match
        
        quality_scores['context_relevance'] = context_matches / len(hybrid_vars) * 100 if hybrid_vars else 0
        
        # Business Alignment: Check alignment with business model patterns
        alignment_score = 0
        business_keywords = []
        
        # Extract key business activities and segments
        if 'sections' in business_data:
            sections = business_data['sections']
            for key in ['key_activities', 'customer_segments', 'value_propositions']:
                if key in sections:
                    business_keywords.extend(str(sections[key]).lower().split())
        
        if business_keywords:
            for var, value in hybrid_vars.items():
                value_words = str(value).lower().split()
                keyword_matches = sum(1 for word in value_words if word in business_keywords)
                alignment_score += min(keyword_matches / len(value_words), 1.0) if value_words else 0
                
            quality_scores['business_alignment'] = alignment_score / len(hybrid_vars) * 100
        else:
            quality_scores['business_alignment'] = 50.0  # Neutral score when no keywords available
        
        return {
            'scores': quality_scores,
            'details': details,
            'business_context': {
                'business_type': business_type,
                'industry': industry,
                'keywords_found': len(business_keywords)
            }
        }
    
    def generate_hybrid_validation_report(self, business_slug: str, template_paths: List[Path] = None) -> str:
        """Generate comprehensive hybrid validation report for business templates"""
        
        if template_paths is None:
            # Default to all deliverable templates
            template_paths = list((self.templates_dir / 'deliverables').rglob('*.j2'))
        
        report = []
        report.append(f"# Hybrid Variable Validation Report - {business_slug.title()}")
        report.append("")
        report.append(f"**Generated**: {Path(__file__).name} at {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Overall statistics
        total_templates = len(template_paths)
        passed_coverage = 0
        passed_quality = 0
        total_variables = 0
        total_hybrid_variables = 0
        
        validation_results = []
        
        for template_path in template_paths:
            result = self.validate_hybrid_coverage(business_slug, template_path)
            if 'error' not in result:
                validation_results.append(result)
                total_variables += result['total_variables']
                total_hybrid_variables += result['hybrid_variables']
                if result['coverage_passed']:
                    passed_coverage += 1
                if result['quality_passed']:
                    passed_quality += 1
        
        # Summary statistics
        report.append("## Summary Statistics")
        report.append(f"- **Templates Validated**: {len(validation_results)}/{total_templates}")
        report.append(f"- **Total Variables**: {total_variables}")
        report.append(f"- **AI-Generated Variables**: {total_hybrid_variables}")
        
        if len(validation_results) > 0:
            coverage_rate = passed_coverage/len(validation_results)*100
            quality_rate = passed_quality/len(validation_results)*100
            report.append(f"- **Coverage Pass Rate**: {passed_coverage}/{len(validation_results)} ({coverage_rate:.1f}%)")
            report.append(f"- **Quality Pass Rate**: {passed_quality}/{len(validation_results)} ({quality_rate:.1f}%)")
        else:
            report.append("- **Coverage Pass Rate**: No templates validated")
            report.append("- **Quality Pass Rate**: No templates validated")
        
        report.append("")
        
        # Quality thresholds
        report.append("## Quality Thresholds")
        for metric, threshold in self.quality_thresholds.items():
            report.append(f"- **{metric.replace('_', ' ').title()}**: {threshold}%")
        report.append("")
        
        # Detailed results
        report.append("## Template Validation Results")
        for result in validation_results:
            status_coverage = "✅" if result['coverage_passed'] else "❌"
            status_quality = "✅" if result['quality_passed'] else "❌"
            
            report.append(f"### {result['template_path']}")
            report.append(f"- **Coverage**: {status_coverage} {result['total_coverage_pct']}% ({result['total_variables']} variables)")
            report.append(f"- **Hybrid Variables**: {result['hybrid_variables']} ({result['hybrid_coverage_pct']}%)")
            report.append(f"- **Quality**: {status_quality}")
            
            # Quality metrics breakdown
            if 'quality_metrics' in result and 'scores' in result['quality_metrics']:
                scores = result['quality_metrics']['scores']
                report.append(f"  - Content Quality: {scores['content_quality']:.1f}%")
                report.append(f"  - Context Relevance: {scores['context_relevance']:.1f}%")
                report.append(f"  - Business Alignment: {scores['business_alignment']:.1f}%")
            
            report.append("")
        
        return '\n'.join(report)


def main():
    """Command-line interface for template synchronization validator"""
    parser = argparse.ArgumentParser(description='Validate template-parser synchronization and hybrid coverage')
    parser.add_argument('--report-file', help='Output report file path')
    parser.add_argument('--generate-extensions', help='Generate parser extension code file')
    parser.add_argument('--project-root', default='/home/chris/bmdp', help='Project root directory')
    
    # Hybrid validation options
    parser.add_argument('--hybrid-validation', action='store_true', help='Run hybrid variable validation')
    parser.add_argument('--business-slug', help='Business slug for hybrid validation (e.g., grower)')
    parser.add_argument('--template-path', help='Specific template path for validation')
    parser.add_argument('--hybrid-report-file', help='Output file for hybrid validation report')
    
    args = parser.parse_args()
    
    validator = TemplateSyncValidator(args.project_root)
    
    if args.hybrid_validation:
        if not args.business_slug:
            print("Error: --business-slug required for hybrid validation")
            return
        
        # Generate hybrid validation report
        template_paths = None
        if args.template_path:
            template_paths = [Path(args.template_path)]
        
        hybrid_report = validator.generate_hybrid_validation_report(args.business_slug, template_paths)
        
        if args.hybrid_report_file:
            with open(args.hybrid_report_file, 'w') as f:
                f.write(hybrid_report)
            print(f"Hybrid validation report saved to: {args.hybrid_report_file}")
        else:
            print(hybrid_report)
    
    else:
        # Standard template-parser synchronization validation
        validation_results = validator.validate_template_parser_sync()
        
        # Generate report
        report = validator.generate_sync_report(validation_results)
        
        if args.report_file:
            with open(args.report_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {args.report_file}")
        else:
            print(report)
        
        # Generate parser extensions
        if args.generate_extensions:
            missing_vars = set(validation_results['analysis']['missing_from_parser'])
            extensions = validator.generate_parser_extensions(missing_vars)
            
            with open(args.generate_extensions, 'w') as f:
                f.write(extensions)
            print(f"Parser extensions saved to: {args.generate_extensions}")


if __name__ == '__main__':
    main()
