#!/usr/bin/env python3
"""
Simple test for type alias normalization.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_simple_aliases():
    """Simple test of alias functionality."""
    print("🧪 Simple Type Alias Test...")
    
    editor = TerminalEditor()
    
    # Test the normalization function
    print("\n1. Testing normalization function:")
    test_cases = [
        ('TIT', 'TITLE'),
        ('SUB', 'SUBTITLE'), 
        ('REQ', 'REQUIREMENT'),
        ('COM', 'COMMENT'),
        ('TITLE', 'TITLE'),  # Full names should work too
    ]
    
    for input_type, expected in test_cases:
        result = editor._normalize_item_type(input_type)
        status = "✅" if result == expected else "❌"
        print(f"   {status} '{input_type}' -> '{result}' (expected '{expected}')")
    
    # Test with a simple document
    print("\n2. Testing with document:")
    editor._create_new_document()
    
    # Try a simple add command with alias
    print("   Adding item with 'REQ' alias...")
    result = editor._process_command("add", ["after", "4", "REQ", "Test requirement using alias"])
    
    if result:
        print("   ✅ Add command succeeded")
        
        # Check what type was actually created
        parts = editor.md_editor.get_classified_parts()
        if len(parts) >= 5:
            new_part = parts[4]  # 5th item (0-indexed)
            print(f"   Created item type: {new_part['type']}")
            if new_part['type'] == 'REQUIREMENT':
                print("   ✅ Alias 'REQ' correctly converted to 'REQUIREMENT'")
            else:
                print(f"   ❌ Expected 'REQUIREMENT', got '{new_part['type']}'")
        else:
            print("   ❌ Item not added correctly")
    else:
        print("   ❌ Add command failed")
    
    print("\n3. Testing help command (shows aliases):")
    editor._process_command("help", [])

if __name__ == "__main__":
    test_simple_aliases()
