#!/usr/bin/env python3
"""
Demo showing the DATTR read-only timestamp functionality.
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))

from terminal_editor import TerminalEditor

def demo_dattr_functionality():
    """Demonstrate the DATTR read-only timestamp functionality."""
    print("🎬 Demo: DATTR Read-Only Timestamp Management")
    print("=" * 60)
    
    editor = TerminalEditor()
    
    print("\n1. Creating new document with automatic timestamps...")
    editor._create_new_document()
    
    print("\n2. Document structure shows DATTR with timestamps:")
    editor.display_document()
    
    print("\n3. Attempting to edit DATTR (should be blocked)...")
    editor._process_command("edit", ["2", "Trying to change timestamps"])
    
    print("\n4. Saving document to update modification timestamp...")
    editor._process_command("saveas", ["demo_dattr.md"])
    
    print("\n5. Making a change and saving again...")
    time.sleep(1)  # Brief pause to ensure time difference
    editor._process_command("edit", ["4", "Updated requirement to test timestamp changes"])
    editor._process_command("save", [])
    
    print("\n6. Final document structure (note updated modification time):")
    editor.display_document()
    
    # Cleanup
    try:
        os.remove("demo_dattr.md")
        os.remove("demo_dattr_config.json")
        print("\n7. Demo completed and files cleaned up!")
    except:
        pass

if __name__ == "__main__":
    demo_dattr_functionality()
