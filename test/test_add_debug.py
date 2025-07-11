#!/usr/bin/env python3
"""
Test adding items using different approaches.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_add_with_aliases():
    """Test adding items with aliases."""
    print("🧪 Testing add command with aliases...")
    
    editor = TerminalEditor()
    editor._create_new_document()
    
    print("\n1. Initial document:")
    editor._process_command("list", [])
    
    print("\n2. Testing add commands:")
    
    # Try adding at the end (after line 4)
    print("   Adding REQ after line 4...")
    result = editor._process_command("add", ["after", "4", "REQ", "New requirement using alias"])
    print(f"   Result: {result}")
    
    if result:
        print("   ✅ Add REQ succeeded")
        editor._process_command("list", [])
    else:
        print("   ❌ Add REQ failed")
    
    # Try adding a COM
    print("\n   Adding COM after line 5 (if previous worked)...")
    result = editor._process_command("add", ["after", "5", "COM", "New comment using alias"])
    print(f"   Result: {result}")
    
    if result:
        print("   ✅ Add COM succeeded")
        editor._process_command("list", [])
    else:
        print("   ❌ Add COM failed")

def test_add_normalization_directly():
    """Test the add command normalization directly."""
    print("\n🧪 Testing add command normalization...")
    
    editor = TerminalEditor()
    
    # Test the _process_add_command method arguments
    print("1. Testing _normalize_item_type with add command arguments:")
    
    test_types = ["REQ", "COM", "TIT", "SUB"]
    for test_type in test_types:
        normalized = editor._normalize_item_type(test_type)
        print(f"   '{test_type}' -> '{normalized}'")

if __name__ == "__main__":
    test_add_normalization_directly()
    test_add_with_aliases()
