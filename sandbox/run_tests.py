#!/usr/bin/env python3
"""
Test runner for comparing all three template solution prototypes
"""

import sys
import os
sys.path.append('/home/chris/bmdp')
sys.path.append('/home/chris/bmdp/sandbox')

from evaluation.test_framework import TemplateSolutionTester
from prototypes.hybrid_parser_llm import HybridParserLLM
from prototypes.adaptive_template_renderer import AdaptiveTemplateRenderer
from prototypes.dynamic_variable_generator import DynamicVariableGenerator

def main():
    """Run comparative tests on all three solutions"""
    
    # Initialize tester
    tester = TemplateSolutionTester()
    
    # Test business data (using grower business as example)
    business_data = {
        'business_type': 'Agricultural Processing',
        'industry_context': 'Sustainable Agriculture',
        'capital_min': 750000,
        'capital_max': 2500000,
        'business_slug': 'grower',
        'sections': {
            'title': 'Grower Agricultural Processing Business',
            'overview': 'Sustainable agricultural processing and distribution'
        }
    }
    
    print("BMDP Template Solution Comparison Test")
    print("=" * 50)
    print(f"Business: {business_data['business_type']}")
    print(f"Industry: {business_data['industry_context']}")
    print(f"Capital Range: ${business_data['capital_min']:,} - ${business_data['capital_max']:,}")
    print()
    
    # Test Solution 1: Hybrid Parser-LLM Pipeline
    print("Testing Solution 1: Hybrid Parser-LLM Pipeline")
    print("-" * 45)
    solution1 = HybridParserLLM()
    results1 = tester.test_solution(solution1, business_data, "Hybrid Parser-LLM")
    print()
    
    # Test Solution 2: Adaptive Template Rendering
    print("Testing Solution 2: Adaptive Template Rendering")
    print("-" * 45)
    solution2 = AdaptiveTemplateRenderer()
    results2 = tester.test_solution(solution2, business_data, "Adaptive Template Renderer")
    print()
    
    # Test Solution 3: Dynamic Variable Generation
    print("Testing Solution 3: Dynamic Variable Generation")
    print("-" * 45)
    solution3 = DynamicVariableGenerator()
    results3 = tester.test_solution(solution3, business_data, "Dynamic Variable Generator")
    print()
    
    # Compare results
    print("COMPARATIVE ANALYSIS")
    print("=" * 50)
    
    all_results = [
        ("Hybrid Parser-LLM", results1),
        ("Adaptive Template Renderer", results2), 
        ("Dynamic Variable Generator", results3)
    ]
    
    # Sort by overall score
    all_results.sort(key=lambda x: x[1]['overall_score'], reverse=True)
    
    print("RANKING BY OVERALL SCORE:")
    for i, (name, results) in enumerate(all_results, 1):
        print(f"{i}. {name}: {results['overall_score']:.1f}/100")
        print(f"   Coverage: {results['coverage_score']:.1f}% | Quality: {results['quality_score']:.1f}/10")
        print(f"   Performance: {results['performance_score']:.1f}/10 | Maintainability: {results['maintainability_score']:.1f}/10")
        print()
    
    # Detailed comparison
    print("DETAILED COMPARISON:")
    print("-" * 20)
    
    metrics = ['coverage_score', 'quality_score', 'performance_score', 'maintainability_score']
    metric_names = ['Coverage (%)', 'Quality (1-10)', 'Performance (1-10)', 'Maintainability (1-10)']
    
    for metric, name in zip(metrics, metric_names):
        print(f"{name}:")
        metric_results = [(sol_name, results[metric]) for sol_name, results in all_results]
        metric_results.sort(key=lambda x: x[1], reverse=True)
        
        for sol_name, score in metric_results:
            print(f"  {sol_name}: {score:.1f}")
        print()
    
    # Winner and recommendation
    winner_name, winner_results = all_results[0]
    print("RECOMMENDATION:")
    print("-" * 15)
    print(f"Winner: {winner_name}")
    print(f"Overall Score: {winner_results['overall_score']:.1f}/100")
    print()
    print("RATIONALE:")
    
    if winner_results['coverage_score'] >= 90:
        print("✓ Excellent variable coverage (90%+)")
    elif winner_results['coverage_score'] >= 80:
        print("✓ Good variable coverage (80%+)")
    else:
        print("⚠ Variable coverage needs improvement")
        
    if winner_results['quality_score'] >= 8:
        print("✓ High-quality variable generation")
    elif winner_results['quality_score'] >= 6:
        print("✓ Acceptable variable quality")
    else:
        print("⚠ Variable quality needs improvement")
        
    if winner_results['performance_score'] >= 8:
        print("✓ Excellent performance characteristics")
    elif winner_results['performance_score'] >= 6:
        print("✓ Acceptable performance")
    else:
        print("⚠ Performance optimization needed")
        
    if winner_results['maintainability_score'] >= 8:
        print("✓ Highly maintainable architecture")
    elif winner_results['maintainability_score'] >= 6:
        print("✓ Reasonably maintainable")
    else:
        print("⚠ Maintainability concerns")
    
    print()
    print("NEXT STEPS:")
    print("1. Implement the winning solution in production")
    print("2. Extend enhanced parser with winning approach")
    print("3. Test with all BMDP phases (0-3)")
    print("4. Integrate with existing workflow automation")

if __name__ == "__main__":
    main()
