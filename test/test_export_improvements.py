#!/usr/bin/env python3
"""
Test improved export functionality
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_export_improvements():
    """Test the improved export functionality."""
    print("🔧 Testing Export Improvements")
    print("=" * 50)
    
    editor = TerminalEditor()
    
    # Test 1: Export without filename on new document (should fail with helpful message)
    print("\n1️⃣ Testing export without filename on new document...")
    editor._create_new_document()
    result = editor._export_html()
    if not result:
        print("   ✅ Correctly handled new document without filename")
    else:
        print("   ❌ Should have failed with helpful message")
    
    # Test 2: Save document and then export without filename (should work)
    print("\n2️⃣ Testing export without filename after saving document...")
    test_filename = "test_export_demo.md"
    test_html_filename = "test_export_demo.html"
    
    # Clean up any existing files
    for f in [test_filename, test_html_filename]:
        if os.path.exists(f):
            os.remove(f)
    
    # Save the document first
    save_result = editor._save_file(test_filename)
    if save_result:
        print(f"   ✅ Document saved as: {test_filename}")
        
        # Now export without specifying filename
        export_result = editor._export_html()
        if export_result and os.path.exists(test_html_filename):
            print(f"   ✅ HTML export successful: {test_html_filename}")
        else:
            print("   ❌ HTML export failed")
    else:
        print("   ❌ Failed to save document")
    
    # Test 3: Export with specific filename (should still work)
    print("\n3️⃣ Testing export with specific filename...")
    custom_html = "custom_export_test.html"
    if os.path.exists(custom_html):
        os.remove(custom_html)
    
    export_result = editor._export_html(custom_html)
    if export_result and os.path.exists(custom_html):
        print(f"   ✅ Custom filename export successful: {custom_html}")
    else:
        print("   ❌ Custom filename export failed")
    
    print("\n" + "=" * 50)
    
    # Cleanup test files
    cleanup_files = [test_filename, test_html_filename, custom_html]
    for f in cleanup_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"🧹 Cleaned up: {f}")
    
    print("✅ Export improvement tests completed!")

def test_export_commands():
    """Test the export commands through the command processor."""
    print("\n🧪 Testing Export Commands")
    print("=" * 30)
    
    editor = TerminalEditor()
    
    # Create and save a test document
    test_filename = "cmd_test_export.md"
    test_html_filename = "cmd_test_export.html"
    
    # Clean up any existing files
    for f in [test_filename, test_html_filename]:
        if os.path.exists(f):
            os.remove(f)
    
    print("📝 Creating and saving test document...")
    editor._create_new_document()
    editor._save_file(test_filename)
    
    # Test export command without arguments
    print("🔧 Testing 'export' command without filename...")
    result = editor._process_command("export", [])
    if result and os.path.exists(test_html_filename):
        print("   ✅ Export command without filename works!")
    else:
        print("   ❌ Export command without filename failed")
    
    # Cleanup
    for f in [test_filename, test_html_filename]:
        if os.path.exists(f):
            os.remove(f)
    
    print("✅ Command tests completed!")

if __name__ == "__main__":
    test_export_improvements()
    test_export_commands()
