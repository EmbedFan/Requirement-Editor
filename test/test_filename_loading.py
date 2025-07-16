#!/usr/bin/env python3
"""
Test script to verify filename processing for loading files.
"""

import os
import sys
import tempfile

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_filename_processing():
    """Test the filename processing functionality."""
    
    print("🧪 Testing Filename Processing for File Loading")
    print("=" * 60)
    
    editor = TerminalEditor()
    
    # Test cases
    test_cases = [
        # (input_filename, expected_result_description)
        ("test/data/test_input", "Should find test_input.md"),
        ("test/data/test_input.md", "Should find exact match"),
        ("test/data/nonexistent", "Should return None"),
        ("test/data/test_input.txt", "Should try test_input.md"),
    ]
    
    for input_file, description in test_cases:
        print(f"\n📝 Testing: '{input_file}'")
        print(f"   Expected: {description}")
        
        result = editor._process_filename_for_loading(input_file)
        
        if result:
            print(f"   ✅ Result: Found '{result}'")
        else:
            print(f"   ❌ Result: No file found")
    
    print(f"\n{'='*60}")
    print("Test completed!")

if __name__ == "__main__":
    test_filename_processing()
