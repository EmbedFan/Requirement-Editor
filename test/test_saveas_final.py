#!/usr/bin/env python3
"""
Final verification test for the saveas command filename processing integration.

This test verifies that all the required functionality is working:
1. Auto-extension of filenames without .md
2. Warning and conversion of non-.md extensions to .md 
3. Overwrite confirmation for existing files
4. Integration with the terminal editor's saveas command
"""

import sys
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_saveas_requirements():
    """Test all the saveas requirements."""
    print("🧪 Final Verification: Saveas Filename Processing")
    print("=" * 60)
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()
    
    try:
        os.chdir(test_dir)
        
        # Initialize terminal editor and create a new document
        editor = TerminalEditor()
        editor._create_new_document()
        
        print("✅ Document created successfully")
        
        # Test 1: Filename without extension
        print("\n📋 Test 1: Filename without .md extension")
        print("   Input: 'my_requirements'")
        print("   Expected: Auto-extend to 'my_requirements.md'")
        
        # Mock user input to avoid interactive prompts
        with patch('builtins.input', return_value=''):
            result = editor._process_command("saveas", ["my_requirements"])
        
        if result and os.path.exists("my_requirements.md"):
            print("   ✅ PASS: File auto-extended to .md")
        else:
            print("   ❌ FAIL: Auto-extension failed")
            return False
        
        # Test 2: Wrong extension conversion
        print("\n📋 Test 2: Wrong extension conversion")
        print("   Input: 'my_doc.txt'")
        print("   Expected: Warning and change to 'my_doc.md'")
        
        with patch('builtins.input', return_value=''):
            result = editor._process_command("saveas", ["my_doc.txt"])
        
        if result and os.path.exists("my_doc.md"):
            print("   ✅ PASS: Extension changed from .txt to .md")
        else:
            print("   ❌ FAIL: Extension conversion failed")
            return False
        
        # Test 3: Correct extension (no change needed)
        print("\n📋 Test 3: Correct .md extension")
        print("   Input: 'correct_doc.md'")
        print("   Expected: No warning, save as-is")
        
        with patch('builtins.input', return_value=''):
            result = editor._process_command("saveas", ["correct_doc.md"])
        
        if result and os.path.exists("correct_doc.md"):
            print("   ✅ PASS: Correct extension handled properly")
        else:
            print("   ❌ FAIL: Correct extension handling failed")
            return False
        
        # Test 4: Overwrite confirmation (decline)
        print("\n📋 Test 4: Overwrite confirmation (decline)")
        print("   Input: 'my_requirements' (file exists)")
        print("   User response: 'n' (decline)")
        print("   Expected: Save cancelled")
        
        with patch('builtins.input', return_value='n'):
            result = editor._process_command("saveas", ["my_requirements"])
        
        if not result:  # Should return False when user declines
            print("   ✅ PASS: Overwrite declined correctly")
        else:
            print("   ❌ FAIL: Overwrite decline not handled")
            return False
        
        # Test 5: Overwrite confirmation (accept)
        print("\n📋 Test 5: Overwrite confirmation (accept)")
        print("   Input: 'my_requirements' (file exists)")
        print("   User response: 'y' (accept)")
        print("   Expected: File overwritten")
        
        with patch('builtins.input', return_value='y'):
            result = editor._process_command("saveas", ["my_requirements"])
        
        if result and os.path.exists("my_requirements.md"):
            print("   ✅ PASS: Overwrite accepted and file saved")
        else:
            print("   ❌ FAIL: Overwrite accept not handled")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 ALL SAVEAS REQUIREMENTS VERIFIED SUCCESSFULLY!")
        print("=" * 60)
        
        # List created files for verification
        print("\n📁 Files created during test:")
        for file in os.listdir('.'):
            if file.endswith('.md') or file.endswith('.json'):
                print(f"   - {file}")
        
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
    if test_saveas_requirements():
        print("\n🎯 SUCCESS: All saveas requirements implemented and verified!")
    else:
        print("\n💥 FAILURE: Some requirements not met!")
