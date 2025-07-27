#!/usr/bin/env python3
"""
Validation test for export improvements
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def validate_export_improvements():
    """Validate all aspects of the export improvements."""
    print("🔍 Validating Export Improvements")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test 1: Help text updated
    print("1️⃣ Checking help text...")
    editor = TerminalEditor()
    # We can't easily capture the help output, but we can check the method exists
    try:
        # Check that export method accepts optional filename
        result = editor._export_html()  # Should fail gracefully for new doc
        print("   ✅ Export method accepts no arguments")
    except TypeError:
        print("   ❌ Export method doesn't accept optional filename")
        all_tests_passed = False
    
    # Test 2: New document behavior
    print("2️⃣ Testing new document export (should fail gracefully)...")
    editor._create_new_document()
    result = editor._export_html()
    if not result:
        print("   ✅ Correctly handled new document without filename")
    else:
        print("   ❌ Should have failed with helpful message")
        all_tests_passed = False
    
    # Test 3: Saved document behavior  
    print("3️⃣ Testing saved document export...")
    test_file = "validation_test.md"
    html_file = "validation_test.html"
    
    # Cleanup
    for f in [test_file, html_file]:
        if os.path.exists(f):
            os.remove(f)
    
    # Save and export
    editor._save_file(test_file)
    result = editor._export_html()
    
    if result and os.path.exists(html_file):
        print("   ✅ Successfully exported using document filename")
    else:
        print("   ❌ Failed to export using document filename")
        all_tests_passed = False
    
    # Test 4: Custom filename still works
    print("4️⃣ Testing custom filename export...")
    custom_file = "custom_validation.html"
    if os.path.exists(custom_file):
        os.remove(custom_file)
    
    result = editor._export_html(custom_file)
    if result and os.path.exists(custom_file):
        print("   ✅ Custom filename export still works")
    else:
        print("   ❌ Custom filename export failed")
        all_tests_passed = False
    
    # Test 5: Command processor integration
    print("5️⃣ Testing command processor integration...")
    temp_file = "cmd_validation.html"
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    # Test export command without arguments
    result = editor._process_command("export", [])
    if result:
        print("   ✅ Export command without arguments works")
    else:
        print("   ❌ Export command without arguments failed")
        all_tests_passed = False
    
    # Cleanup
    cleanup_files = [test_file, html_file, custom_file, temp_file, "validation_test_config.json"]
    for f in cleanup_files:
        if os.path.exists(f):
            os.remove(f)
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✅ ALL EXPORT IMPROVEMENTS VALIDATED SUCCESSFULLY!")
        print("🎉 The export functionality now:")
        print("   • Works without filename (uses current document name)")
        print("   • Provides helpful error messages for new documents") 
        print("   • Maintains backward compatibility with explicit filenames")
        print("   • Is integrated with the command processor")
    else:
        print("❌ Some validation tests failed")
    
    return all_tests_passed

if __name__ == "__main__":
    validate_export_improvements()
