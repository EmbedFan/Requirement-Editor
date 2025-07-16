#!/usr/bin/env python3
"""
Test the integer ID fix for terminal editor.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_integer_ids():
    """Test that all IDs are now integers starting from 1000."""
    print("🧪 Testing Integer ID Fix")
    print("=" * 50)
    
    # Create a new document
    editor = TerminalEditor()
    editor._create_new_document()
    
    # Check the IDs in the new document
    parts = editor.md_editor.get_classified_parts()
    
    print("📋 Document structure with IDs:")
    for part in parts:
        item_id = part.get('id')
        item_type = part['type']
        description = part['description'][:50] + "..." if len(part['description']) > 50 else part['description']
        
        # Handle None IDs properly
        id_str = str(item_id) if item_id is not None else "None"
        print(f"  {item_type:12} | ID: {id_str:6} | {description}")
    
    print()
    
    # Verify all IDs are integers >= 1000
    print("🔍 ID Validation:")
    all_valid = True
    
    for part in parts:
        item_id = part.get('id')
        item_type = part['type']
        
        if item_type in ['REQUIREMENT', 'COMMENT', 'DATTR']:  # Items that should have IDs
            if item_id is None:
                print(f"  ❌ {item_type} has no ID")
                all_valid = False
            elif not isinstance(item_id, int):
                print(f"  ❌ {item_type} has non-integer ID: {item_id} (type: {type(item_id)})")
                all_valid = False
            elif item_id < 1000:
                print(f"  ❌ {item_type} has ID < 1000: {item_id}")
                all_valid = False
            else:
                print(f"  ✅ {item_type} has valid integer ID: {item_id}")
        elif item_type in ['TITLE', 'SUBTITLE']:  # Items that shouldn't have IDs
            if item_id is None:
                print(f"  ✅ {item_type} correctly has no ID")
            else:
                print(f"  ⚠️  {item_type} unexpectedly has ID: {item_id}")
    
    print()
    
    # Test next ID generation
    print("🔄 Testing next ID generation:")
    next_id = editor._get_next_available_id()
    print(f"  Next available ID: {next_id}")
    
    if next_id == 1003:  # Should be 1003 after 1000, 1001, 1002
        print("  ✅ Next ID generation working correctly")
    else:
        print(f"  ❌ Expected next ID to be 1003, got {next_id}")
        all_valid = False
    
    print()
    
    if all_valid:
        print("🎉 All ID validation tests PASSED!")
        print("✅ Integer IDs starting from 1000 are working correctly")
    else:
        print("❌ Some ID validation tests FAILED")
        print("🔧 Further fixes may be needed")

if __name__ == "__main__":
    test_integer_ids()
