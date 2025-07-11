#!/usr/bin/env python3
"""
Integration test for terminal editor config creation location
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

from terminal_editor import TerminalEditor
from md_edit import MarkdownEditor

def test_terminal_editor_config_location():
    """Test that terminal editor creates config in the same directory as saved files"""
    
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a subdirectory for our test
        test_dir = os.path.join(temp_dir, "docs", "requirements")
        os.makedirs(test_dir)
        
        print(f"Test directory: {test_dir}")
        print(f"Current working directory: {os.getcwd()}")
        
        # Create terminal editor
        terminal_editor = TerminalEditor()
        
        # Create a new document
        terminal_editor.md_editor = MarkdownEditor()
        terminal_editor.md_editor.create_new_document()
        
        # Save to the test directory
        md_file = os.path.join(test_dir, "test_requirements.md")
        
        # Simulate saving the file 
        result = terminal_editor.md_editor.save_to_file(md_file)
        if result:
            print(f"Saved markdown file: {md_file}")
            
            # Simulate the config creation (this happens in _save_common)
            if not terminal_editor.project_config:
                from project import create_project_config
                base_name = os.path.splitext(os.path.basename(md_file))[0]
                terminal_editor.project_config = create_project_config(md_file, base_name)
                
                if terminal_editor.project_config:
                    config_path = terminal_editor.project_config.config_file_path
                    print(f"Config file created at: {config_path}")
                    
                    # Check if config file is in the same directory as the markdown file
                    md_dir = os.path.dirname(os.path.abspath(md_file))
                    config_dir = os.path.dirname(os.path.abspath(config_path))
                    
                    print(f"Markdown directory: {md_dir}")
                    print(f"Config directory: {config_dir}")
                    
                    if md_dir == config_dir:
                        print("✅ SUCCESS: Terminal editor creates config in same directory as markdown file")
                        return True
                    else:
                        print("❌ FAIL: Config file NOT in same directory as markdown file")
                        return False
                else:
                    print("❌ FAIL: Failed to create project config")
                    return False
        else:
            print("❌ FAIL: Failed to save markdown file")
            return False

if __name__ == "__main__":
    success = test_terminal_editor_config_location()
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
