#!/usr/bin/env python3
"""Test script to verify terminal indentation fix."""

import sys
import os

# Add the parent directory to Python path to import libs
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.terminal_editor import TerminalEditor

def test_indentation():
    """Test the terminal editor indentation display."""
    editor = TerminalEditor()
    
    # Load a test file (adjust path since we're now in test directory)
    test_file = "data/test_input.md"
    editor._load_file(test_file)
    
    print("Testing terminal indentation display:")
    print("=" * 60)
    
    # Show first 10 parts with their indentation
    parts = editor.md_editor.classified_parts[:10]
    for i, part in enumerate(parts):
        display_part = part.copy()
        display_part['line_number'] = i + 1
        
        # Get indent level
        indent_level = part['indent']
        
        # Show the formatted line
        formatted_line = editor._format_line(display_part)
        
        print(f"Indent level {indent_level}: {formatted_line}")

if __name__ == "__main__":
    test_indentation()
