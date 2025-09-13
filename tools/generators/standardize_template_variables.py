#!/usr/bin/env python3
"""
Template Variable Standardization Tool

Converts lowercase template variables with default() fallbacks to uppercase 
variables that work with the hybrid parser-LLM pipeline.

Usage:
    python standardize_template_variables.py --directory /path/to/templates [--dry-run]
"""

import os
import re
import argparse
from pathlib import Path

def standardize_variables_in_file(file_path, dry_run=False):
    """Convert lowercase variables to uppercase in a single template file"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    # Pattern to match {{ variable_name | default("...") }} or {{ variable_name }}
    variable_pattern = r'\{\{\s*([a-z_][a-z0-9_]*)\s*(\|\s*default\([^}]+\))?\s*\}\}'
    
    def replace_variable(match):
        var_name = match.group(1)
        default_part = match.group(2)
        
        # Convert to uppercase
        uppercase_var = var_name.upper()
        
        # Remove default() fallback since hybrid parser provides intelligent defaults
        result = f"{{{{ {uppercase_var} }}}}"
        
        changes_made.append(f"  {var_name} → {uppercase_var}")
        return result
    
    # Apply replacements
    content = re.sub(variable_pattern, replace_variable, content)
    
    if changes_made and not dry_run:
        with open(file_path, 'w') as f:
            f.write(content)
    
    return len(changes_made), changes_made

def standardize_directory(directory_path, dry_run=False):
    """Standardize all .j2 template files in a directory"""
    
    directory = Path(directory_path)
    if not directory.exists():
        print(f"Error: Directory {directory_path} does not exist")
        return
    
    total_changes = 0
    files_processed = 0
    
    print(f"{'DRY RUN: ' if dry_run else ''}Standardizing template variables in {directory_path}")
    print("=" * 60)
    
    for template_file in directory.glob("*.j2"):
        changes_count, changes_list = standardize_variables_in_file(template_file, dry_run)
        
        if changes_count > 0:
            files_processed += 1
            total_changes += changes_count
            
            print(f"\n📄 {template_file.name}")
            print(f"   {changes_count} variables standardized:")
            for change in changes_list:
                print(change)
    
    print("\n" + "=" * 60)
    print(f"Summary: {files_processed} files processed, {total_changes} variables standardized")
    
    if dry_run:
        print("\n⚠️  DRY RUN - No files were actually modified")
        print("   Run without --dry-run to apply changes")

def main():
    parser = argparse.ArgumentParser(description='Standardize template variables to uppercase')
    parser.add_argument('--directory', required=True, help='Directory containing .j2 template files')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without applying them')
    
    args = parser.parse_args()
    
    standardize_directory(args.directory, args.dry_run)

if __name__ == '__main__':
    main()
