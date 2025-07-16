#!/usr/bin/env python3
"""
Test script to identify where the raw content display issue occurs.
Tests various scenarios to reproduce the issue the user reported.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_display_scenarios():
    """Test different scenarios to identify the display issue."""
    test_file = os.path.join(os.path.dirname(__file__), 'data', 'new-2.md')
    
    print("=== Testing Display Scenarios ===")
    print(f"Test file: {test_file}")
    print()
    
    # Create editor instance
    editor = TerminalEditor()
    
    # Scenario 1: Load file directly
    print("1. Testing direct file load...")
    success = editor._load_file(test_file)
    print(f"Load success: {success}")
    
    if success:
        print("After load - editor state:")
        print(f"  Current file: {editor.current_file}")
        print(f"  Has md_editor: {editor.md_editor is not None}")
        if editor.md_editor:
            print(f"  Number of parts: {len(editor.md_editor.classified_parts)}")
        print()
        
        # Test display
        print("2. Testing display_document()...")
        editor.display_document()
        print()
        
        # Test individual parts display
        print("3. Testing individual part formatting...")
        if editor.md_editor:
            for i, part in enumerate(editor.md_editor.classified_parts[:3]):  # First 3 parts
                formatted = editor._format_line(part, show_full=True)
                print(f"Part {i+1} formatted: {formatted}")
        print()

if __name__ == "__main__":
    test_display_scenarios()
