#!/usr/bin/env python3
"""
Demo showing the new features: DATTR in new documents and modification date updates.
"""

import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))

from terminal_editor import TerminalEditor

def demo_new_features():
    """Demonstrate the new features."""
    print("🎬 Demo: New Features - DATTR and Modification Date Updates")
    print("=" * 70)
    
    editor = TerminalEditor()
    
    print("\n1. Creating new document with DATTR...")
    editor._create_new_document()
    
    print("\n2. Document structure (now includes DATTR):")
    editor.display_document()
    
    print("\n3. Saving document to test modification date...")
    editor._process_command("saveas", ["demo_features.md"])
    
    # Check the config file
    config_path = "demo_features_config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        print(f"\n4. Project configuration created:")
        print(f"   Creation date: {config_data.get('project_creation_date')}")
        print(f"   Modification date: {config_data.get('project_last_modification_date')}")
        print(f"   Note: Both dates include HH:mm format")
        
        # Show that editor settings are also saved
        editor_settings = config_data.get('editor_settings', {})
        print(f"   Display mode: {editor_settings.get('display_mode', 'not set')}")
    
    print("\n5. Making a change and saving again...")
    editor._process_command("edit", ["2", "Updated DATTR with new metadata"])
    editor._process_command("save", [])
    
    # Check the updated config
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            updated_config = json.load(f)
        
        print(f"\n6. Updated modification date:")
        print(f"   New modification date: {updated_config.get('project_last_modification_date')}")
        print(f"   (Should be different from creation date)")
    
    print("\n7. Demo completed!")
    
    # Cleanup
    try:
        os.remove("demo_features.md")
        os.remove(config_path)
        print("   Cleanup completed")
    except:
        pass

if __name__ == "__main__":
    demo_new_features()
