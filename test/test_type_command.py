#!/usr/bin/env python3
"""
Test the type command with aliases specifically.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_type_command_aliases():
    """Test the type command with aliases."""
    print("🧪 Testing type command with aliases...")
    
    editor = TerminalEditor()
    editor._create_new_document()
    
    # Display initial document
    print("\n1. Initial document structure:")
    editor._process_command("list", [])
    
    # Test changing types using aliases
    print("\n2. Testing type command with aliases:")
    
    # Change line 3 (COMMENT) to REQ (REQUIREMENT)
    print("   Changing line 3 from COMMENT to REQ...")
    result = editor._process_command("type", ["3", "REQ"])
    
    if result:
        print("   ✅ Type command succeeded")
        
        # Verify the change
        parts = editor.md_editor.get_classified_parts()
        line_3_part = parts[2]  # 0-indexed
        print(f"   Line 3 type is now: {line_3_part['type']}")
        
        if line_3_part['type'] == 'REQUIREMENT':
            print("   ✅ Successfully changed COM -> REQ -> REQUIREMENT")
        else:
            print(f"   ❌ Expected REQUIREMENT, got {line_3_part['type']}")
    else:
        print("   ❌ Type command failed")
    
    # Test another change: line 4 (REQUIREMENT) to COM (COMMENT)
    print("\n   Changing line 4 from REQUIREMENT to COM...")
    result = editor._process_command("type", ["4", "COM"])
    
    if result:
        print("   ✅ Type command succeeded")
        
        # Verify the change
        parts = editor.md_editor.get_classified_parts()
        line_4_part = parts[3]  # 0-indexed
        print(f"   Line 4 type is now: {line_4_part['type']}")
        
        if line_4_part['type'] == 'COMMENT':
            print("   ✅ Successfully changed REQ -> COM -> COMMENT")
        else:
            print(f"   ❌ Expected COMMENT, got {line_4_part['type']}")
    else:
        print("   ❌ Type command failed")
    
    # Show final document
    print("\n3. Final document structure:")
    editor._process_command("list", [])
    
    # Test full names still work
    print("\n4. Testing full type names still work:")
    result = editor._process_command("type", ["3", "SUBTITLE"])
    if result:
        print("   ✅ Full type name SUBTITLE works")
    else:
        print("   ❌ Full type name failed")

if __name__ == "__main__":
    test_type_command_aliases()
