#!/usr/bin/env python3
"""
Test to verify that all new items get integer IDs starting from 1000,
even when loading documents with legacy string-based IDs.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor
from libs.parse_req_md import ReadMDFile, ClassifyParts
from libs.md_edit import MarkdownEditor

def test_id_generation_with_legacy_data():
    """Test that new IDs start from 1000 even with legacy string IDs in the document."""
    print("🔬 Testing ID generation with legacy string-based IDs...")
    
    # Create a document with legacy string-based IDs to simulate the problem
    legacy_parts = [
        {
            'line_number': 1,
            'original_line': '# Test Document',
            'type': 'TITLE',
            'indent': 0,
            'id': None,
            'description': 'Test Document',
            'parent': None,
            'children': [2, 3, 4],
            'children_refs': []
        },
        {
            'line_number': 2,
            'original_line': 'DATTR001 Dattr: Created at: 2025-07-11 18:52 Modified at: 2025-07-11 18:54',
            'type': 'DATTR',
            'indent': 1,
            'id': 'DATTR001',  # Legacy string ID
            'description': 'Created at: 2025-07-11 18:52 Modified at: 2025-07-11 18:54',
            'parent': 1,
            'children': [],
            'children_refs': []
        },
        {
            'line_number': 3,
            'original_line': 'REQ001 Req: System shall work',
            'type': 'REQUIREMENT',
            'indent': 1,
            'id': 'REQ001',  # Legacy string ID
            'description': 'System shall work',
            'parent': 1,
            'children': [],
            'children_refs': []
        },
        {
            'line_number': 4,
            'original_line': 'COMM001 Comm: This is a comment',
            'type': 'COMMENT',
            'indent': 1,
            'id': 'COMM001',  # Legacy string ID
            'description': 'This is a comment',
            'parent': 1,
            'children': [],
            'children_refs': []
        }
    ]
    
    # Create editor with legacy data
    md_editor = MarkdownEditor(legacy_parts)
    
    # Test MarkdownEditor ID generation directly
    print("🧪 Testing MarkdownEditor._get_next_item_id()...")
    next_req_id = md_editor._get_next_item_id('REQUIREMENT')
    next_comm_id = md_editor._get_next_item_id('COMMENT')
    next_dattr_id = md_editor._get_next_item_id('DATTR')
    
    print(f"   Next REQUIREMENT ID: {next_req_id}")
    print(f"   Next COMMENT ID: {next_comm_id}")
    print(f"   Next DATTR ID: {next_dattr_id}")
    
    # Verify all IDs start from 1000
    assert next_req_id >= 1000, f"REQUIREMENT ID should be >= 1000, got {next_req_id}"
    assert next_comm_id >= 1000, f"COMMENT ID should be >= 1000, got {next_comm_id}"
    assert next_dattr_id >= 1000, f"DATTR ID should be >= 1000, got {next_dattr_id}"
    
    print("✅ All IDs are >= 1000 as expected")
    
    # Test adding new items
    print("🧪 Testing add operations with legacy data...")
    
    # Add a new requirement
    new_req = md_editor.add_item_after(3, 'REQUIREMENT', 'New requirement after legacy one')
    print(f"   Added REQUIREMENT with ID: {new_req['id']}")
    assert new_req['id'] >= 1000, f"New REQUIREMENT ID should be >= 1000, got {new_req['id']}"
    
    # Add a new comment
    new_comm = md_editor.add_item_after(4, 'COMMENT', 'New comment after legacy one')
    print(f"   Added COMMENT with ID: {new_comm['id']}")
    assert new_comm['id'] >= 1000, f"New COMMENT ID should be >= 1000, got {new_comm['id']}"
    
    # Add a new DATTR
    new_dattr = md_editor.add_item_after(2, 'DATTR', 'New DATTR after legacy one')
    print(f"   Added DATTR with ID: {new_dattr['id']}")
    assert new_dattr['id'] >= 1000, f"New DATTR ID should be >= 1000, got {new_dattr['id']}"
    
    print("✅ All new items have integer IDs >= 1000")

def test_terminal_editor_integration():
    """Test that terminal editor also generates correct IDs."""
    print("🔬 Testing terminal editor integration...")
    
    # Create terminal editor with new document
    editor = TerminalEditor()
    editor._create_new_document()
    
    # Test the terminal editor's ID generation
    next_id = editor._get_next_available_id()
    print(f"   Terminal editor next ID: {next_id}")
    assert next_id >= 1000, f"Terminal editor ID should be >= 1000, got {next_id}"
    
    # The new document should have integer IDs starting from 1000
    parts = editor.md_editor.get_classified_parts()
    for part in parts:
        if part['type'] in ['REQUIREMENT', 'COMMENT', 'DATTR']:
            part_id = part.get('id')
            print(f"   {part['type']} has ID: {part_id} (type: {type(part_id)})")
            assert isinstance(part_id, int), f"{part['type']} ID should be integer, got {type(part_id)}"
            assert part_id >= 1000, f"{part['type']} ID should be >= 1000, got {part_id}"
    
    print("✅ Terminal editor creates documents with correct integer IDs")

def main():
    """Run all ID fix tests."""
    print("=" * 60)
    print("🧪 TESTING INTEGER ID FIX FOR LEGACY STRING IDs")
    print("=" * 60)
    
    try:
        test_id_generation_with_legacy_data()
        print()
        test_terminal_editor_integration()
        
        print()
        print("=" * 60)
        print("🎉 ALL ID FIX TESTS PASSED!")
        print("✅ New items will now use integer IDs starting from 1000")
        print("✅ Even when loading documents with legacy string IDs")
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
