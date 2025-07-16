#!/usr/bin/env python3
"""
Fix import statements in test files to use proper libs. prefixes.
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix import statements in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix various import patterns
        replacements = [
            (r'from project import', 'from libs.project import'),
            (r'from terminal_editor import', 'from libs.terminal_editor import'),
            (r'from md_edit import', 'from libs.md_edit import'),
            (r'from parse_req_md import', 'from libs.parse_req_md import'),
            (r'from gen_html_doc import', 'from libs.gen_html_doc import'),
            # Fix path setup
            (r"sys\.path\.insert\(0, os\.path\.join\(os\.path\.dirname\(__file__\), '\.\.', 'libs'\)\)", 
             "sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))")
        ]
        
        changes_made = 0
        for old_pattern, new_pattern in replacements:
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                changes_made += 1
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed {changes_made} import(s) in {file_path.name}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all import statements in test files."""
    print("🔧 Fixing Import Statements in Test Files")
    print("=" * 50)
    
    # Get test directory
    test_dir = Path(__file__).parent
    
    # Find all Python test files
    test_files = list(test_dir.glob("test_*.py"))
    test_files.extend(test_dir.glob("demo_*.py"))
    test_files.extend(test_dir.glob("troubleshoot_*.py"))
    
    fixed_count = 0
    for test_file in sorted(test_files):
        if test_file.name == "fix_imports.py":
            continue  # Skip this script itself
        
        if fix_imports_in_file(test_file):
            fixed_count += 1
    
    print(f"\n📊 Summary: Fixed imports in {fixed_count} files")

if __name__ == "__main__":
    main()
