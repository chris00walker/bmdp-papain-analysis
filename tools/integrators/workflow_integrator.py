#!/usr/bin/env python3
"""
Workflow Integrator - Updates BMDP workflows to use hybrid parser with performance monitoring
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import argparse
import shutil
from datetime import datetime


class WorkflowIntegrator:
    """Integrates hybrid parser into BMDP workflows with performance monitoring"""
    
    def __init__(self, project_root='/home/chris/bmdp'):
        self.project_root = Path(project_root)
        self.workflows_dir = self.project_root / '.windsurf' / 'workflows'
        self.tools_dir = self.project_root / 'tools'
        
        # Workflow patterns to update
        self.update_patterns = {
            'env_export': {
                'old_pattern': r'eval \$\(python tools/parsers/brief_parser\.py --business \$1 --output-format env\)',
                'new_pattern': 'eval $(python tools/parsers/brief_parser.py --business $1 --output-format env)'
            },
            'template_render': {
                'old_pattern': r'python tools/generators/render_template\.py',
                'new_pattern': 'python tools/generators/template_processor.py --template-file'
            },
            'hybrid_render': {
                'old_pattern': r'--template ([^\s]+)',
                'new_pattern': '--template-file \\1 --test-hybrid $1'
            }
        }
        
        # Performance monitoring injection points
        self.monitoring_commands = {
            'start_timer': 'PHASE_START_TIME=$(date +%s.%N)',
            'end_timer': 'PHASE_END_TIME=$(date +%s.%N)',
            'log_performance': 'echo "Phase execution time: $(echo "$PHASE_END_TIME - $PHASE_START_TIME" | bc)s" >> performance.log'
        }
    
    def backup_workflows(self) -> Path:
        """Create backup of existing workflows"""
        backup_dir = self.project_root / 'workflow_backups' / datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        for workflow_file in self.workflows_dir.glob('*.md'):
            shutil.copy2(workflow_file, backup_dir / workflow_file.name)
        
        print(f"Workflows backed up to: {backup_dir}")
        return backup_dir
    
    def update_workflow_file(self, workflow_path: Path) -> Dict[str, Any]:
        """Update a single workflow file to use hybrid parser"""
        
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        original_content = content
        updates_made = []
        
        # Add performance monitoring at the beginning
        if 'PHASE_START_TIME' not in content:
            # Find the first bash command block
            bash_block_pattern = r'(```bash\n)'
            if re.search(bash_block_pattern, content):
                content = re.sub(
                    bash_block_pattern,
                    f'\\1{self.monitoring_commands["start_timer"]}\n',
                    content,
                    count=1
                )
                updates_made.append('Added performance monitoring start timer')
        
        # Update environment variable exports to use hybrid parser
        old_env_pattern = self.update_patterns['env_export']['old_pattern']
        new_env_pattern = self.update_patterns['env_export']['new_pattern']
        
        if re.search(old_env_pattern, content):
            content = re.sub(old_env_pattern, new_env_pattern, content)
            updates_made.append('Updated environment variable export commands')
        
        # Update template rendering to use hybrid approach
        template_render_pattern = r'python tools/generators/render_template\.py\s+--template\s+([^\s]+)\s+--output\s+([^\s]+)'
        
        def replace_template_render(match):
            template_path = match.group(1)
            output_path = match.group(2)
            return f'python tools/generators/template_processor.py --template-file {template_path} --test-hybrid $1 > {output_path}'
        
        if re.search(template_render_pattern, content):
            content = re.sub(template_render_pattern, replace_template_render, content)
            updates_made.append('Updated template rendering to use hybrid approach')
        
        # Add performance monitoring at the end
        if 'PHASE_END_TIME' not in content:
            # Find the last bash command block
            bash_blocks = list(re.finditer(r'```bash\n(.*?)```', content, re.DOTALL))
            if bash_blocks:
                last_block = bash_blocks[-1]
                block_content = last_block.group(1)
                
                # Add performance monitoring before the closing ```
                new_block_content = block_content.rstrip() + f'\n\n{self.monitoring_commands["end_timer"]}\n{self.monitoring_commands["log_performance"]}\n'
                content = content[:last_block.start(1)] + new_block_content + content[last_block.end(1):]
                updates_made.append('Added performance monitoring end timer')
        
        # Add hybrid validation step
        if 'hybrid validation' not in content.lower():
            validation_command = '''
# Validate hybrid variable coverage and quality
python tools/validators/template_sync.py --hybrid-validation --business-slug $1 --hybrid-report-file businesses/$1/hybrid_validation_report.md
'''
            
            # Insert before the final performance logging
            if self.monitoring_commands["log_performance"] in content:
                content = content.replace(
                    self.monitoring_commands["log_performance"],
                    validation_command + self.monitoring_commands["log_performance"]
                )
                updates_made.append('Added hybrid validation step')
        
        # Write updated content if changes were made
        if content != original_content:
            with open(workflow_path, 'w') as f:
                f.write(content)
        
        return {
            'file': workflow_path.name,
            'updates_made': updates_made,
            'has_changes': content != original_content
        }
    
    def integrate_all_workflows(self) -> Dict[str, Any]:
        """Integrate hybrid parser into all BMDP workflows"""
        
        # Create backup
        backup_dir = self.backup_workflows()
        
        results = {
            'backup_location': str(backup_dir),
            'workflows_processed': [],
            'total_updates': 0,
            'successful_integrations': 0,
            'failed_integrations': 0,
            'errors': []
        }
        
        # Process each workflow file
        for workflow_file in self.workflows_dir.glob('*.md'):
            try:
                update_result = self.update_workflow_file(workflow_file)
                results['workflows_processed'].append(update_result)
                
                if update_result['has_changes']:
                    results['successful_integrations'] += 1
                    results['total_updates'] += len(update_result['updates_made'])
                
            except Exception as e:
                results['failed_integrations'] += 1
                results['errors'].append({
                    'file': workflow_file.name,
                    'error': str(e)
                })
        
        return results
    
    def create_performance_monitoring_tool(self):
        """Create performance monitoring and analysis tool"""
        
        monitoring_script = '''#!/usr/bin/env python3
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
        
        return '\\n'.join(report)


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
'''
        
        monitor_file = self.tools_dir / 'monitors' / 'performance_monitor.py'
        monitor_file.parent.mkdir(exist_ok=True)
        
        with open(monitor_file, 'w') as f:
            f.write(monitoring_script)
        
        # Make executable
        os.chmod(monitor_file, 0o755)
        
        return monitor_file
    
    def generate_integration_report(self, integration_results: Dict[str, Any]) -> str:
        """Generate workflow integration report"""
        
        report = []
        report.append("# BMDP Workflow Integration Report")
        report.append("")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Backup Location**: {integration_results['backup_location']}")
        report.append("")
        
        # Summary
        report.append("## Integration Summary")
        report.append(f"- **Workflows Processed**: {len(integration_results['workflows_processed'])}")
        report.append(f"- **Successful Integrations**: {integration_results['successful_integrations']}")
        report.append(f"- **Failed Integrations**: {integration_results['failed_integrations']}")
        report.append(f"- **Total Updates Made**: {integration_results['total_updates']}")
        report.append("")
        
        # Detailed Results
        report.append("## Workflow Updates")
        for workflow_result in integration_results['workflows_processed']:
            status = "✅ Updated" if workflow_result['has_changes'] else "ℹ️ No changes needed"
            report.append(f"### {workflow_result['file']} - {status}")
            
            if workflow_result['updates_made']:
                for update in workflow_result['updates_made']:
                    report.append(f"- {update}")
            else:
                report.append("- No updates required")
            report.append("")
        
        # Errors
        if integration_results['errors']:
            report.append("## Integration Errors")
            for error in integration_results['errors']:
                report.append(f"### {error['file']}")
                report.append(f"**Error**: {error['error']}")
                report.append("")
        
        # Next Steps
        report.append("## Next Steps")
        report.append("1. Test updated workflows with sample business data")
        report.append("2. Monitor performance logs during execution")
        report.append("3. Run Phase 3 validation to verify integration success")
        report.append("4. Review and optimize any performance bottlenecks")
        report.append("")
        
        return '\n'.join(report)


def main():
    """Command-line interface for workflow integration"""
    parser = argparse.ArgumentParser(description='BMDP Workflow Integrator')
    parser.add_argument('--report-file', help='Output integration report file')
    parser.add_argument('--project-root', default='/home/chris/bmdp', help='Project root directory')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
    
    args = parser.parse_args()
    
    integrator = WorkflowIntegrator(args.project_root)
    
    if args.dry_run:
        print("DRY RUN: Showing what would be changed...")
        # TODO: Implement dry run functionality
        return
    
    print("Starting BMDP workflow integration...")
    
    # Integrate workflows
    results = integrator.integrate_all_workflows()
    
    # Create performance monitoring tool
    monitor_file = integrator.create_performance_monitoring_tool()
    print(f"Performance monitoring tool created: {monitor_file}")
    
    # Generate report
    report = integrator.generate_integration_report(results)
    
    if args.report_file:
        with open(args.report_file, 'w') as f:
            f.write(report)
        print(f"Integration report saved to: {args.report_file}")
    else:
        print(report)
    
    # Summary
    print(f"\nIntegration Complete:")
    print(f"Workflows Updated: {results['successful_integrations']}")
    print(f"Total Updates: {results['total_updates']}")
    print(f"Backup Location: {results['backup_location']}")


if __name__ == '__main__':
    main()
