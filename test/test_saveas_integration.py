#!/usr/bin/env python3
"""
Test script for the saveas command with filename processing integration.

This script tests:
1. Filename extension handling (auto-adding .md)
2. Extension conversion (changing non-.md to .md)
3. Overwrite confirmation for existing files
"""

import os
import sys
import tempfile
import shutil
from unittest.mock import patch

# Add the libs directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_saveas_filename_processing():
    """Test the saveas command with various filename scenarios."""
    print("🧪 Testing saveas command with filename processing...")
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()
    
    try:
        os.chdir(test_dir)
        
        # Initialize terminal editor
        editor = TerminalEditor()
        
        # Create a new document
        editor._create_new_document()
        
        print("\n📝 Test 1: Filename without extension")
        # Test saving with filename without extension
        with patch('builtins.input', return_value=''):
            result = editor._save_file("test_doc")
        print(f"✅ Result: {result}")
        
        # Check if file was created with .md extension
        expected_file = "test_doc.md"
        if os.path.exists(expected_file):
            print(f"✅ File created successfully: {expected_file}")
        else:
            print(f"❌ File not found: {expected_file}")
        
        print("\n📝 Test 2: Filename with wrong extension")
        # Test saving with wrong extension
        with patch('builtins.input', return_value=''):
            result = editor._save_file("test_doc2.txt")
        print(f"✅ Result: {result}")
        
        # Check if file was created with .md extension
        expected_file2 = "test_doc2.md"
        if os.path.exists(expected_file2):
            print(f"✅ File created successfully: {expected_file2}")
        else:
            print(f"❌ File not found: {expected_file2}")
        
        print("\n📝 Test 3: Overwrite confirmation (decline)")
        # Test overwrite confirmation - decline
        with patch('builtins.input', return_value='n'):
            result = editor._save_file("test_doc")  # This should already exist
        print(f"✅ Result (should be False): {result}")
        
        print("\n📝 Test 4: Overwrite confirmation (accept)")
        # Test overwrite confirmation - accept
        with patch('builtins.input', return_value='y'):
            result = editor._save_file("test_doc")  # This should already exist
        print(f"✅ Result (should be True): {result}")
        
        print("\n📝 Test 5: Correct .md extension (no processing needed)")
        # Test with correct .md extension
        with patch('builtins.input', return_value=''):
            result = editor._save_file("test_doc3.md")
        print(f"✅ Result: {result}")
        
        # Check if file was created
        expected_file3 = "test_doc3.md"
        if os.path.exists(expected_file3):
            print(f"✅ File created successfully: {expected_file3}")
        else:
            print(f"❌ File not found: {expected_file3}")
            
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up
        os.chdir(original_cwd)
        shutil.rmtree(test_dir, ignore_errors=True)

if __name__ == "__main__":
    test_saveas_filename_processing()
