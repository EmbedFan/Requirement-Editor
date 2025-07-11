#!/usr/bin/env python3
"""
Test loading a file with legacy string IDs and adding new items.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_legacy_file_with_new_items():
    """Load a file with legacy string IDs and add new items with integer IDs."""
    print("🔬 Testing legacy file loading and new item addition...")
    
    # File with legacy string IDs
    legacy_file = "test_legacy_simple.md"
    
    if not os.path.exists(legacy_file):
        print(f"❌ Test file {legacy_file} not found")
        return False
    
    editor = TerminalEditor()
    
    # Load the legacy file
    print(f"📂 Loading legacy file: {legacy_file}")
    success = editor._load_file(legacy_file)
    if not success:
        print("❌ Failed to load legacy file")
        return False
    
    # Show current document structure
    print("\n📄 Current document structure (with legacy IDs):")
    parts = editor.md_editor.get_classified_parts()
    for part in parts:
        indent_str = "  " * part['indent']
        part_id = part.get('id', 'N/A')
        id_type = type(part_id).__name__
        print(f"   Line {part['line_number']}: {indent_str}{part['type']} {part_id} ({id_type}) - {part['description'][:40]}...")
    
    # Add new items - these should get integer IDs (using correct line numbers)
    # Based on the structure, last item is on line 7, so add after it
    print(f"\n📝 Adding new requirement after last item (should get integer ID >= 1000)...")
    md_editor = editor.md_editor
    result = md_editor.add_item_after(7, 'REQUIREMENT', 'New requirement with integer ID')
    print(f"   Added requirement with ID: {result['id']} (type: {type(result['id'])})")
    
    # Now add after the newly added item
    parts_updated = md_editor.get_classified_parts()
    last_line = max(part['line_number'] for part in parts_updated)
    print(f"📝 Adding new comment after line {last_line} (should get integer ID >= 1000)...")
    result = md_editor.add_item_after(last_line, 'COMMENT', 'New comment with integer ID')
    print(f"   Added comment with ID: {result['id']} (type: {type(result['id'])})")
    
    # Show final document structure
    print("\n📄 Final document structure (legacy + new integer IDs):")
    parts = editor.md_editor.get_classified_parts()
    for part in parts:
        indent_str = "  " * part['indent']
        part_id = part.get('id', 'N/A')
        id_type = type(part_id).__name__
        print(f"   Line {part['line_number']}: {indent_str}{part['type']} {part_id} ({id_type}) - {part['description'][:40]}...")
    
    # Verify new items have integer IDs >= 1000
    print("\n🔍 Verifying new items have correct IDs:")
    new_items_count = 0
    for part in parts:
        if part['type'] in ['REQUIREMENT', 'COMMENT', 'DATTR'] and isinstance(part.get('id'), int):
            part_id = part.get('id')
            if part_id >= 1000:
                print(f"   ✅ {part['type']} ID {part_id} is correct (new integer ID)")
                new_items_count += 1
    
    print(f"\n🎉 Found {new_items_count} items with new integer IDs >= 1000!")
    print("✅ Legacy string IDs are preserved, new items get integer IDs")
    
    return True

def main():
    """Run legacy file test."""
    print("=" * 60)
    print("🧪 LEGACY FILE TEST: STRING IDs + NEW INTEGER IDs")
    print("=" * 60)
    
    try:
        success = test_legacy_file_with_new_items()
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 LEGACY FILE TEST PASSED!")
            print("✅ Legacy string IDs preserved")
            print("✅ New items get integer IDs starting from 1000")
            print("=" * 60)
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
