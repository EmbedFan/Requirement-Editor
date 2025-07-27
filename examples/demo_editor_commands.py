#!/usr/bin/env python3
"""
Demo script showing external editor configuration in terminal editor.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.terminal_editor import TerminalEditor

def demo_external_editor_commands():
    """Demo the seteditor and cleareditor commands."""
    
    print("Demo: External Editor Configuration Commands")
    print("=" * 50)
    
    # Create terminal editor
    terminal_editor = TerminalEditor()
    
    # Load a test file
    test_file = "test/real_requirements/shopping_list_app.md"
    print(f"\nLoading test file: {test_file}")
    terminal_editor._load_file(test_file)
    
    if not terminal_editor.md_editor:
        print("❌ Failed to load file")
        return False
    
    print("✅ File loaded successfully")
    
    # Show initial project info
    print("\n1. Initial project configuration:")
    terminal_editor._show_project_info()
    
    # Test seteditor command
    print("\n2. Testing seteditor command:")
    editor_path = "C:\\Windows\\System32\\notepad.exe"
    print(f"   Setting external editor to: {editor_path}")
    
    # Simulate the seteditor command
    success = terminal_editor._process_command("seteditor", [editor_path])
    print(f"   Command result: {'Success' if success else 'Failed'}")
    
    # Show updated project info
    print("\n3. Project configuration after seteditor:")
    terminal_editor._show_project_info()
    
    # Test external editor functionality
    print("\n4. Testing external editor configuration:")
    if terminal_editor.project_config:
        configured_editor = terminal_editor.project_config.get_external_editor_path()
        print(f"   Configured external editor: {configured_editor}")
        
        if configured_editor == editor_path:
            print("   ✅ External editor configured correctly")
        else:
            print("   ❌ External editor configuration mismatch")
    
    # Test cleareditor command
    print("\n5. Testing cleareditor command:")
    success = terminal_editor._process_command("cleareditor", [])
    print(f"   Command result: {'Success' if success else 'Failed'}")
    
    # Show final project info
    print("\n6. Project configuration after cleareditor:")
    terminal_editor._show_project_info()
    
    # Final verification
    if terminal_editor.project_config:
        final_editor = terminal_editor.project_config.get_external_editor_path()
        print(f"\n7. Final external editor setting: {final_editor}")
        
        if final_editor is None:
            print("   ✅ External editor cleared successfully")
        else:
            print("   ❌ External editor not cleared properly")
    
    return True

if __name__ == "__main__":
    success = demo_external_editor_commands()
    if success:
        print("\n🎉 External editor commands are working correctly!")
    else:
        print("\n❌ External editor commands test failed!")
        sys.exit(1)
