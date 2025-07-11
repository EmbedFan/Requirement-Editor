#!/usr/bin/env python3
"""
Test the complete file loading solution with the terminal editor.
"""

import os
import sys

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

from terminal_editor import TerminalEditor

def test_complete_solution():
    """Test the complete file loading solution."""
    
    print("🧪 Testing Complete File Loading Solution")
    print("=" * 60)
    
    editor = TerminalEditor()
    
    test_file = "test/data/new-2"  # Without .md extension
    
    print(f"📄 Testing: python main.py -ed {test_file}")
    print()
    
    # Step 1: Test filename processing
    print("1. Testing filename processing...")
    processed_file = editor._process_filename_for_loading(test_file)
    
    if processed_file:
        print(f"   ✅ Found file: {processed_file}")
        
        # Step 2: Test file loading
        print("2. Testing file loading with encoding handling...")
        success = editor._load_file(processed_file)
        
        if success:
            print(f"   ✅ File loaded successfully!")
            print(f"   📄 Current file: {editor.current_file}")
            
            if editor.md_editor:
                items = editor.md_editor.list_all_items()
                print(f"   📋 Loaded {len(items)} items")
                
                # Show document structure
                print("3. Document structure:")
                for item in items[:5]:  # Show first 5 items
                    print(f"   Line {item['line_number']}: [{item['type']}] {item['description'][:50]}...")
            else:
                print(f"   ❌ Markdown editor not initialized")
        else:
            print(f"   ❌ Failed to load file")
    else:
        print(f"   ❌ Could not find file")
    
    print("=" * 60)
    print("🎉 Complete solution test finished!")

if __name__ == "__main__":
    test_complete_solution()
