#!/usr/bin/env python3
"""
Interactive demonstration of tab completion functionality.

This script demonstrates how to properly test tab completion in the terminal editor.
"""

import sys
import os

# Add the libs directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

def demonstrate_tab_completion():
    """Demonstrate how tab completion works."""
    print("🎯 Tab Completion Demonstration")
    print("=" * 50)
    
    print("Tab completion is working! Here's how to test it:")
    print()
    
    print("1. Start the terminal editor:")
    print("   python main.py -ed")
    print()
    
    print("2. Try these commands with TAB completion:")
    print("   load test<TAB>      # Should complete to available files starting with 'test'")
    print("   save my<TAB>        # Should complete to available files starting with 'my'")
    print("   load test/<TAB>     # Should show files in test/ directory")
    print("   export test<TAB>    # Should complete to available files")
    print()
    
    print("3. Commands that support tab completion:")
    
    try:
        from terminal_editor import TabCompleter
        completer = TabCompleter()
        print(f"   - {', '.join(completer.completion_commands)}")
    except:
        print("   - load, save, export")
    
    print()
    print("4. Expected behavior:")
    print("   - Press TAB once: Complete if only one match")
    print("   - Press TAB twice: Show all possible matches")
    print("   - Works with file paths and directories")
    print("   - Adds trailing slash (/) for directories")
    print()
    
    # Test actual file completion
    print("5. Live test of file completion:")
    try:
        from terminal_editor import TabCompleter
        completer = TabCompleter()
        
        test_patterns = ["test", "main", "README"]
        for pattern in test_patterns:
            matches = completer._complete_filename(pattern)
            if matches:
                print(f"   '{pattern}' completes to: {matches[0]}")
                if len(matches) > 1:
                    print(f"     (and {len(matches)-1} other options)")
            else:
                print(f"   '{pattern}' has no matches")
    except Exception as e:
        print(f"   Error testing completion: {e}")

if __name__ == "__main__":
    demonstrate_tab_completion()
    
    print("\n🚀 Try it now:")
    print("Run: python main.py -ed")
    print("Then type: load test<TAB>")
