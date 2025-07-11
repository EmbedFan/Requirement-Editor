#!/usr/bin/env python3
"""
Practical test of the ID fix - create a new document and add items to verify IDs.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_practical_new_document():
    """Create a new document and add items to verify integer IDs."""
    print("🔬 Creating new document and adding items...")
    
    editor = TerminalEditor()
    
    # Create new document
    editor._create_new_document()
    
    # Simulate adding items via terminal commands
    print("\n📝 Adding new requirement...")
    # Simulating: add after 4 requirement "New system requirement"
    md_editor = editor.md_editor
    result = md_editor.add_item_after(4, 'REQUIREMENT', 'New system requirement')
    print(f"   Added requirement with ID: {result['id']} (type: {type(result['id'])})")
    
    print("📝 Adding new comment...")
    # Simulating: add after 5 comment "Implementation note"
    result = md_editor.add_item_after(5, 'COMMENT', 'Implementation note')
    print(f"   Added comment with ID: {result['id']} (type: {type(result['id'])})")
    
    print("📝 Adding another requirement...")
    # Simulating: add under 1 requirement "Sub-requirement under title"
    result = md_editor.add_item_under(1, 'REQUIREMENT', 'Sub-requirement under title')
    print(f"   Added requirement with ID: {result['id']} (type: {type(result['id'])})")
    
    # Display the document structure
    print("\n📄 Final document structure:")
    parts = md_editor.get_classified_parts()
    for part in parts:
        indent_str = "  " * part['indent']
        part_id = part.get('id', 'N/A')
        print(f"   Line {part['line_number']}: {indent_str}{part['type']} {part_id} - {part['description'][:50]}...")
    
    # Verify all IDs are integers >= 1000
    print("\n🔍 Verifying all IDs:")
    for part in parts:
        if part['type'] in ['REQUIREMENT', 'COMMENT', 'DATTR']:
            part_id = part.get('id')
            assert isinstance(part_id, int), f"{part['type']} ID should be integer, got {type(part_id)}"
            assert part_id >= 1000, f"{part['type']} ID should be >= 1000, got {part_id}"
            print(f"   ✅ {part['type']} ID {part_id} is correct")
    
    print("\n🎉 All IDs are correct integer values >= 1000!")

def main():
    """Run practical test."""
    print("=" * 60)
    print("🧪 PRACTICAL TEST: NEW DOCUMENT WITH INTEGER IDs")
    print("=" * 60)
    
    try:
        test_practical_new_document()
        
        print("\n" + "=" * 60)
        print("🎉 PRACTICAL TEST PASSED!")
        print("✅ All new items use integer IDs starting from 1000")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
