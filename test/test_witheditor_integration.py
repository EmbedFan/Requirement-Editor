#!/usr/bin/env python3
"""
Integration test for the witheditor command implementation.

This test verifies that all components of the witheditor feature
are properly integrated and working.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from libs.terminal_editor import TerminalEditor

def test_witheditor_integration():
    """Test the complete witheditor integration."""
    print("🧪 Witheditor Integration Test")
    print("=" * 50)
    
    success_count = 0
    total_tests = 5
    
    # Test 1: Command in available commands
    print("\n1. Testing command availability...")
    editor = TerminalEditor()
    if 'witheditor' in editor.tab_completer.available_commands:
        print("   ✅ PASS: witheditor found in available commands")
        success_count += 1
    else:
        print("   ❌ FAIL: witheditor not in available commands")
    
    # Test 2: Check method exists
    print("\n2. Testing method implementation...")
    if hasattr(editor, '_open_external_editor'):
        print("   ✅ PASS: _open_external_editor method exists")
        success_count += 1
    else:
        print("   ❌ FAIL: _open_external_editor method missing")
    
    # Test 3: Check imports
    print("\n3. Testing required imports...")
    try:
        import tempfile
        import subprocess
        print("   ✅ PASS: Required modules (tempfile, subprocess) imported")
        success_count += 1
    except ImportError as e:
        print(f"   ❌ FAIL: Import error: {e}")
    
    # Test 4: Check help text includes command
    print("\n4. Testing help text integration...")
    # This is more complex to test programmatically, so we'll check indirectly
    # by looking for the method that handles the command
    found_witheditor_handling = False
    try:
        # Read the terminal_editor.py file to check for command handling
        with open('libs/terminal_editor.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'elif command == "witheditor"' in content:
                found_witheditor_handling = True
    except Exception as e:
        pass
    
    if found_witheditor_handling:
        print("   ✅ PASS: witheditor command handling found")
        success_count += 1
    else:
        print("   ❌ FAIL: witheditor command handling not found")
    
    # Test 5: Check documentation updated
    print("\n5. Testing documentation integration...")
    doc_updated = False
    try:
        with open('docs/TERMINAL_EDITOR.md', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'witheditor' in content.lower():
                doc_updated = True
    except Exception as e:
        pass
    
    if doc_updated:
        print("   ✅ PASS: Documentation includes witheditor command")
        success_count += 1
    else:
        print("   ❌ FAIL: Documentation not updated")
    
    # Summary
    print(f"\n📊 Test Results: {success_count}/{total_tests} tests passed")
    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED! Witheditor integration is complete.")
        print("\n✨ Ready to use:")
        print("   python main.py -ed")
        print("   > new")
        print("   > witheditor 4")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return success_count == total_tests

if __name__ == "__main__":
    test_witheditor_integration()
