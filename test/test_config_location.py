#!/usr/bin/env python3
"""
Test script to verify project configuration creation location
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

from project import create_project_config

def test_config_location():
    """Test that project config is created in the same directory as the markdown file"""
    
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a subdirectory for our test
        test_dir = os.path.join(temp_dir, "test_project")
        os.makedirs(test_dir)
        
        # Create a test markdown file in the subdirectory
        md_file = os.path.join(test_dir, "requirements.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Test Requirements\n\n## REQ001 - Test Requirement\nTest content\n")
        
        print(f"Created test markdown file: {md_file}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Test directory: {test_dir}")
        
        # Create project config
        project_config = create_project_config(md_file, "test_project")
        
        if project_config:
            config_path = project_config.config_file_path
            print(f"Config file created at: {config_path}")
            
            # Check if config file is in the same directory as the markdown file
            md_dir = os.path.dirname(os.path.abspath(md_file))
            config_dir = os.path.dirname(os.path.abspath(config_path))
            
            print(f"Markdown directory: {md_dir}")
            print(f"Config directory: {config_dir}")
            
            if md_dir == config_dir:
                print("✅ SUCCESS: Config file created in same directory as markdown file")
                return True
            else:
                print("❌ FAIL: Config file NOT in same directory as markdown file")
                return False
        else:
            print("❌ FAIL: Failed to create project config")
            return False

if __name__ == "__main__":
    success = test_config_location()
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
