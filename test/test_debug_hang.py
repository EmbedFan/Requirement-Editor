#!/usr/bin/env python3
"""
Simple test to check what's causing the hang
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("1. Starting test...")

try:
    print("2. Importing TerminalEditor...")
    from libs.terminal_editor import TerminalEditor
    print("3. Creating editor instance...")
    editor = TerminalEditor()
    print("4. Editor created successfully")
    
    print("5. Creating new document...")
    editor._create_new_document()
    print("6. Document created successfully")
    
    print("7. Test completed without hanging!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
