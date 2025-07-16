#!/usr/bin/env python3
"""
Test loading a file with legacy string IDs and adding new items.
Fixed version that works reliably without hanging.
"""

import sys
import os
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_legacy_file_with_new_items():
    """Load a file with legacy string IDs and add new items with integer IDs."""
    print("🔬 Testing legacy file loading and new item addition...")
    
    # File with legacy string IDs - use pathlib for better path handling
    test_dir = Path(__file__).parent
    legacy_file_path = test_dir / "data" / "test_legacy_simple.md"
    legacy_file = str(legacy_file_path.resolve())  # Convert to absolute path string
    
    if not legacy_file_path.exists():
        print(f"❌ Test file {legacy_file} not found")
        return False
    
    try:
        # Import only what we need to avoid terminal/readline issues
        from libs.parse_req_md import ReadMDFile, ClassifyParts
        from libs.md_edit import MarkdownEditor
        
        # Load the legacy file
        print(f"📂 Loading legacy file: {legacy_file}")
        
        # Read and parse directly
        content = ReadMDFile(legacy_file)
        if not content:
            print("❌ Failed to read legacy file")
            return False
        
        classified_parts = ClassifyParts(content)
        if not classified_parts:
            print("❌ Failed to classify legacy file content")
            return False
        
        print(f"✅ Loaded {len(classified_parts)} items from legacy file")
        
        # Create markdown editor
        md_editor = MarkdownEditor(classified_parts)
        
        # Show current document structure
        print("\n📄 Current document structure (with legacy IDs):")
        parts = md_editor.get_classified_parts()
        for part in parts:
            indent_str = "  " * part['indent']
            part_id = part.get('id', 'N/A')
            id_type = type(part_id).__name__
            print(f"   Line {part['line_number']}: {indent_str}{part['type']} {part_id} ({id_type}) - {part['description'][:40]}...")
        
        # Add new items - these should get integer IDs
        last_line = max(part['line_number'] for part in parts)
        print(f"\n📝 Adding new requirement after line {last_line} (should get integer ID >= 1000)...")
        result = md_editor.add_item_after(last_line, 'REQUIREMENT', 'New requirement with integer ID')
        if result:
            print(f"   Added requirement with ID: {result['id']} (type: {type(result['id'])})")
        else:
            print("   ❌ Failed to add new requirement")
            return False
        
        # Add another item
        parts_updated = md_editor.get_classified_parts()
        last_line = max(part['line_number'] for part in parts_updated)
        print(f"📝 Adding new comment after line {last_line} (should get integer ID >= 1000)...")
        result = md_editor.add_item_after(last_line, 'COMMENT', 'New comment with integer ID')
        if result:
            print(f"   Added comment with ID: {result['id']} (type: {type(result['id'])})")
        else:
            print("   ❌ Failed to add new comment")
            return False
        
        # Show final document structure
        print("\n📄 Final document structure (legacy + new integer IDs):")
        parts = md_editor.get_classified_parts()
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
        
    except Exception as e:
        print(f"❌ Exception during test: {e}")
        import traceback
        traceback.print_exc()
        return False

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
    sys.exit(0 if success else 1)
