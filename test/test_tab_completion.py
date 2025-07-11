#!/usr/bin/env python3
"""
Test tab completion functionality in the terminal editor.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

from terminal_editor import TerminalEditor, TabCompleter

def test_tab_completion():
    """Test the tab completion functionality."""
    print("🧪 Testing Tab Completion Functionality")
    print("=" * 60)
    
    # Test 1: TabCompleter initialization
    print("1. Testing TabCompleter initialization...")
    completer = TabCompleter()
    setup_success = completer.setup_completion()
    print(f"   Setup successful: {setup_success}")
    print()
    
    # Test 2: File completion without actual input
    print("2. Testing file completion methods...")
    
    # Test completion in current directory
    matches = completer._complete_filename("")
    print(f"   Files in current directory: {len(matches)} found")
    for match in matches[:5]:  # Show first 5
        print(f"     - {match}")
    if len(matches) > 5:
        print(f"     ... and {len(matches) - 5} more")
    print()
    
    # Test .md file completion
    md_matches = completer._complete_filename("test")
    print(f"   Files starting with 'test': {len(md_matches)} found")
    for match in md_matches:
        print(f"     - {match}")
    print()
    
    # Test 3: TerminalEditor with tab completion
    print("3. Testing TerminalEditor tab completion integration...")
    editor = TerminalEditor()
    print(f"   Tab completion enabled: {editor.tab_completion_enabled}")
    print(f"   TabCompleter instance: {editor.tab_completer is not None}")
    print()
    
    print("✅ Tab completion test completed!")
    print()
    print("💡 To test manually:")
    print("   1. Run the main editor: python main.py")
    print("   2. Type: load test<TAB>")
    print("   3. See if it completes to 'test/' or shows test files")
    print("   4. Try: load test/data/<TAB>")
    print("   5. Try: save myfile<TAB>")

if __name__ == "__main__":
    test_tab_completion()
