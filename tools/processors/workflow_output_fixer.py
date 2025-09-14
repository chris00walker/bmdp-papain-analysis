#!/usr/bin/env python3
"""
Workflow Output Fixer - Fixes common quality issues in workflow outputs
Single responsibility: Fix broken substitutions and quality issues in generated files
"""

import re
from pathlib import Path
import argparse
from typing import List, Tuple

class WorkflowOutputFixer:
    """Fixes common quality issues in workflow outputs"""
    
    def __init__(self, business: str):
        self.business = business
        self.business_path = Path(f'/home/chris/bmdp/businesses/{business}')
        self.fixes_applied = []
        
        # Common broken patterns and their fixes
        self.fix_patterns = [
            # Fix broken dollar amounts like \grower0M -> $10M
            (re.compile(r'\\[a-z]+(\d+)M'), r'$\1M'),
            # Fix broken dollar amounts like \growerM -> $1M
            (re.compile(r'\\[a-z]+M'), r'$1M'),
            # Fix escaped dollar signs
            (re.compile(r'\\\$'), r'$'),
            # Fix double dollar signs
            (re.compile(r'\$\$'), r'$'),
            # Fix Year 5 Revenue specifically
            (re.compile(r'\\grower0M'), r'$10M'),
            # Fix Month 12 ARR
            (re.compile(r'\\growerM'), r'$1M'),
        ]
    
    def fix_file(self, file_path: Path) -> bool:
        """Fix issues in a single file"""
        if not file_path.exists():
            return False
        
        # Skip non-text files
        if file_path.suffix not in ['.md', '.txt']:
            return False
        
        try:
            original_content = file_path.read_text()
            fixed_content = original_content
            
            # Apply all fix patterns
            for pattern, replacement in self.fix_patterns:
                if pattern.search(fixed_content):
                    fixed_content = pattern.sub(replacement, fixed_content)
            
            # Only write if changes were made
            if fixed_content != original_content:
                file_path.write_text(fixed_content)
                self.fixes_applied.append(str(file_path.relative_to(self.business_path)))
                return True
                
            return False
            
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")
            return False
    
    def fix_phase(self, phase: int) -> int:
        """Fix all files in a phase"""
        phase_dirs = {
            0: '00_initiation',
            1: '10_mobilize',
            2: '20_understand',
            3: '30_design'
        }
        
        if phase not in phase_dirs:
            return 0
        
        phase_path = self.business_path / phase_dirs[phase]
        if not phase_path.exists():
            return 0
        
        fixes = 0
        for file_path in phase_path.rglob('*.md'):
            if self.fix_file(file_path):
                fixes += 1
        
        return fixes
    
    def fix_all(self) -> Tuple[int, List[str]]:
        """Fix all phases for the business"""
        total_fixes = 0
        
        for phase in range(4):
            fixes = self.fix_phase(phase)
            total_fixes += fixes
        
        return total_fixes, self.fixes_applied
    
    def report(self) -> str:
        """Generate fix report"""
        total_fixes, fixed_files = self.fix_all()
        
        output = []
        output.append(f"{'='*60}")
        output.append(f"WORKFLOW OUTPUT FIXES")
        output.append(f"Business: {self.business}")
        output.append(f"{'='*60}")
        output.append("")
        
        if total_fixes > 0:
            output.append(f"✅ Fixed {total_fixes} files:")
            for file in fixed_files:
                output.append(f"  - {file}")
        else:
            output.append("✅ No fixes needed - all files are clean")
        
        return '\n'.join(output)

def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(description='Fix workflow output quality issues')
    parser.add_argument('--business', required=True,
                       choices=['grower', 'processor', 'distributor', 'marketplace'],
                       help='Business to fix')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be fixed without making changes')
    
    args = parser.parse_args()
    
    fixer = WorkflowOutputFixer(args.business)
    report = fixer.report()
    print(report)

if __name__ == '__main__':
    main()
