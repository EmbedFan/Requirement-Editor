#!/usr/bin/env python3
"""
Demonstrate the manual completion functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

from terminal_editor import TerminalEditor

def demo_manual_completion():
    """Demonstrate manual completion functionality."""
    print("🎯 Manual File Completion Demo")
    print("=" * 60)
    
    editor = TerminalEditor()
    
    print(f"Tab completion status: {'✅ Enabled' if editor.tab_completion_enabled else '❌ Disabled (using manual completion)'}")
    print()
    
    # Demo 1: Complete 'test' in current directory
    print("Demo 1: Complete 'test' in current directory")
    print("Command: complete load test")
    editor.tab_completer.show_completion_help('load', 'test')
    
    # Demo 2: Complete empty string (show all files)
    print("Demo 2: Show all files in current directory")
    print("Command: complete load \"\"")
    editor.tab_completer.show_completion_help('load', '')
    
    # Demo 3: Complete path with directory
    print("Demo 3: Complete path with directory")
    print("Command: complete load test/")
    editor.tab_completer.show_completion_help('load', 'test/')
    
    # Demo 4: Complete .md files
    print("Demo 4: Look for .md files starting with 'README'")
    print("Command: complete load README")
    editor.tab_completer.show_completion_help('load', 'README')
    
    print("💡 Usage in the terminal editor:")
    print("   1. Start editor: python main.py")
    print("   2. Use: complete load <partial_filename>")
    print("   3. Copy the desired filename from the list")
    print("   4. Use: load <copied_filename>")
    print()
    print("🚀 This provides file completion even without TAB support!")

if __name__ == "__main__":
    demo_manual_completion()
