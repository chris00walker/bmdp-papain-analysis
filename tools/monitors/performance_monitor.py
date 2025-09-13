#!/usr/bin/env python3
"""
BMDP Performance Monitor - Analyzes workflow execution performance
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any
import argparse
from datetime import datetime
import statistics


class PerformanceMonitor:
    """Monitors and analyzes BMDP workflow performance"""
    
    def __init__(self, project_root='/home/chris/bmdp'):
        self.project_root = Path(project_root)
    
    def parse_performance_logs(self, log_file: Path = None) -> Dict[str, Any]:
        """Parse performance logs from workflow executions"""
        
        if log_file is None:
            log_file = self.project_root / 'performance.log'
        
        if not log_file.exists():
            return {'error': f'Performance log not found: {log_file}'}
        
        execution_times = []
        
        with open(log_file, 'r') as f:
            for line in f:
                # Parse execution time entries
                match = re.search(r'Phase execution time: ([0-9.]+)s', line)
                if match:
                    execution_times.append(float(match.group(1)))
        
        if not execution_times:
            return {'error': 'No performance data found in log'}
        
        return {
            'total_executions': len(execution_times),
            'total_time': sum(execution_times),
            'average_time': statistics.mean(execution_times),
            'median_time': statistics.median(execution_times),
            'min_time': min(execution_times),
            'max_time': max(execution_times),
            'std_dev': statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
            'execution_times': execution_times
        }
    
    def generate_performance_report(self, performance_data: Dict[str, Any]) -> str:
        """Generate performance analysis report"""
        
        if 'error' in performance_data:
            return f"Performance Analysis Error: {performance_data['error']}"
        
        report = []
        report.append("# BMDP Workflow Performance Report")
        report.append("")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary Statistics
        report.append("## Performance Summary")
        report.append(f"- **Total Executions**: {performance_data['total_executions']}")
        report.append(f"- **Total Execution Time**: {performance_data['total_time']:.2f}s")
        report.append(f"- **Average Execution Time**: {performance_data['average_time']:.2f}s")
        report.append(f"- **Median Execution Time**: {performance_data['median_time']:.2f}s")
        report.append(f"- **Fastest Execution**: {performance_data['min_time']:.2f}s")
        report.append(f"- **Slowest Execution**: {performance_data['max_time']:.2f}s")
        report.append(f"- **Standard Deviation**: {performance_data['std_dev']:.2f}s")
        report.append("")
        
        # Performance Analysis
        report.append("## Performance Analysis")
        
        avg_time = performance_data['average_time']
        if avg_time < 30:
            report.append("✅ **Excellent Performance**: Average execution under 30 seconds")
        elif avg_time < 60:
            report.append("⚠️ **Good Performance**: Average execution under 1 minute")
        elif avg_time < 120:
            report.append("⚠️ **Acceptable Performance**: Average execution under 2 minutes")
        else:
            report.append("❌ **Performance Issues**: Average execution over 2 minutes")
        
        # Consistency Analysis
        if performance_data['std_dev'] < avg_time * 0.2:
            report.append("✅ **Consistent Performance**: Low execution time variance")
        elif performance_data['std_dev'] < avg_time * 0.5:
            report.append("⚠️ **Moderate Variance**: Some execution time inconsistency")
        else:
            report.append("❌ **High Variance**: Significant execution time inconsistency")
        
        report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        
        if avg_time > 60:
            report.append("- Consider optimizing template processing pipeline")
            report.append("- Review hybrid variable generation efficiency")
        
        if performance_data['std_dev'] > avg_time * 0.3:
            report.append("- Investigate causes of execution time variance")
            report.append("- Consider caching mechanisms for repeated operations")
        
        if performance_data['max_time'] > avg_time * 2:
            report.append("- Identify and optimize outlier executions")
            report.append("- Implement timeout mechanisms for long-running operations")
        
        report.append("")
        
        return '\n'.join(report)


def main():
    """Command-line interface for performance monitoring"""
    parser = argparse.ArgumentParser(description='BMDP Performance Monitor')
    parser.add_argument('--log-file', help='Performance log file path')
    parser.add_argument('--report-file', help='Output report file path')
    parser.add_argument('--project-root', default='/home/chris/bmdp', help='Project root directory')
    
    args = parser.parse_args()
    
    monitor = PerformanceMonitor(args.project_root)
    
    # Parse performance data
    log_file = Path(args.log_file) if args.log_file else None
    performance_data = monitor.parse_performance_logs(log_file)
    
    # Generate report
    report = monitor.generate_performance_report(performance_data)
    
    if args.report_file:
        with open(args.report_file, 'w') as f:
            f.write(report)
        print(f"Performance report saved to: {args.report_file}")
    else:
        print(report)


if __name__ == '__main__':
    main()
