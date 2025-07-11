#!/usr/bin/env python3
"""
Debug script to identify display issue with markdown content.
Tests how content is read and processed by the parser.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

from parse_req_md import ReadMDFile, ClassifyParts

def debug_content_processing():
    """Debug the content processing pipeline."""
    test_file = os.path.join(os.path.dirname(__file__), 'data', 'new-2.md')
    
    print("=== Debug Content Processing ===")
    print(f"Test file: {test_file}")
    print()
    
    # Step 1: Read file content
    print("1. Reading file content...")
    content = ReadMDFile(test_file)
    if content is None:
        print("ERROR: Could not read file")
        return
    
    print(f"Raw content length: {len(content)}")
    print("Raw content (with repr to show escape sequences):")
    print(repr(content))
    print()
    
    print("Raw content (as displayed):")
    print(content)
    print()
    
    # Step 2: Classify parts
    print("2. Classifying parts...")
    parts = ClassifyParts(content)
    
    print(f"Number of parts found: {len(parts)}")
    print()
    
    # Step 3: Display parts
    print("3. Parts analysis:")
    for i, part in enumerate(parts):
        print(f"Part {i+1}:")
        print(f"  Line number: {part['line_number']}")
        print(f"  Type: {part['type']}")
        print(f"  Description: {repr(part['description'])}")
        print(f"  Indent: {part['indent']}")
        print(f"  ID: {part.get('id')}")
        print()

if __name__ == "__main__":
    debug_content_processing()
