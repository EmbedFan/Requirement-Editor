#!/usr/bin/env python3
"""
Interactive test of the terminal editor saveas functionality.

This test demonstrates:
1. Creating a new document
2. Using saveas with various filename scenarios
3. Verifying that filename processing works correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def interactive_saveas_test():
    """Interactive test of saveas functionality."""
    print("🧪 Interactive Terminal Editor Saveas Test")
    print("=" * 50)
    
    editor = TerminalEditor()
    
    print("\n1. Creating a new document...")
    editor._create_new_document()
    
    print("\n2. Document created! Here's the structure:")
    editor.display_document()
    
    print("\n" + "=" * 50)
    print("Now let's test the saveas command with different scenarios:")
    print("=" * 50)
    
    # Test scenarios
    scenarios = [
        ("test_doc", "Filename without extension - should add .md"),
        ("test_doc2.txt", "Filename with wrong extension - should change to .md"),
        ("test_doc3.md", "Filename with correct extension - should work as-is"),
        ("test_doc", "Existing file - should prompt for overwrite")
    ]
    
    for i, (filename, description) in enumerate(scenarios, 1):
        print(f"\nScenario {i}: {description}")
        print(f"Command: saveas {filename}")
        print("-" * 30)
        
        # Use the command processor to test the actual saveas command
        result = editor._process_command("saveas", [filename])
        
        if result:
            print(f"✅ Command succeeded")
        else:
            print(f"❌ Command failed (this might be expected for overwrite decline)")
    
    print("\n" + "=" * 50)
    print("Test completed! Check the files that were created.")
    print("=" * 50)

if __name__ == "__main__":
    interactive_saveas_test()
