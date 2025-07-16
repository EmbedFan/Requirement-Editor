#!/usr/bin/env python3
"""
Comprehensive Tab Completion Troubleshooting Script

This script diagnoses and fixes tab completion issues in the Requirement Editor.
"""

import sys
import os

# Add the libs directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

def check_environment():
    """Check the environment for tab completion support."""
    print("🔧 Environment Check")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Operating system: {os.name}")
    print(f"Platform: {sys.platform}")
    
    # Check if we're in an interactive terminal
    if hasattr(sys.stdin, 'isatty'):
        print(f"Interactive terminal: {sys.stdin.isatty()}")
    else:
        print("Interactive terminal: Unknown")
    
    print()

def test_readline_modules():
    """Test different readline implementations."""
    print("📚 Testing Readline Modules")
    print("=" * 50)
    
    # Test standard readline
    try:
        import readline
        print("✅ Standard readline module available")
        print(f"   Readline version: {getattr(readline, '__version__', 'Unknown')}")
        
        # Test key functions
        try:
            readline.get_line_buffer
            print("   ✅ get_line_buffer available")
        except AttributeError:
            print("   ❌ get_line_buffer not available")
            
        try:
            readline.set_completer
            print("   ✅ set_completer available")
        except AttributeError:
            print("   ❌ set_completer not available")
            
    except ImportError:
        print("❌ Standard readline not available")
        
        # Try pyreadline3
        try:
            import pyreadline3 as readline
            print("✅ pyreadline3 available as fallback")
        except ImportError:
            print("❌ pyreadline3 not available either")
            print("💡 Install with: pip install pyreadline3")
            return False
    
    print()
    return True

def test_tab_completion_setup():
    """Test the actual tab completion setup."""
    print("🎯 Testing Tab Completion Setup")
    print("=" * 50)
    
    try:
        from terminal_editor import TabCompleter, TerminalEditor
        
        # Test TabCompleter
        print("Testing TabCompleter...")
        completer = TabCompleter()
        setup_result = completer.setup_completion()
        print(f"   Setup result: {setup_result}")
        
        if setup_result:
            # Test completion
            matches = completer._complete_filename("test")
            print(f"   Test completion for 'test': {len(matches)} matches")
            for i, match in enumerate(matches[:3]):
                print(f"     {i+1}. {match}")
            if len(matches) > 3:
                print(f"     ... and {len(matches)-3} more")
        
        # Test TerminalEditor
        print("\nTesting TerminalEditor...")
        editor = TerminalEditor()
        print(f"   Tab completion enabled: {editor.tab_completion_enabled}")
        print(f"   Completion commands: {editor.tab_completer.completion_commands}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing tab completion: {e}")
        return False

def create_interactive_test():
    """Create a simple interactive test."""
    print("🧪 Interactive Test")
    print("=" * 50)
    
    print("Testing basic readline functionality...")
    
    try:
        import readline
        
        def simple_completer(text, state):
            options = ['test_file.md', 'test_doc.md', 'test_simple.py', 'main.py', 'README.md']
            matches = [opt for opt in options if opt.startswith(text)]
            if state < len(matches):
                return matches[state]
            return None
        
        # Set up simple completion
        readline.set_completer(simple_completer)
        readline.parse_and_bind('tab: complete')
        
        print("✅ Simple completion setup complete")
        print("Try typing 'test' and pressing TAB:")
        
        try:
            user_input = input("test_prompt> ")
            print(f"You entered: {user_input}")
        except KeyboardInterrupt:
            print("\n✅ Test cancelled")
        except Exception as e:
            print(f"❌ Error during input: {e}")
            
    except Exception as e:
        print(f"❌ Error setting up test: {e}")

def main():
    """Main troubleshooting function."""
    print("🛠️  Tab Completion Troubleshooter")
    print("=" * 60)
    print()
    
    # Run all checks
    check_environment()
    
    if not test_readline_modules():
        print("❌ Cannot proceed without readline support")
        return
    
    if not test_tab_completion_setup():
        print("❌ Tab completion setup failed")
        return
    
    print("✅ All checks passed!")
    print()
    print("🎯 How to test tab completion:")
    print("1. Run: python main.py -ed")
    print("2. Type: load test")
    print("3. Press TAB (without hitting Enter)")
    print("4. You should see completion options or the text should complete")
    print()
    print("📝 Supported commands for tab completion:")
    print("   - load <filename>")
    print("   - save <filename>") 
    print("   - saveas <filename>")
    print("   - export <filename>")
    print()
    
    # Optional interactive test
    response = input("Would you like to run a simple interactive test? (y/N): ").strip().lower()
    if response.startswith('y'):
        create_interactive_test()

if __name__ == "__main__":
    main()
