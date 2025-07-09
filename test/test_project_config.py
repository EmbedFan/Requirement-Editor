#!/usr/bin/env python3
"""
Test script to verify project configuration working directory enforcement.

This script tests that project configuration files are always created in the
current working directory, regardless of user input.

Author: Attila Gallai <attila@tux-net.hu>
License: MIT License (see LICENSE.txt)
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to Python path to access libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.project import create_project_config, create_project_config_with_filename


def test_working_directory_enforcement():
    """Test that config files are always created in working directory."""
    
    print("Testing Project Configuration Working Directory Enforcement")
    print("=" * 60)
    
    # Get current working directory
    original_cwd = os.getcwd()
    
    # Create a temporary markdown file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_md:
        tmp_md.write("# Test Requirements\n\nThis is a test.")
        tmp_md_path = tmp_md.name
    
    try:
        # Test 1: Basic project creation
        print("\nTest 1: Basic project creation with default naming")
        project1 = create_project_config(tmp_md_path)
        
        if project1:
            expected_name = f"{Path(tmp_md_path).stem}_config.json"
            expected_path = os.path.join(original_cwd, expected_name)
            
            if os.path.exists(expected_path):
                print(f"✓ SUCCESS: Config file created at: {expected_path}")
                os.remove(expected_path)  # Clean up
            else:
                print(f"✗ FAILED: Expected config file not found at: {expected_path}")
        else:
            print("✗ FAILED: Project creation returned None")
        
        # Test 2: Project creation with custom name
        print("\nTest 2: Project creation with custom name")
        project2 = create_project_config(tmp_md_path, "custom_test")
        
        if project2:
            expected_path = os.path.join(original_cwd, "custom_test_config.json")
            
            if os.path.exists(expected_path):
                print(f"✓ SUCCESS: Config file created at: {expected_path}")
                os.remove(expected_path)  # Clean up
            else:
                print(f"✗ FAILED: Expected config file not found at: {expected_path}")
        else:
            print("✗ FAILED: Project creation returned None")
        
        # Test 3: Custom filename with path components (should be stripped)
        print("\nTest 3: Custom filename with path components (security test)")
        project3 = create_project_config_with_filename(tmp_md_path, "/tmp/malicious_config.json")
        
        if project3:
            # Should create in working directory, not /tmp/
            expected_path = os.path.join(original_cwd, "malicious_config.json")
            malicious_path = "/tmp/malicious_config.json"
            
            if os.path.exists(expected_path) and not os.path.exists(malicious_path):
                print(f"✓ SUCCESS: Config file safely created at: {expected_path}")
                print("✓ SUCCESS: Path traversal attack prevented")
                os.remove(expected_path)  # Clean up
            elif os.path.exists(malicious_path):
                print(f"✗ SECURITY FAILURE: File created at malicious path: {malicious_path}")
                os.remove(malicious_path)  # Clean up malicious file
            else:
                print(f"✗ FAILED: Expected config file not found at: {expected_path}")
        else:
            print("✗ FAILED: Project creation returned None")
        
        # Test 4: Filename without .json extension (should be added)
        print("\nTest 4: Filename without .json extension")
        project4 = create_project_config_with_filename(tmp_md_path, "no_extension")
        
        if project4:
            expected_path = os.path.join(original_cwd, "no_extension.json")
            
            if os.path.exists(expected_path):
                print(f"✓ SUCCESS: Config file created with .json extension: {expected_path}")
                os.remove(expected_path)  # Clean up
            else:
                print(f"✗ FAILED: Expected config file not found at: {expected_path}")
        else:
            print("✗ FAILED: Project creation returned None")
            
    finally:
        # Clean up temporary markdown file
        if os.path.exists(tmp_md_path):
            os.remove(tmp_md_path)
    
    print("\n" + "=" * 60)
    print("Test completed!")


if __name__ == "__main__":
    test_working_directory_enforcement()
