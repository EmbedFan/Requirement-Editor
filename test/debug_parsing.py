#!/usr/bin/env python3
"""
Debug the file parsing issue.
"""

import os
import sys

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

from parse_req_md import ReadMDFile, ClassifyParts

def debug_parsing():
    """Debug the file parsing to see why it's not splitting properly."""
    
    print("🔍 Debugging File Parsing Issue")
    print("=" * 60)
    
    test_file = "test/data/new-2.md"
    
    # Step 1: Check raw file content
    print("1. Reading raw file content...")
    content = ReadMDFile(test_file)
    
    if content:
        print(f"✅ File read successfully")
        print(f"📝 Content length: {len(content)} characters")
        print(f"📋 Raw content: {repr(content)}")
        print()
        
        # Step 2: Check how it splits into lines
        print("2. Splitting into lines...")
        lines = content.split('\n')
        print(f"📄 Number of lines: {len(lines)}")
        
        for i, line in enumerate(lines, 1):
            print(f"   Line {i}: {repr(line)}")
        print()
        
        # Step 3: Test classification
        print("3. Testing classification...")
        classified_parts = ClassifyParts(content)
        
        if classified_parts:
            print(f"📊 Classified into {len(classified_parts)} parts:")
            for i, part in enumerate(classified_parts, 1):
                print(f"   Part {i}: [{part['type']}] Line {part['line_number']}: {repr(part['description'][:50])}")
        else:
            print("❌ Classification failed")
            
    else:
        print("❌ Failed to read file")
    
    print("=" * 60)

if __name__ == "__main__":
    debug_parsing()
