#!/usr/bin/env python3
"""
Debug HTML generation to see what elements are actually present.
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path to access libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.gen_html_doc import GenerateHTML

def debug_html_generation():
    """Debug HTML generation to see what's actually generated."""
    
    print("🔍 HTML Generation Debug")
    print("=" * 50)
    
    # Test data paths
    test_data_dir = Path(__file__).parent / "data"
    test_input_md = test_data_dir / "test_input.md"
    
    print(f"Reading markdown file: {test_input_md}")
    md_content = ReadMDFile(str(test_input_md))
    
    if not md_content:
        print("❌ Failed to read markdown file")
        return
    
    print(f"✅ Read {len(md_content)} characters")
    
    # Classify content
    classified_parts = ClassifyParts(md_content)
    if not classified_parts:
        print("❌ Failed to classify content")
        return
    
    print(f"✅ Classified {len(classified_parts)} parts")
    
    # Generate HTML
    html_content = GenerateHTML(classified_parts)
    if not html_content:
        print("❌ Failed to generate HTML")
        return
    
    print(f"✅ Generated {len(html_content)} characters of HTML")
    
    # Check for specific elements
    check_elements = [
        '<!DOCTYPE html>',
        '<html>',
        '<html ',  # Maybe it has attributes
        '<head>',
        '<body>',
        'expand-all-btn',
        'collapse-all-btn',
        'toggle-line-numbers-btn',
        'print-btn'
    ]
    
    print("\n🔍 Element Check:")
    for element in check_elements:
        if element in html_content:
            print(f"✅ Found: {element}")
        else:
            print(f"❌ Missing: {element}")
    
    # Show first 500 characters to see structure
    print("\n📝 HTML Structure (first 500 chars):")
    print("-" * 50)
    print(html_content[:500])
    print("-" * 50)
    
    # Show any button-related content
    print("\n🔘 Button-related content:")
    lines = html_content.split('\n')
    for i, line in enumerate(lines):
        if 'btn' in line.lower() or 'button' in line.lower():
            print(f"Line {i+1}: {line.strip()}")

if __name__ == "__main__":
    debug_html_generation()
