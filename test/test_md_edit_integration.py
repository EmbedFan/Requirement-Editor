#!/usr/bin/env python3
"""
Integration test for the md_edit.py module using the existing test data.
Updated to work with the line number-based API.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'libs'))

from parse_req_md import ReadMDFile, ClassifyParts
from md_edit import MarkdownEditor


def test_with_real_data():
    """Test the editor with real test data using line numbers."""
    print("🧪 Testing with Real Test Data...")
    
    # Read the existing test file
    test_file = os.path.join(os.path.dirname(__file__), "data", "test_input.md")
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return False
    
    content = ReadMDFile(test_file)
    if not content:
        print("❌ Failed to read test file")
        return False
    
    print(f"✅ Read {len(content)} characters from {test_file}")
    
    # Parse the content
    classified_parts = ClassifyParts(content)
    if not classified_parts:
        print("❌ Failed to parse test file")
        return False
    
    print(f"✅ Parsed {len(classified_parts)} parts from test file")
    
    # Create editor
    editor = MarkdownEditor(classified_parts)
    
    # List all items to see what we're working with
    items = editor.list_all_items()
    print(f"✅ Created editor with {len(items)} items")
    
    # Find some requirements to work with
    req_lines = []
    for item in items:
        if item['type'] == 'REQUIREMENT' and item['item_id']:
            req_lines.append((item['line_number'], item['item_id']))
    
    if req_lines:
        print(f"✅ Found {len(req_lines)} requirements")
        
        # Test operations with the first requirement
        first_req_line, first_req_id = req_lines[0]
        print(f"Working with requirement {first_req_id} at line {first_req_line}")
        
        # Test adding a new requirement after it
        new_req = editor.add_item_after(first_req_line, 'REQUIREMENT', 
                                       'Test integration requirement', 9999)
        print(f"✅ Added new requirement at line {new_req['line_number']}")
        
        # Test adding a comment under the original requirement
        new_comment = editor.add_item_under(first_req_line, 'COMMENT', 
                                           'Test integration comment', 8888)
        print(f"✅ Added new comment at line {new_comment['line_number']}")
        
        # Test content operations
        original_content = editor.get_content(first_req_line)
        print(f"✅ Original content: {original_content[:50]}...")
        
        # Test updating content
        updated = editor.update_content(first_req_line, original_content + " [UPDATED]")
        if updated:
            new_content = editor.get_content(first_req_line)
            print(f"✅ Updated content: {new_content[:50]}...")
        
        # Test hierarchical operations
        children = editor.get_children(first_req_line)
        print(f"✅ Requirement has {len(children)} children: {children}")
        
        # Test search operations
        search_results = editor.find_by_description('test', case_sensitive=False)
        print(f"✅ Found {len(search_results)} items containing 'test'")
        
        return True
    else:
        print("❌ No requirements found in test file")
        return False


def test_complex_operations():
    """Test more complex editing operations with real data."""
    print("\n🔧 Testing Complex Operations...")
    
    test_file = os.path.join(os.path.dirname(__file__), "data", "test_input.md")
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return False
    
    content = ReadMDFile(test_file)
    classified_parts = ClassifyParts(content)
    editor = MarkdownEditor(classified_parts)
    
    # Get initial state
    initial_items = editor.list_all_items()
    print(f"Initial state: {len(initial_items)} items")
    
    # Find a requirement to work with
    req_line = None
    for item in initial_items:
        if item['type'] == 'REQUIREMENT' and item['item_id']:
            req_line = item['line_number']
            break
    
    if not req_line:
        print("❌ No requirements found for complex operations")
        return False
    
    # Test moving operations
    # First add a new requirement to move around
    new_req = editor.add_item_after(req_line, 'REQUIREMENT', 'Mobile requirement', 7777)
    new_req_line = new_req['line_number']
    
    # Now try moving it to different positions
    success = editor.move_item_before(new_req_line, req_line)
    if success:
        print("✅ Successfully moved requirement before original")
    
    # Test type changes
    comment_lines = [item['line_number'] for item in editor.list_all_items() 
                    if item['type'] == 'COMMENT']
    if comment_lines:
        first_comment = comment_lines[0]
        success = editor.change_item_type(first_comment, 'REQUIREMENT', 6666)
        if success:
            print("✅ Successfully changed comment to requirement")
    
    # Test deletion
    items_before = len(editor.list_all_items())
    if comment_lines and len(comment_lines) > 1:
        editor.delete_item(comment_lines[1], delete_children=True)
        items_after = len(editor.list_all_items())
        print(f"✅ Deleted item: {items_before} -> {items_after} items")
    
    return True


def run_integration_tests():
    """Run all integration test suites."""
    print("🚀 Starting md_edit.py Integration Tests (Line Number-Based)\n")
    
    tests = [
        test_with_real_data,
        test_complex_operations
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✅ PASSED\n")
            else:
                failed += 1
                print("❌ FAILED\n")
        except Exception as e:
            failed += 1
            print(f"❌ FAILED with exception: {e}\n")
    
    print(f"📊 Integration Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All integration tests passed!")
        return True
    else:
        print("⚠️ Some integration tests failed.")
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
