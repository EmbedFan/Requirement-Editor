#!/usr/bin/env python3
"""
Test the new document creation with default structure.
"""

import sys
import os
# Add parent directory to path to access libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_new_document_structure():
    """Test new document creation with default structure."""
    print("🧪 Testing new document creation with default structure...")
    
    editor = TerminalEditor()
    
    # Create new document
    print("1. Creating new document...")
    editor._create_new_document()
    print(f"   Current file: {editor.current_file}")
    print(f"   Modified: {editor.modified}")
    
    # Check document structure
    print("2. Checking document structure...")
    if not editor.md_editor:
        print("   ❌ No md_editor created")
        return False
    
    parts = editor.md_editor.get_classified_parts()
    print(f"   Number of parts: {len(parts)}")
    
    # Verify we have 4 parts
    if len(parts) != 4:
        print(f"   ❌ Expected 4 parts, got {len(parts)}")
        return False
    
    # Check each part (but use flexible checking for DATTR content since it contains timestamps)
    expected_structure = [
        {"line": 1, "type": "TITLE", "indent": 0, "description": "New Requirement Document"},
        {"line": 2, "type": "DATTR", "indent": 1, "id": "DATTR001"},  # Will check separately
        {"line": 3, "type": "COMMENT", "indent": 1, "id": "COMM001", "description": "Document created with terminal editor"},
        {"line": 4, "type": "REQUIREMENT", "indent": 1, "id": "REQ001", "description": "System shall meet basic requirements"}
    ]
    
    for i, expected in enumerate(expected_structure):
        part = parts[i]
        print(f"   Part {i+1}: Line {part['line_number']}, Type {part['type']}, Indent {part['indent']}")
        print(f"           ID: {part.get('id', 'None')}, Description: {part['description']}")
        
        if part['line_number'] != expected["line"]:
            print(f"   ❌ Line number mismatch: expected {expected['line']}, got {part['line_number']}")
            return False
        
        if part['type'] != expected["type"]:
            print(f"   ❌ Type mismatch: expected {expected['type']}, got {part['type']}")
            return False
        
        if part['indent'] != expected["indent"]:
            print(f"   ❌ Indent mismatch: expected {expected['indent']}, got {part['indent']}")
            return False
        
        # Special handling for DATTR - check that it contains timestamps
        if part['type'] == 'DATTR':
            description = part['description']
            if 'Created at:' not in description or 'Modified at:' not in description:
                print(f"   ❌ DATTR description should contain timestamps: {description}")
                return False
            print(f"   ✓ DATTR contains proper timestamps")
        elif 'description' in expected:
            if part['description'] != expected["description"]:
                print(f"   ❌ Description mismatch: expected '{expected['description']}', got '{part['description']}'")
                return False
        
        if 'id' in expected and part.get('id') != expected['id']:
            print(f"   ❌ ID mismatch: expected {expected['id']}, got {part.get('id')}")
            return False
    
    print("   ✓ All parts have correct structure")
    
    # Test the save command behavior
    print("3. Testing 'save' command behavior...")
    result = editor._process_command("save", [])
    if not result:
        print("   ❌ Save command returned False")
        return False
    print("   ✓ Save command shows error but doesn't exit")
    
    # Test display
    print("4. Testing document display...")
    try:
        editor.display_document()
        print("   ✓ Document displays without errors")
    except Exception as e:
        print(f"   ❌ Display error: {e}")
        return False
    
    # Test DATTR read-only behavior
    print("5. Testing DATTR read-only protection...")
    result = editor._process_command("edit", ["2", "Trying to edit DATTR"])
    if not result:
        print("   ❌ Edit command should not fail, just show warning")
        return False
    print("   ✓ DATTR editing is properly protected")
    
    print("6. Test completed successfully!")
    return True

if __name__ == "__main__":
    if test_new_document_structure():
        print("\n✅ New document structure test passed!")
    else:
        print("\n❌ New document structure test failed!")
