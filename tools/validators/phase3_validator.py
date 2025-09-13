#!/usr/bin/env python3
"""
Phase 3 BMDP Coverage Validator - Comprehensive testing across all BMDP phases and templates
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.validators.template_sync import TemplateSyncValidator


class Phase3Validator:
    """Comprehensive validator for Phase 3 BMDP coverage testing"""
    
    def __init__(self, project_root='/home/chris/bmdp'):
        self.project_root = Path(project_root)
        self.templates_dir = self.project_root / 'templates' / 'deliverables'
        self.sync_validator = TemplateSyncValidator(project_root)
        
        # Performance tracking
        self.performance_metrics = {
            'start_time': None,
            'end_time': None,
            'template_processing_times': {},
            'total_templates': 0,
            'successful_validations': 0,
            'failed_validations': 0,
            'total_variables': 0,
            'hybrid_variables_generated': 0,
            'average_quality_score': 0.0
        }
        
        # Phase organization
        self.phase_templates = {
            'phase_0': [],
            'phase_1': [],
            'phase_2': [],
            'phase_3': [],
            'other': []
        }
        
    def organize_templates_by_phase(self) -> Dict[str, List[Path]]:
        """Organize all templates by BMDP phase"""
        
        all_templates = list(self.templates_dir.rglob('*.j2'))
        
        for template_path in all_templates:
            relative_path = str(template_path.relative_to(self.templates_dir))
            
            # Categorize by phase based on directory structure and naming
            if any(phase in relative_path for phase in ['00_initiation', '0_initiation']):
                self.phase_templates['phase_0'].append(template_path)
            elif any(phase in relative_path for phase in ['10_mobilize', '1_mobilize']):
                self.phase_templates['phase_1'].append(template_path)
            elif any(phase in relative_path for phase in ['20_understand', '2_understand']):
                self.phase_templates['phase_2'].append(template_path)
            elif any(phase in relative_path for phase in ['30_design', '3_design']):
                self.phase_templates['phase_3'].append(template_path)
            else:
                # Check for numeric prefixes
                if relative_path.startswith(('0', '1', '2', '3')):
                    phase_num = int(relative_path[0])
                    if phase_num <= 3:
                        self.phase_templates[f'phase_{phase_num}'].append(template_path)
                    else:
                        self.phase_templates['other'].append(template_path)
                else:
                    self.phase_templates['other'].append(template_path)
        
        return self.phase_templates
    
    def validate_single_template(self, business_slug: str, template_path: Path) -> Dict[str, Any]:
        """Validate a single template with performance tracking"""
        
        start_time = time.time()
        
        try:
            # Run hybrid validation
            result = self.sync_validator.validate_hybrid_coverage(business_slug, template_path)
            
            processing_time = time.time() - start_time
            self.performance_metrics['template_processing_times'][str(template_path)] = processing_time
            
            if 'error' not in result:
                self.performance_metrics['successful_validations'] += 1
                self.performance_metrics['total_variables'] += result.get('total_variables', 0)
                self.performance_metrics['hybrid_variables_generated'] += result.get('hybrid_variables', 0)
                
                # Calculate quality score
                if 'quality_metrics' in result and 'scores' in result['quality_metrics']:
                    scores = result['quality_metrics']['scores']
                    avg_score = sum(scores.values()) / len(scores) if scores else 0
                    result['average_quality_score'] = avg_score
                
            else:
                self.performance_metrics['failed_validations'] += 1
                result['processing_time'] = processing_time
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.performance_metrics['failed_validations'] += 1
            return {
                'error': f'Validation failed: {str(e)}',
                'template_path': str(template_path.relative_to(self.project_root)),
                'processing_time': processing_time
            }
    
    def run_comprehensive_validation(self, business_slugs: List[str], max_workers: int = 4) -> Dict[str, Any]:
        """Run comprehensive validation across all phases and businesses"""
        
        self.performance_metrics['start_time'] = time.time()
        
        # Organize templates by phase
        phase_templates = self.organize_templates_by_phase()
        
        # Results structure
        results = {
            'summary': {},
            'phase_results': {},
            'business_results': {},
            'performance_metrics': {},
            'failed_validations': []
        }
        
        total_validations = 0
        
        # Process each phase
        for phase_name, templates in phase_templates.items():
            if not templates:
                continue
                
            print(f"Processing {phase_name}: {len(templates)} templates")
            phase_results = {}
            
            for business_slug in business_slugs:
                business_results = []
                
                # Use ThreadPoolExecutor for parallel processing
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # Submit validation tasks
                    future_to_template = {
                        executor.submit(self.validate_single_template, business_slug, template): template
                        for template in templates
                    }
                    
                    # Collect results
                    for future in as_completed(future_to_template):
                        template = future_to_template[future]
                        try:
                            result = future.result()
                            business_results.append(result)
                            total_validations += 1
                            
                            if 'error' in result:
                                results['failed_validations'].append({
                                    'business': business_slug,
                                    'phase': phase_name,
                                    'template': str(template.relative_to(self.project_root)),
                                    'error': result['error']
                                })
                                
                        except Exception as e:
                            results['failed_validations'].append({
                                'business': business_slug,
                                'phase': phase_name,
                                'template': str(template.relative_to(self.project_root)),
                                'error': f'Future execution failed: {str(e)}'
                            })
                
                phase_results[business_slug] = business_results
                
                # Store business-level results
                if business_slug not in results['business_results']:
                    results['business_results'][business_slug] = {}
                results['business_results'][business_slug][phase_name] = business_results
            
            results['phase_results'][phase_name] = phase_results
        
        # Finalize performance metrics
        self.performance_metrics['end_time'] = time.time()
        self.performance_metrics['total_duration'] = self.performance_metrics['end_time'] - self.performance_metrics['start_time']
        self.performance_metrics['total_templates'] = sum(len(templates) for templates in phase_templates.values())
        self.performance_metrics['total_validations'] = total_validations
        
        # Calculate average quality score
        quality_scores = []
        for phase_results in results['phase_results'].values():
            for business_results in phase_results.values():
                for result in business_results:
                    if 'average_quality_score' in result:
                        quality_scores.append(result['average_quality_score'])
        
        self.performance_metrics['average_quality_score'] = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        results['performance_metrics'] = self.performance_metrics
        
        # Generate summary
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive summary of validation results"""
        
        metrics = results['performance_metrics']
        
        # Calculate success rates by phase
        phase_success_rates = {}
        for phase_name, phase_results in results['phase_results'].items():
            total_validations = 0
            successful_validations = 0
            
            for business_results in phase_results.values():
                for result in business_results:
                    total_validations += 1
                    if 'error' not in result:
                        successful_validations += 1
            
            phase_success_rates[phase_name] = {
                'total': total_validations,
                'successful': successful_validations,
                'success_rate': (successful_validations / total_validations * 100) if total_validations > 0 else 0
            }
        
        # Calculate business success rates
        business_success_rates = {}
        for business_slug, business_phases in results['business_results'].items():
            total_validations = 0
            successful_validations = 0
            
            for phase_results in business_phases.values():
                for result in phase_results:
                    total_validations += 1
                    if 'error' not in result:
                        successful_validations += 1
            
            business_success_rates[business_slug] = {
                'total': total_validations,
                'successful': successful_validations,
                'success_rate': (successful_validations / total_validations * 100) if total_validations > 0 else 0
            }
        
        return {
            'total_templates': metrics['total_templates'],
            'total_validations': metrics['total_validations'],
            'successful_validations': metrics['successful_validations'],
            'failed_validations': metrics['failed_validations'],
            'overall_success_rate': (metrics['successful_validations'] / metrics['total_validations'] * 100) if metrics['total_validations'] > 0 else 0,
            'total_duration_seconds': metrics['total_duration'],
            'average_processing_time': metrics['total_duration'] / metrics['total_validations'] if metrics['total_validations'] > 0 else 0,
            'total_variables': metrics['total_variables'],
            'hybrid_variables_generated': metrics['hybrid_variables_generated'],
            'hybrid_generation_rate': (metrics['hybrid_variables_generated'] / metrics['total_variables'] * 100) if metrics['total_variables'] > 0 else 0,
            'average_quality_score': metrics['average_quality_score'],
            'phase_success_rates': phase_success_rates,
            'business_success_rates': business_success_rates
        }
    
    def generate_comprehensive_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive Phase 3 validation report"""
        
        report = []
        summary = results['summary']
        
        report.append("# Phase 3: Full BMDP Coverage Validation Report")
        report.append("")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Validation Duration**: {summary['total_duration_seconds']:.2f} seconds")
        report.append("")
        
        # Executive Summary
        report.append("## Executive Summary")
        report.append(f"- **Total Templates**: {summary['total_templates']}")
        report.append(f"- **Total Validations**: {summary['total_validations']}")
        report.append(f"- **Success Rate**: {summary['overall_success_rate']:.1f}%")
        report.append(f"- **Average Processing Time**: {summary['average_processing_time']:.3f}s per template")
        report.append(f"- **Total Variables**: {summary['total_variables']:,}")
        report.append(f"- **Hybrid Variables Generated**: {summary['hybrid_variables_generated']:,} ({summary['hybrid_generation_rate']:.1f}%)")
        report.append(f"- **Average Quality Score**: {summary['average_quality_score']:.1f}%")
        report.append("")
        
        # Phase-by-Phase Results
        report.append("## Phase-by-Phase Results")
        for phase_name, phase_stats in summary['phase_success_rates'].items():
            if phase_stats['total'] > 0:
                report.append(f"### {phase_name.replace('_', ' ').title()}")
                report.append(f"- **Templates**: {phase_stats['total']}")
                report.append(f"- **Success Rate**: {phase_stats['success_rate']:.1f}%")
                report.append(f"- **Successful**: {phase_stats['successful']}/{phase_stats['total']}")
                report.append("")
        
        # Business-by-Business Results
        report.append("## Business-by-Business Results")
        for business_slug, business_stats in summary['business_success_rates'].items():
            report.append(f"### {business_slug.title()}")
            report.append(f"- **Total Validations**: {business_stats['total']}")
            report.append(f"- **Success Rate**: {business_stats['success_rate']:.1f}%")
            report.append(f"- **Successful**: {business_stats['successful']}/{business_stats['total']}")
            report.append("")
        
        # Performance Metrics
        report.append("## Performance Metrics")
        metrics = results['performance_metrics']
        
        # Processing time distribution
        processing_times = list(metrics['template_processing_times'].values())
        if processing_times:
            report.append(f"- **Fastest Template**: {min(processing_times):.3f}s")
            report.append(f"- **Slowest Template**: {max(processing_times):.3f}s")
            report.append(f"- **Median Processing Time**: {sorted(processing_times)[len(processing_times)//2]:.3f}s")
        report.append("")
        
        # Failed Validations
        if results['failed_validations']:
            report.append("## Failed Validations")
            for failure in results['failed_validations'][:10]:  # Show first 10 failures
                report.append(f"### {failure['business']} - {failure['phase']} - {failure['template']}")
                report.append(f"**Error**: {failure['error']}")
                report.append("")
            
            if len(results['failed_validations']) > 10:
                report.append(f"... and {len(results['failed_validations']) - 10} more failures")
                report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        
        if summary['overall_success_rate'] >= 95:
            report.append("✅ **Excellent Coverage**: System ready for production deployment")
        elif summary['overall_success_rate'] >= 85:
            report.append("⚠️ **Good Coverage**: Minor optimizations recommended")
        else:
            report.append("❌ **Insufficient Coverage**: Significant improvements needed")
        
        if summary['average_quality_score'] >= 85:
            report.append("✅ **High Quality**: AI-generated variables meet quality standards")
        else:
            report.append("⚠️ **Quality Improvement**: Review AI generation patterns")
        
        if summary['average_processing_time'] < 0.1:
            report.append("✅ **Excellent Performance**: Processing time within acceptable limits")
        elif summary['average_processing_time'] < 0.5:
            report.append("⚠️ **Acceptable Performance**: Consider optimization for large-scale use")
        else:
            report.append("❌ **Performance Issues**: Optimization required")
        
        report.append("")
        
        return '\n'.join(report)


def main():
    """Command-line interface for Phase 3 validation"""
    parser = argparse.ArgumentParser(description='Phase 3 BMDP Coverage Validator')
    parser.add_argument('--businesses', nargs='+', default=['grower', 'processor', 'distributor', 'marketplace'],
                       help='Business slugs to validate')
    parser.add_argument('--max-workers', type=int, default=4, help='Maximum parallel workers')
    parser.add_argument('--report-file', help='Output report file path')
    parser.add_argument('--results-file', help='Output detailed results JSON file')
    parser.add_argument('--project-root', default='/home/chris/bmdp', help='Project root directory')
    
    args = parser.parse_args()
    
    validator = Phase3Validator(args.project_root)
    
    print(f"Starting Phase 3 validation for businesses: {', '.join(args.businesses)}")
    print(f"Using {args.max_workers} parallel workers")
    
    # Run comprehensive validation
    results = validator.run_comprehensive_validation(args.businesses, args.max_workers)
    
    # Generate report
    report = validator.generate_comprehensive_report(results)
    
    if args.report_file:
        with open(args.report_file, 'w') as f:
            f.write(report)
        print(f"Report saved to: {args.report_file}")
    else:
        print(report)
    
    # Save detailed results
    if args.results_file:
        with open(args.results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Detailed results saved to: {args.results_file}")
    
    # Print summary
    summary = results['summary']
    print(f"\nValidation Complete:")
    print(f"Success Rate: {summary['overall_success_rate']:.1f}%")
    print(f"Quality Score: {summary['average_quality_score']:.1f}%")
    print(f"Processing Time: {summary['total_duration_seconds']:.2f}s")


if __name__ == '__main__':
    main()
