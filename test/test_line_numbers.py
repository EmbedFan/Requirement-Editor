#!/usr/bin/env python3
"""
Test to confirm the line number issue with empty lines.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from libs.parse_req_md import ReadMDFile, ClassifyParts

def test_line_numbers():
    print("Testing line number assignment")
    print("=" * 40)
    
    file_path = "test/real_requirements/shopping_list_app.md"
    
    # Read the file and show actual line numbers
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("Actual file lines:")
    for i, line in enumerate(lines, 1):
        is_empty = len(line.strip()) == 0
        status = " (EMPTY)" if is_empty else ""
        print(f"  {i:2d}: '{line.rstrip()}'{status}")
    
    print(f"\nFile has {len(lines)} total lines")
    
    # Now check how ClassifyParts handles this
    md_content = ReadMDFile(file_path)
    classified_parts = ClassifyParts(md_content)
    
    print(f"\nClassifyParts returned {len(classified_parts)} parts:")
    for i, part in enumerate(classified_parts, 1):
        print(f"  Part {i}: line_number={part['line_number']}, type={part['type']}, desc='{part['description'][:30]}...'")
    
    # Check what the terminal editor would display
    print(f"\nTerminal editor display logic:")
    print("Looking for parts with line_number between 1 and 6:")
    for i in range(1, 7):  # Looking for lines 1-6
        found_parts = [p for p in classified_parts if p['line_number'] == i]
        if found_parts:
            part = found_parts[0]
            print(f"  Line {i}: FOUND - {part['type']} - {part['description'][:30]}...")
        else:
            print(f"  Line {i}: NOT FOUND (would be skipped)")

if __name__ == "__main__":
    test_line_numbers()
