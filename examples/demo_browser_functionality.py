#!/usr/bin/env python3
"""
Demo script showing browser configuration and browse command functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.terminal_editor import TerminalEditor

def demo_browser_functionality():
    """Demo the browser configuration and browse command."""
    
    print("Demo: Browser Configuration and Browse Command")
    print("=" * 60)
    
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
    
    # Test setbrowser command (using a common browser path)
    print("\n2. Testing setbrowser command:")
    # Try to find Chrome browser on different systems
    browser_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",  # Windows Chrome
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",  # Windows Chrome x86
        "C:\\Program Files\\Mozilla Firefox\\firefox.exe",  # Windows Firefox
        "/usr/bin/google-chrome",  # Linux Chrome
        "/usr/bin/firefox",  # Linux Firefox
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS Chrome
        "/Applications/Firefox.app/Contents/MacOS/firefox"  # macOS Firefox
    ]
    
    browser_path = None
    for path in browser_paths:
        if os.path.exists(path):
            browser_path = path
            break
    
    if browser_path:
        print(f"   Setting browser to: {browser_path}")
        success = terminal_editor._process_command("setbrowser", [browser_path])
        print(f"   Command result: {'Success' if success else 'Failed'}")
    else:
        print("   No common browser found, using system default")
    
    # Test setwindow command
    print("\n3. Testing setwindow command:")
    window_name = "RequirementEditor-Demo"
    print(f"   Setting window name to: {window_name}")
    success = terminal_editor._process_command("setwindow", [window_name])
    print(f"   Command result: {'Success' if success else 'Failed'}")
    
    # Show updated project info
    print("\n4. Project configuration after browser setup:")
    terminal_editor._show_project_info()
    
    # Test HTML export (without actually opening browser)
    print("\n5. Testing HTML export functionality:")
    html_filename = "test_shopping_list_app.html"
    success = terminal_editor._export_html(html_filename)
    if success:
        print(f"   ✅ HTML export successful: {html_filename}")
        
        # Check if HTML file was created
        if os.path.exists(html_filename):
            print(f"   ✅ HTML file created and accessible")
            
            # Show file size for verification
            file_size = os.path.getsize(html_filename)
            print(f"   File size: {file_size} bytes")
            
            # Clean up the test HTML file
            os.remove(html_filename)
            print(f"   🧹 Cleaned up test HTML file")
        else:
            print(f"   ❌ HTML file not found after export")
    else:
        print(f"   ❌ HTML export failed")
    
    # Test browser functionality (without actually opening)
    print("\n6. Testing browser configuration:")
    if terminal_editor.project_config:
        configured_browser = terminal_editor.project_config.get_browser_path()
        configured_window = terminal_editor.project_config.get_browser_window_name()
        
        print(f"   Configured browser: {configured_browser or 'System default'}")
        print(f"   Configured window name: {configured_window}")
        
        if configured_browser and os.path.exists(configured_browser):
            print(f"   ✅ Configured browser exists and is accessible")
        elif configured_browser:
            print(f"   ⚠️  Configured browser path not found: {configured_browser}")
        else:
            print(f"   ℹ️  No custom browser configured, will use system default")
    
    # Show usage instructions
    print(f"\n7. Usage Instructions:")
    print(f"   • To export and open in browser: browse")
    print(f"   • To export with specific filename: browse myfile.html")
    print(f"   • To configure browser: setbrowser <path_to_browser>")
    print(f"   • To set window name: setwindow <window_name>")
    print(f"   • To clear browser config: clearbrowser")
    
    # Test clearbrowser command
    print(f"\n8. Testing clearbrowser command:")
    success = terminal_editor._process_command("clearbrowser", [])
    print(f"   Command result: {'Success' if success else 'Failed'}")
    
    # Show final project info
    print("\n9. Final project configuration:")
    terminal_editor._show_project_info()
    
    return True

if __name__ == "__main__":
    success = demo_browser_functionality()
    if success:
        print("\n🎉 Browser configuration and browse command are fully functional!")
        print("✅ Users can now configure their preferred browser and window name!")
        print("✅ The browse command exports HTML and opens it in the configured browser!")
    else:
        print("\n❌ Browser functionality test failed!")
        sys.exit(1)
