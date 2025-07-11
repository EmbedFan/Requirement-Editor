#!/usr/bin/env python3
"""
Script to update import paths in all test files after moving them to test/ directory.
"""

import os
import glob
import re

def update_test_file_imports():
    """Update import paths in all test files."""
    test_dir = "."  # Current directory (test/)
    test_files = glob.glob(os.path.join(test_dir, "test_*.py"))
    
    print(f"Found {len(test_files)} test files to update:")
    
    for test_file in test_files:
        print(f"  Processing: {test_file}")
        
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update the sys.path.append line
            old_pattern = r"sys\.path\.append\(os\.path\.join\(os\.path\.dirname\(__file__\), 'libs'\)\)"
            new_replacement = "sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))"
            
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_replacement, content)
                print(f"    ✓ Updated sys.path line")
            else:
                print(f"    - No sys.path update needed")
            
            # Also handle any other variations
            old_pattern2 = r"sys\.path\.append\(os\.path\.join\(os\.path\.dirname\(__file__\), '\.\.', 'libs'\)\)"
            if re.search(old_pattern2, content):
                content = re.sub(old_pattern2, new_replacement, content)
                print(f"    ✓ Updated alternative sys.path line")
            
            # Write back the updated content
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"    ✓ Updated {test_file}")
            
        except Exception as e:
            print(f"    ❌ Error updating {test_file}: {e}")
    
    print("\n✅ Import path update completed!")

if __name__ == "__main__":
    update_test_file_imports()
