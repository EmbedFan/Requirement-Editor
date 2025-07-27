#!/usr/bin/env python3
"""Test script to verify terminal indentation fix."""

from libs.terminal_editor import TerminalEditor

def test_indentation():
    """Test the terminal editor indentation display."""
    editor = TerminalEditor()
    
    # Load a test file
    test_file = "test/data/test_input.md"
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
