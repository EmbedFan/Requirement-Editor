#!/usr/bin/env python3
"""
Test legacy file functionality without terminal editor (avoiding readline issues)
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_legacy_file_parsing_only():
    """Test just the file parsing without terminal editor."""
    print("🧪 Testing legacy file parsing (no terminal editor)...")
    
    # Find the legacy file
    test_dir = Path(__file__).parent
    legacy_file = test_dir / "data" / "test_legacy_simple.md"
    
    if not legacy_file.exists():
        print(f"❌ Test file not found: {legacy_file}")
        return False
    
    print(f"📂 Loading legacy file: {legacy_file}")
    
    # Import only the parsing modules
    from libs.parse_req_md import ReadMDFile, ClassifyParts
    from libs.md_edit import MarkdownEditor
    
    # Read and parse the file
    content = ReadMDFile(str(legacy_file))
    if not content:
        print("❌ Failed to read file")
        return False
    
    print(f"✅ Read {len(content)} characters")
    
    # Classify the content
    classified_parts = ClassifyParts(content)
    if not classified_parts:
        print("❌ Failed to classify content")
        return False
    
    print(f"✅ Classified {len(classified_parts)} parts")
    
    # Show current document structure
    print("\n📄 Document structure with legacy IDs:")
    for part in classified_parts:
        indent_str = "  " * part['indent']
        part_id = part.get('id', 'N/A')
        id_type = type(part_id).__name__
        print(f"   Line {part['line_number']}: {indent_str}{part['type']} {part_id} ({id_type}) - {part['description'][:40]}...")
    
    # Create MarkdownEditor and test adding new items
    md_editor = MarkdownEditor(classified_parts)
    
    # Add a new requirement (should get integer ID >= 1000)
    parts = md_editor.get_classified_parts()
    last_line = max(part['line_number'] for part in parts)
    
    print(f"\n📝 Adding new requirement after line {last_line}...")
    result = md_editor.add_item_after(last_line, 'REQUIREMENT', 'New requirement with integer ID')
    if result:
        print(f"   ✅ Added requirement with ID: {result['id']} (type: {type(result['id'])})")
    else:
        print("   ❌ Failed to add requirement")
        return False
    
    # Verify the ID is an integer >= 1000
    if isinstance(result['id'], int) and result['id'] >= 1000:
        print("   ✅ New requirement has correct integer ID >= 1000")
    else:
        print(f"   ❌ New requirement ID is incorrect: {result['id']}")
        return False
    
    print("🎉 Legacy file parsing and new ID generation test PASSED!")
    return True

if __name__ == "__main__":
    try:
        success = test_legacy_file_parsing_only()
        if success:
            print("\n✅ Test completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Test failed!")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
