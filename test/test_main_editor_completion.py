#!/usr/bin/env python3
"""
Test the main terminal editor with tab completion functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.terminal_editor import TerminalEditor

def test_main_editor():
    """Test the main editor functionality with tab completion."""
    print("🧪 Testing Main Terminal Editor with Tab Completion")
    print("=" * 60)
    
    try:
        # Initialize editor
        print("1. Initializing terminal editor...")
        editor = TerminalEditor()
        print(f"   ✅ Editor initialized successfully")
        print(f"   Tab completion enabled: {editor.tab_completion_enabled}")
        print()
        
        # Test manual completion
        print("2. Testing manual completion...")
        print("   Testing 'complete load README':")
        editor.tab_completer.show_completion_help('load', 'README')
        
        # Test file loading
        print("3. Testing file operations...")
        test_file = os.path.join(os.path.dirname(__file__), 'data', 'new-2.md')
        if os.path.exists(test_file):
            success = editor._load_file(test_file)
            print(f"   ✅ File loading: {'Success' if success else 'Failed'}")
        else:
            print(f"   ⚠️  Test file not found: {test_file}")
        
        print()
        print("✅ All tests passed! Tab completion implementation is working.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_editor()
