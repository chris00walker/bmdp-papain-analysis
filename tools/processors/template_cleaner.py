#!/usr/bin/env python3
"""
Clean LLM instructions from templates to prevent them appearing in output documents.
"""

import os
import re
from pathlib import Path

def clean_llm_instructions(file_path):
    """Remove LLM instructions and placeholders from template file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Remove LLM instruction comment blocks (lines starting with # LLM Instruction:)
    content = re.sub(r'^# LLM Instruction:.*?\n(?:^#.*?\n)*', '', content, flags=re.MULTILINE)
    
    # Replace LLM placeholders with generic content
    replacements = {
        r'\[LLM: Generate realistic session date\]': 'TBD',
        r'\[LLM: Define appropriate participants for.*?\]': 'Core team, industry experts, customer representatives',
        r'\[LLM: Specify.*?methodology.*?\]': 'Systematic methodology approach',
        r'\[LLM: Define appropriate duration.*?\]': '2-4 hour structured session',
        r'\[LLM: Generate.*?Name\]': 'Option A',
        r'\[LLM: Generate comprehensive.*?\]': 'Detailed analysis and recommendations',
        r'\[LLM: Define.*?\]': 'TBD - To be defined during implementation',
        r'\[LLM: Create.*?\]': 'TBD - To be created during implementation',
        r'\[LLM: .*?\]': 'TBD'
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    """Clean all template files"""
    templates_dir = Path('/home/chris/bmdp/templates')
    
    cleaned_files = []
    for template_file in templates_dir.rglob('*.j2'):
        if clean_llm_instructions(template_file):
            cleaned_files.append(str(template_file))
    
    print(f"Cleaned {len(cleaned_files)} template files:")
    for file_path in cleaned_files:
        print(f"  - {file_path}")

if __name__ == '__main__':
    main()
