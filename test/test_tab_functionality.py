#!/usr/bin/env python3
"""
Test to identify why tab completion is not working.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

def test_readline_availability():
    """Test if readline is available and working."""
    print("🔍 Testing Tab Completion Issues")
    print("=" * 50)
    
    # Test 1: Check readline availability
    print("1. Testing readline availability...")
    try:
        import readline
        print("   ✅ readline module imported successfully")
        
        # Test basic readline functions
        try:
            readline.set_completer(lambda text, state: None)
            print("   ✅ set_completer works")
        except Exception as e:
            print(f"   ❌ set_completer failed: {e}")
            
        try:
            readline.parse_and_bind('tab: complete')
            print("   ✅ parse_and_bind works")
        except Exception as e:
            print(f"   ❌ parse_and_bind failed: {e}")
            
    except ImportError as e:
        print(f"   ❌ readline not available: {e}")
        
        # Try pyreadline3
        try:
            import pyreadline3 as readline
            print("   ✅ pyreadline3 imported successfully")
        except ImportError as e2:
            print(f"   ❌ pyreadline3 also not available: {e2}")
    
    print()
    
    # Test 2: Test TabCompleter directly
    print("2. Testing TabCompleter class...")
    try:
        from terminal_editor import TabCompleter
        
        completer = TabCompleter()
        print("   ✅ TabCompleter created")
        
        # Test setup
        setup_success = completer.setup_completion()
        print(f"   Setup success: {setup_success}")
        
        # Test file completion manually
        matches = completer._complete_filename("test")
        print(f"   File completion test: {len(matches)} matches found")
        for match in matches[:3]:
            print(f"     - {match}")
        
    except Exception as e:
        print(f"   ❌ TabCompleter test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Test 3: Test TerminalEditor integration
    print("3. Testing TerminalEditor integration...")
    try:
        from terminal_editor import TerminalEditor
        
        editor = TerminalEditor()
        print("   ✅ TerminalEditor created")
        print(f"   Tab completion enabled: {editor.tab_completion_enabled}")
        
        if hasattr(editor, 'tab_completer'):
            print("   ✅ TabCompleter instance exists")
        else:
            print("   ❌ No TabCompleter instance")
            
    except Exception as e:
        print(f"   ❌ TerminalEditor test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("🎯 Recommendations:")
    print("   1. If readline is not available, install it: pip install pyreadline3")
    print("   2. Use manual completion: complete load <partial_filename>")
    print("   3. Check if your terminal supports readline functionality")

if __name__ == "__main__":
    test_readline_availability()
