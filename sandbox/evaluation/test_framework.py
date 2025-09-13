#!/usr/bin/env python3
"""
Test Framework for Template Solution Evaluation
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from jinja2 import Environment, FileSystemLoader, meta
import sys
import os

# Add project root to path
sys.path.append('/home/chris/bmdp')

class TemplateSolutionTester:
    """Test framework for evaluating template variable coverage solutions"""
    
    def __init__(self):
        self.sandbox_dir = Path('/home/chris/bmdp/sandbox')
        self.test_data_dir = self.sandbox_dir / 'test_data'
        self.test_results_dir = self.sandbox_dir / 'test_results'
        self.prototypes_dir = self.sandbox_dir / 'prototypes'
        
    def extract_template_variables(self, template_path: Path) -> set:
        """Extract all variables from a template"""
        env = Environment(loader=FileSystemLoader(template_path.parent))
        with open(template_path, 'r') as f:
            content = f.read()
        ast = env.parse(content)
        return meta.find_undeclared_variables(ast)
    
    def test_solution(self, solution_module, business_data: Dict, solution_name: str) -> Dict:
        """Test a solution module against the sample template"""
        start_time = time.time()
        
        # Load template and extract required variables
        template_path = self.test_data_dir / 'sample_template.j2'
        required_vars = self.extract_template_variables(template_path)
        
        # Generate variables using the solution
        try:
            generated_vars = solution_module.generate_variables(business_data, required_vars)
            generation_success = True
            error_message = None
        except Exception as e:
            generated_vars = {}
            generation_success = False
            error_message = str(e)
        
        # Calculate coverage
        coverage_count = len(required_vars.intersection(generated_vars.keys()))
        coverage_percentage = (coverage_count / len(required_vars)) * 100 if required_vars else 100
        
        # Render template with generated variables
        try:
            env = Environment(loader=FileSystemLoader(template_path.parent))
            template = env.get_template(template_path.name)
            rendered_content = template.render(**generated_vars)
            render_success = True
            render_error = None
        except Exception as e:
            rendered_content = ""
            render_success = False
            render_error = str(e)
        
        execution_time = time.time() - start_time
        
        # Calculate individual scores
        coverage_score = coverage_percentage
        quality_score = self.assess_content_quality(rendered_content) / 10  # Convert to 1-10 scale
        performance_score = min(10, max(1, 10 - (execution_time * 2)))  # Penalize slow execution
        maintainability_score = 10 if generation_success and render_success else 5
        
        # Calculate overall score
        overall_score = (
            coverage_score * 0.4 +  # 40% weight on coverage
            quality_score * 0.3 +   # 30% weight on quality  
            performance_score * 0.2 + # 20% weight on performance
            maintainability_score * 0.1  # 10% weight on maintainability
        )
        
        return {
            'solution_name': solution_name,
            'execution_time': execution_time,
            'generation_success': generation_success,
            'generation_error': error_message,
            'render_success': render_success,
            'render_error': render_error,
            'required_variables_count': len(required_vars),
            'generated_variables_count': len(generated_vars),
            'coverage_count': coverage_count,
            'coverage_percentage': coverage_percentage,
            'coverage_score': coverage_score,
            'quality_score': quality_score,
            'performance_score': performance_score,
            'maintainability_score': maintainability_score,
            'overall_score': overall_score,
            'missing_variables': list(required_vars - generated_vars.keys()),
            'extra_variables': list(generated_vars.keys() - required_vars),
            'rendered_content': rendered_content,
            'content_quality_score': self.assess_content_quality(rendered_content)
        }
    
    def assess_content_quality(self, content: str) -> float:
        """Assess the quality of rendered content (0-100 score)"""
        if not content:
            return 0.0
        
        score = 0.0
        
        # Check for TBD placeholders (lower quality)
        tbd_count = content.count('TBD')
        tbd_penalty = min(tbd_count * 5, 30)  # Max 30 point penalty
        
        # Check for realistic values (basic heuristics)
        realistic_score = 50  # Base score
        
        # Check for proper formatting
        formatting_score = 20 if len(content.split('\n')) > 5 else 10
        
        # Check for completeness (no undefined variables)
        completeness_score = 30 if '{{' not in content and '}}' not in content else 0
        
        score = realistic_score + formatting_score + completeness_score - tbd_penalty
        return max(0.0, min(100.0, score))
    
    def run_comparative_test(self, solutions: Dict[str, Any], template_path: Path, 
                           business_data: Dict) -> Dict[str, Any]:
        """Run comparative test across all solutions"""
        results = {}
        
        for solution_name, solution_module in solutions.items():
            results[solution_name] = self.test_solution(
                solution_name, solution_module, template_path, business_data
            )
        
        return results
    
    def calculate_overall_score(self, test_result: Dict[str, Any]) -> float:
        """Calculate overall effectiveness score (0-100)"""
        # Weighted scoring based on evaluation criteria
        coverage_weight = 0.4
        quality_weight = 0.3
        performance_weight = 0.2
        maintainability_weight = 0.1
        
        # Coverage score
        coverage_score = test_result['coverage_percentage']
        
        # Quality score
        quality_score = test_result['content_quality_score']
        
        # Performance score (inverse of execution time, normalized)
        exec_time = test_result['execution_time']
        performance_score = max(0, 100 - (exec_time * 10))  # Penalty for slow execution
        
        # Maintainability score (simplified - based on success rates)
        maintainability_score = 100 if test_result['generation_success'] and test_result['render_success'] else 50
        
        overall_score = (
            coverage_score * coverage_weight +
            quality_score * quality_weight +
            performance_score * performance_weight +
            maintainability_score * maintainability_weight
        )
        
        return overall_score
    
    def generate_test_report(self, results: Dict[str, Dict], output_path: Path):
        """Generate comprehensive test report"""
        report = {
            'test_summary': {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'solutions_tested': list(results.keys()),
                'template_tested': str(self.test_data_dir / 'sample_template.j2')
            },
            'detailed_results': {},
            'rankings': []
        }
        
        # Process detailed results and calculate scores
        for solution_name, result in results.items():
            overall_score = self.calculate_overall_score(result)
            result['overall_score'] = overall_score
            report['detailed_results'][solution_name] = result
            
            report['rankings'].append({
                'solution': solution_name,
                'overall_score': overall_score,
                'coverage_percentage': result['coverage_percentage'],
                'content_quality_score': result['content_quality_score'],
                'execution_time': result['execution_time']
            })
        
        # Sort rankings by overall score
        report['rankings'].sort(key=lambda x: x['overall_score'], reverse=True)
        
        # Save report
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report


def main():
    """Run the test framework"""
    tester = TemplateSolutionTester()
    
    # Sample business data
    business_data = {
        'business_slug': 'grower',
        'business_type': 'Agriculture',
        'industry_context': 'Papaya Cultivation',
        'capital_min': 750000,
        'capital_max': 2500000
    }
    
    print("Template Solution Testing Framework")
    print("=" * 50)
    print(f"Test template: {tester.test_data_dir / 'sample_template.j2'}")
    print(f"Required variables: {len(tester.extract_template_variables(tester.test_data_dir / 'sample_template.j2'))}")
    print()
    
    # Note: Solutions will be implemented as separate modules
    print("Ready to test solutions once prototypes are implemented.")
    print("Next steps:")
    print("1. Implement solution prototypes in sandbox/prototypes/")
    print("2. Run: python sandbox/evaluation/test_framework.py")


if __name__ == '__main__':
    main()
