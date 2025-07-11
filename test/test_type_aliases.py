#!/usr/bin/env python3
"""
Test script for type aliases functionality.

This script tests:
1. Using short aliases in add commands (TIT, SUB, REQ, COM)
2. Using short aliases in type commands
3. Verifying that aliases are converted to full type names
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_type_aliases():
    """Test the type aliases functionality."""
    print("🧪 Testing type aliases functionality...")
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()
    
    try:
        os.chdir(test_dir)
        
        # Initialize terminal editor and create a new document
        editor = TerminalEditor()
        editor._create_new_document()
        
        print("✅ Created new document")
        
        # Test 1: Add items using aliases
        print("\n📋 Test 1: Adding items with aliases")
        
        # Test TIT (TITLE)
        result = editor._process_command("add", ["after", "1", "TIT", "Main Title Using Alias"])
        if result:
            print("   ✅ Added TIT (should become TITLE)")
        else:
            print("   ❌ Failed to add TIT")
            return False
        
        # Test SUB (SUBTITLE)
        result = editor._process_command("add", ["after", "2", "SUB", "Subtitle Using Alias"])
        if result:
            print("   ✅ Added SUB (should become SUBTITLE)")
        else:
            print("   ❌ Failed to add SUB")
            return False
        
        # Test REQ (REQUIREMENT)
        result = editor._process_command("add", ["after", "3", "REQ", "Requirement Using Alias"])
        if result:
            print("   ✅ Added REQ (should become REQUIREMENT)")
        else:
            print("   ❌ Failed to add REQ")
            return False
        
        # Test COM (COMMENT)
        result = editor._process_command("add", ["after", "4", "COM", "Comment Using Alias"])
        if result:
            print("   ✅ Added COM (should become COMMENT)")
        else:
            print("   ❌ Failed to add COM")
            return False
        
        # Test 2: Verify types were converted correctly
        print("\n📋 Test 2: Verifying type conversion")
        
        parts = editor.md_editor.get_classified_parts()
        
        # Check that aliases were converted to full names
        expected_types = ['TITLE', 'DATTR', 'COMMENT', 'REQUIREMENT', 'TITLE', 'SUBTITLE', 'REQUIREMENT', 'COMMENT']
        
        for i, part in enumerate(parts):
            expected_type = expected_types[i]
            actual_type = part['type']
            
            if actual_type == expected_type:
                print(f"   ✅ Line {i+1}: {actual_type} (correct)")
            else:
                print(f"   ❌ Line {i+1}: Expected {expected_type}, got {actual_type}")
                return False
        
        # Test 3: Test type command with aliases
        print("\n📋 Test 3: Testing type command with aliases")
        
        # Change line 6 (SUBTITLE) to REQ (REQUIREMENT)
        result = editor._process_command("type", ["6", "REQ"])
        if result:
            print("   ✅ Changed SUBTITLE to REQ using alias")
        else:
            print("   ❌ Failed to change type using alias")
            return False
        
        # Verify the change
        parts = editor.md_editor.get_classified_parts()
        line_6_type = parts[5]['type']  # 0-indexed
        if line_6_type == 'REQUIREMENT':
            print("   ✅ Type change verified: SUB -> REQ -> REQUIREMENT")
        else:
            print(f"   ❌ Type change failed: expected REQUIREMENT, got {line_6_type}")
            return False
        
        # Test 4: Test full names still work
        print("\n📋 Test 4: Testing full names still work")
        
        result = editor._process_command("add", ["after", "8", "COMMENT", "Full name comment"])
        if result:
            print("   ✅ Full type name COMMENT still works")
        else:
            print("   ❌ Full type name failed")
            return False
        
        # Test 5: Display document to see final result
        print("\n📋 Test 5: Final document structure")
        editor.display_document()
        
        print("\n🎉 All type alias tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Clean up
        os.chdir(original_cwd)
        shutil.rmtree(test_dir, ignore_errors=True)

def test_normalization_function():
    """Test the _normalize_item_type function directly."""
    print("\n🧪 Testing _normalize_item_type function...")
    
    editor = TerminalEditor()
    
    test_cases = [
        # (input, expected_output)
        ('TIT', 'TITLE'),
        ('tit', 'TITLE'),
        ('SUB', 'SUBTITLE'),
        ('sub', 'SUBTITLE'),
        ('REQ', 'REQUIREMENT'),
        ('req', 'REQUIREMENT'),
        ('COM', 'COMMENT'),
        ('com', 'COMMENT'),
        ('TITLE', 'TITLE'),  # Full names should pass through
        ('SUBTITLE', 'SUBTITLE'),
        ('REQUIREMENT', 'REQUIREMENT'),
        ('COMMENT', 'COMMENT'),
        ('DATTR', 'DATTR'),  # No alias for DATTR
        ('UNKNOWN', 'UNKNOWN'),  # Unknown types pass through
    ]
    
    all_passed = True
    for input_type, expected in test_cases:
        result = editor._normalize_item_type(input_type)
        if result == expected:
            print(f"   ✅ '{input_type}' -> '{result}'")
        else:
            print(f"   ❌ '{input_type}' -> '{result}' (expected '{expected}')")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🚀 Type Aliases Test Suite")
    print("=" * 50)
    
    # Test the normalization function
    norm_test = test_normalization_function()
    
    # Test the full integration
    integration_test = test_type_aliases()
    
    print("\n" + "=" * 50)
    if norm_test and integration_test:
        print("🎯 SUCCESS: All type alias tests passed!")
        print("💡 Users can now use TIT, SUB, REQ, COM as shortcuts!")
    else:
        print("💥 FAILURE: Some type alias tests failed!")
