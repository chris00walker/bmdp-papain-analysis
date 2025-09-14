#!/usr/bin/env python3
"""
Fix Template Comments - Remove HTML comments and keep only Jinja2 comments
"""

import re
from pathlib import Path

def fix_template_comments(template_path: Path) -> bool:
    """Remove HTML comments from template, keeping only Jinja2 comments"""
    try:
        content = template_path.read_text()
        original = content
        
        # Remove HTML comment blocks that contain LLM GUIDANCE
        pattern = r'<!-- LLM GUIDANCE.*?-->\n*'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Also remove any duplicate newlines created
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        if content != original:
            template_path.write_text(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {template_path}: {e}")
        return False

def main():
    template_dir = Path('/home/chris/bmdp/templates/deliverables')
    fixed_count = 0
    
    for phase_dir in template_dir.iterdir():
        if phase_dir.is_dir() and phase_dir.name != 'shared':
            for template_file in phase_dir.glob('*.j2'):
                if fix_template_comments(template_file):
                    fixed_count += 1
                    print(f"✅ Fixed {template_file.relative_to(template_dir)}")
    
    print(f"\n✅ Fixed {fixed_count} templates - removed HTML comments")
    return 0

if __name__ == '__main__':
    exit(main())
