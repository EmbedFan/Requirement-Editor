#!/usr/bin/env python3
"""
Test to reproduce the exact display issue reported by the user.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.terminal_editor import TerminalEditor

def test_exact_issue():
    """Test the exact content and see if we can reproduce the issue."""
    test_file = os.path.join(os.path.dirname(__file__), 'data', 'test_input.md')
    
    print("=== Reproducing User's Issue ===")
    print()
    
    # Check if file exists first
    if not os.path.exists(test_file):
        print(f"❌ Test file '{test_file}' not found.")
        return False
    
    # 1. Test raw content
    content = ReadMDFile(test_file)
    if content is None:
        print(f"❌ Failed to read file '{test_file}'")
        return False
        
    print(f"1. Raw file content:")
    print(f"   Length: {len(content)}")
    print(f"   Content preview: {repr(content[:100])}...")
    print()
    
    # 2. Test parsing
    parts = ClassifyParts(content)
    if not parts:
        print("❌ Failed to classify content or no parts found")
        return False
        
    print(f"2. Parsed parts ({len(parts)} found):")
    for i, part in enumerate(parts):
        print(f"   Part {i+1}: Line {part['line_number']}, Type {part['type']}, Desc: {repr(part['description'])}")
    print()
    
    # 3. Test terminal editor formatting
    editor = TerminalEditor()
    editor._load_file(test_file)
    
    print(f"3. Terminal editor formatting:")
    if editor.md_editor:
        for part in editor.md_editor.classified_parts:
            formatted = editor._format_line(part, show_full=True)
            print(f"   {formatted}")
    print()
    
    # 4. Check if there's any way the user's output could occur
    print(f"4. Testing potential issue scenarios:")
    
    # Check if the description field contains raw content
    title_part = parts[0] if parts else None
    if title_part:
        print(f"   Title description: {repr(title_part['description'])}")
        print(f"   Title description length: {len(title_part['description'])}")
        
        # Check if the description accidentally contains the whole content
        if len(title_part['description']) > 50:  # Suspiciously long for just "Test Document"
            print(f"   ⚠️  Title description seems too long!")
            print(f"   ⚠️  This might be the issue!")
        
    print()

if __name__ == "__main__":
    test_exact_issue()
