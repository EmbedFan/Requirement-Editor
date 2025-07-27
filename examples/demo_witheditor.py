#!/usr/bin/env python3
"""
Interactive demo for the witheditor command.

This script creates a test document and demonstrates how to use
the witheditor command to edit items with an external editor.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_witheditor():
    """Demo the witheditor command functionality."""
    print("📝 Witheditor Command Demo")
    print("=" * 40)
    print()
    
    print("🚀 New Feature: Edit with External Editor")
    print("The 'witheditor' command opens your system's text editor")
    print("for editing item descriptions - perfect for longer text!")
    print()
    
    print("✨ Key Features:")
    print("• Opens system default text editor (Notepad on Windows)")
    print("• Works with any text that can be edited inline")
    print("• Preserves formatting and allows multi-line editing")
    print("• Safe - creates temporary file, cleans up automatically")
    print("• Protects DATTR items (read-only timestamps)")
    print()
    
    print("📋 Usage:")
    print("1. Start the terminal editor: python main.py -ed")
    print("2. Create or load a document")
    print("3. Use: witheditor <line_number>")
    print("   Example: witheditor 4")
    print("4. Edit in the external editor")
    print("5. Save and close the editor")
    print("6. Content is automatically updated")
    print()
    
    print("💡 Comparison:")
    print("edit 4 'New text here'          ← Edit inline (good for short text)")
    print("witheditor 4                    ← Edit externally (good for long text)")
    print()
    
    print("🔧 Technical Details:")
    print("• Windows: Uses notepad.exe or system default")
    print("• Unix/Linux: Uses $EDITOR environment variable or nano")
    print("• Creates temporary .txt file for editing")
    print("• UTF-8 encoding support for international characters")
    print("• Automatic cleanup of temporary files")
    print()
    
    print("🎯 Try it now:")
    print("python main.py -ed")
    print("> new")
    print("> witheditor 4")
    print("(Edit the requirement in notepad, save, close)")
    print("> list")
    print("(See your changes!)")

if __name__ == "__main__":
    demo_witheditor()
