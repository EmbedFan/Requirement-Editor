#!/usr/bin/env python3
"""
Quick interactive test to demonstrate tab completion.
"""

import sys
import os

# Test with actual readline functionality
def test_tab_completion():
    print("🎯 Quick Tab Completion Test")
    print("=" * 40)
    
    try:
        import readline
        
        # Simple test completion function
        def completer(text, state):
            options = [
                'test_file.md',
                'test_doc.md', 
                'test_simple.py',
                'testdatanew-2.md',
                'main.py',
                'README.md'
            ]
            matches = [opt for opt in options if opt.startswith(text)]
            if state < len(matches):
                return matches[state]
            return None
        
        # Set up completion
        readline.set_completer(completer)
        readline.parse_and_bind('tab: complete')
        
        print("✅ Tab completion is set up!")
        print("Try typing 'test' and press TAB:")
        print("(Press Ctrl+C to exit)")
        
        while True:
            try:
                user_input = input("test> ").strip()
                if user_input.lower() in ['quit', 'exit']:
                    break
                print(f"You entered: '{user_input}'")
            except KeyboardInterrupt:
                print("\n👋 Test completed!")
                break
            except EOFError:
                break
                
    except ImportError:
        print("❌ Readline not available")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_tab_completion()
