#!/usr/bin/env python3
"""
Comprehensive test for project configuration creation behavior
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from libs.project import create_project_config, load_project_config

def test_comprehensive_config_location():
    """Test comprehensive project config creation behavior across different scenarios"""
    
    print("=" * 60)
    print("COMPREHENSIVE PROJECT CONFIG LOCATION TEST")
    print("=" * 60)
    
    # Test 1: Config created in same directory as markdown file
    print("\n🧪 Test 1: Config creation in document directory")
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create nested directory structure
        doc_dir = os.path.join(temp_dir, "documents", "project1")
        os.makedirs(doc_dir)
        
        # Create markdown file in nested directory
        md_file = os.path.join(doc_dir, "requirements.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Project Requirements\n\n## REQ001 - Test\nTest requirement\n")
        
        print(f"📁 Document directory: {doc_dir}")
        print(f"📄 Markdown file: {md_file}")
        print(f"🏠 Current working dir: {os.getcwd()}")
        
        # Create project config
        project_config = create_project_config(md_file)
        
        if project_config:
            config_path = project_config.config_file_path
            print(f"⚙️  Config file: {config_path}")
            
            # Verify location
            md_dir = os.path.dirname(os.path.abspath(md_file))
            config_dir = os.path.dirname(os.path.abspath(config_path))
            
            if md_dir == config_dir:
                print("✅ PASS: Config created in same directory as markdown file")
                
                # Verify config file exists and has correct content
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                    
                    expected_md_path = os.path.abspath(md_file)
                    actual_md_path = os.path.abspath(config_data['input_md_file_path'])
                    
                    if expected_md_path == actual_md_path:
                        print("✅ PASS: Config contains correct markdown file path")
                    else:
                        print(f"❌ FAIL: Config path mismatch - Expected: {expected_md_path}, Got: {actual_md_path}")
                        return False
                else:
                    print("❌ FAIL: Config file does not exist")
                    return False
            else:
                print(f"❌ FAIL: Config in wrong directory - MD: {md_dir}, Config: {config_dir}")
                return False
        else:
            print("❌ FAIL: Failed to create project config")
            return False
    
    # Test 2: Config with custom name still goes to document directory
    print("\n🧪 Test 2: Custom named config in document directory")
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create different directory structure
        src_dir = os.path.join(temp_dir, "src", "docs")
        os.makedirs(src_dir)
        
        # Create markdown file
        md_file = os.path.join(src_dir, "specifications.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Specifications\n\n## SPEC001 - Feature\nSpecification content\n")
        
        print(f"📁 Document directory: {src_dir}")
        print(f"📄 Markdown file: {md_file}")
        
        # Create project config with custom name
        project_config = create_project_config(md_file, "custom_project")
        
        if project_config:
            config_path = project_config.config_file_path
            print(f"⚙️  Config file: {config_path}")
            
            # Verify location and name
            expected_config = os.path.join(src_dir, "custom_project_config.json")
            
            if os.path.abspath(config_path) == os.path.abspath(expected_config):
                print("✅ PASS: Custom named config created in correct location")
            else:
                print(f"❌ FAIL: Config location mismatch - Expected: {expected_config}, Got: {config_path}")
                return False
        else:
            print("❌ FAIL: Failed to create custom named project config")
            return False
    
    # Test 3: Relative vs absolute paths
    print("\n🧪 Test 3: Relative vs absolute path handling")
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create directory and change to it temporarily
        test_dir = os.path.join(temp_dir, "relative_test")
        os.makedirs(test_dir)
        original_cwd = os.getcwd()
        
        try:
            os.chdir(test_dir)
            
            # Create markdown file using relative path
            md_file = "relative_requirements.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write("# Relative Path Test\n\n## REQ001 - Test\nContent\n")
            
            print(f"📁 Working directory: {os.getcwd()}")
            print(f"📄 Markdown file (relative): {md_file}")
            
            # Create project config with relative path
            project_config = create_project_config(md_file)
            
            if project_config:
                config_path = project_config.config_file_path
                print(f"⚙️  Config file: {config_path}")
                
                # Verify config is in same directory as markdown file
                if os.path.dirname(os.path.abspath(config_path)) == os.getcwd():
                    print("✅ PASS: Relative path config created in correct location")
                else:
                    print("❌ FAIL: Relative path config in wrong location")
                    return False
            else:
                print("❌ FAIL: Failed to create project config with relative path")
                return False
                
        finally:
            os.chdir(original_cwd)
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED - Project config creation works correctly!")
    print("✅ Config files are always created in the same directory as the markdown document")
    print("✅ Both absolute and relative paths work correctly")
    print("✅ Custom project names work correctly")
    print("✅ Config file content is correct")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_comprehensive_config_location()
    if not success:
        sys.exit(1)
