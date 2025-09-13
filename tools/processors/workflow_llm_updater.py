#!/usr/bin/env python3
"""
Update all workflows to include LLM processing step after template rendering.
"""

import re
from pathlib import Path

def update_workflow_with_llm_processing(file_path):
    """Update workflow file to include LLM processing after template rendering"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to match template rendering commands that output .md files
    # Only add LLM processing for markdown files, not CSV files
    pattern = r'(python tools/generators/render_template\.py[^`]*?--output ([^`\s]+\.md))'
    
    def add_llm_processing(match):
        original_command = match.group(1)
        output_file = match.group(2)
        
        # Add LLM processing step
        return f"{original_command} && \\\npython tools/processors/llm_processor.py \\\n  --input {output_file}"
    
    # Apply the replacement
    updated_content = re.sub(pattern, add_llm_processing, content, flags=re.MULTILINE | re.DOTALL)
    
    # Only write if content changed
    if updated_content != original_content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        return True
    return False

def main():
    """Update all workflow files"""
    workflows_dir = Path('/home/chris/bmdp/.windsurf/workflows')
    
    # List of workflow files to update
    workflow_files = [
        'bmdp-phase0-initiation.md',
        'bmdp-phase1-mobilize.md', 
        'bmdp-phase2-understand.md',
        'bmdp-phase3-design.md'
    ]
    
    updated_files = []
    for workflow_file in workflow_files:
        file_path = workflows_dir / workflow_file
        if file_path.exists():
            if update_workflow_with_llm_processing(file_path):
                updated_files.append(str(file_path))
    
    print(f"Updated {len(updated_files)} workflow files with LLM processing:")
    for file_path in updated_files:
        print(f"  - {file_path}")

if __name__ == '__main__':
    main()
