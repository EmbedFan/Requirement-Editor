#!/usr/bin/env python3
"""
Test the corrected file loading with the terminal editor.
"""

import os
import sys

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

from terminal_editor import TerminalEditor

def test_corrected_file():
    """Test the corrected file loading."""
    
    print("🎉 Testing Corrected File Loading")
    print("=" * 60)
    
    editor = TerminalEditor()
    
    # Load the file
    success = editor._load_file("test/data/new-2.md")
    
    if success:
        print("✅ File loaded successfully!")
        print(f"📄 Current file: {editor.current_file}")
        
        if editor.md_editor:
            items = editor.md_editor.list_all_items()
            print(f"📋 Total items: {len(items)}")
            print()
            print("📊 Document structure:")
            
            for item in items:
                indent = "  " * (item.get('indent_level', 0))
                type_short = item['type'][:4].upper()
                desc = item['description']
                print(f"  {item['line_number']}│ {indent}[{type_short}] {desc}")
                
        print()
        print("🎯 This is how it should look in the terminal editor!")
        
    else:
        print("❌ Failed to load file")
    
    print("=" * 60)

if __name__ == "__main__":
    test_corrected_file()
