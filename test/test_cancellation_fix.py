#!/usr/bin/env python3
"""
Test the saveas cancellation behavior to ensure editor doesn't exit.
"""

import sys
import os
import tempfile
import shutil
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_saveas_cancellation_behavior():
    """Test that cancelling a saveas operation doesn't exit the editor."""
    print("🧪 Testing saveas cancellation behavior...")
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()
    
    try:
        os.chdir(test_dir)
        
        # Initialize terminal editor and create a new document
        editor = TerminalEditor()
        editor._create_new_document()
        
        # Create a test file that already exists
        test_filename = "existing_file.md"
        with open(test_filename, 'w') as f:
            f.write("# Existing content\n")
        
        print(f"✅ Created test file: {test_filename}")
        
        # Test 1: Cancel overwrite prompt should return True (continue editing)
        print("\n📋 Test 1: Cancel overwrite with 'n'")
        with patch('builtins.input', return_value='n'):
            result = editor._process_command("saveas", ["existing_file.md"])
        
        if result:
            print("   ✅ PASS: Command returned True (editor continues)")
        else:
            print("   ❌ FAIL: Command returned False (would exit editor)")
            return False
        
        # Test 2: Cancel overwrite prompt with empty response should return True
        print("\n📋 Test 2: Cancel overwrite with empty response")
        with patch('builtins.input', return_value=''):
            result = editor._process_command("saveas", ["existing_file"])  # Will be extended to .md
        
        if result:
            print("   ✅ PASS: Command returned True (editor continues)")
        else:
            print("   ❌ FAIL: Command returned False (would exit editor)")
            return False
        
        # Test 3: Accept overwrite should also return True
        print("\n📋 Test 3: Accept overwrite with 'y'")
        with patch('builtins.input', return_value='y'):
            result = editor._process_command("saveas", ["existing_file.md"])
        
        if result:
            print("   ✅ PASS: Command returned True (editor continues)")
        else:
            print("   ❌ FAIL: Command returned False (would exit editor)")
            return False
        
        # Test 4: Save command with no filename should return True (show error but continue)
        print("\n📋 Test 4: Save command with no filename")
        result = editor._process_command("save", [])
        
        if result:
            print("   ✅ PASS: Command returned True (editor continues)")
        else:
            print("   ❌ FAIL: Command returned False (would exit editor)")
            return False
        
        print("\n🎉 All cancellation behavior tests passed!")
        print("✅ Editor will continue running after save cancellations")
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

if __name__ == "__main__":
    if test_saveas_cancellation_behavior():
        print("\n🎯 SUCCESS: Saveas cancellation behavior is correct!")
        print("💡 The terminal editor will NOT exit when user cancels save operations.")
    else:
        print("\n💥 FAILURE: Saveas cancellation behavior needs fixing!")
