#!/usr/bin/env python3
"""
Verification test for project config directory behavior
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add libs to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))

from project import create_project_config

def test_issue_resolution():
    """Verify that the reported issue is actually resolved"""
    
    print("=" * 70)
    print("🔍 ISSUE VERIFICATION: Project Config Directory Behavior")
    print("=" * 70)
    
    print("\n📋 ISSUE REPORT:")
    print("   'The project config files always shall be created the same directory where the document saved. Now it does not work'")
    
    print("\n🧪 TESTING ACTUAL BEHAVIOR:")
    
    test_cases = []
    
    # Test Case 1: Simple case in temp directory
    print("\n   Test 1: Basic directory behavior")
    with tempfile.TemporaryDirectory() as temp_dir:
        docs_dir = os.path.join(temp_dir, "documents") 
        os.makedirs(docs_dir)
        
        md_file = os.path.join(docs_dir, "test.md")
        with open(md_file, 'w') as f:
            f.write("# Test Document\n")
        
        project_config = create_project_config(md_file)
        if project_config:
            config_path = project_config.config_file_path
            md_dir = os.path.dirname(md_file)
            config_dir = os.path.dirname(config_path)
            
            result = md_dir == config_dir
            test_cases.append(("Basic case", result))
            print(f"      📄 Markdown: {md_file}")
            print(f"      ⚙️  Config:   {config_path}")
            print(f"      ✅ Same dir: {'YES' if result else 'NO'}")
        else:
            test_cases.append(("Basic case", False))
            print("      ❌ Failed to create config")
    
    # Test Case 2: Deep nested structure
    print("\n   Test 2: Deep nested directory structure")
    with tempfile.TemporaryDirectory() as temp_dir:
        deep_dir = os.path.join(temp_dir, "projects", "client1", "docs", "requirements")
        os.makedirs(deep_dir)
        
        md_file = os.path.join(deep_dir, "spec.md")
        with open(md_file, 'w') as f:
            f.write("# Specification Document\n")
        
        project_config = create_project_config(md_file, "client1_spec")
        if project_config:
            config_path = project_config.config_file_path
            md_dir = os.path.dirname(md_file)
            config_dir = os.path.dirname(config_path)
            
            result = md_dir == config_dir
            test_cases.append(("Deep nested", result))
            print(f"      📄 Markdown: {md_file}")
            print(f"      ⚙️  Config:   {config_path}")
            print(f"      ✅ Same dir: {'YES' if result else 'NO'}")
        else:
            test_cases.append(("Deep nested", False))
            print("      ❌ Failed to create config")
    
    # Test Case 3: Relative paths
    print("\n   Test 3: Relative path handling")
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            test_subdir = os.path.join(temp_dir, "workdir")
            os.makedirs(test_subdir)
            os.chdir(test_subdir)
            
            md_file = "relative_test.md"
            with open(md_file, 'w') as f:
                f.write("# Relative Test\n")
            
            project_config = create_project_config(md_file)
            if project_config:
                config_path = project_config.config_file_path
                md_dir = os.path.dirname(os.path.abspath(md_file))
                config_dir = os.path.dirname(os.path.abspath(config_path))
                
                result = md_dir == config_dir
                test_cases.append(("Relative path", result))
                print(f"      📄 Markdown: {os.path.abspath(md_file)}")
                print(f"      ⚙️  Config:   {os.path.abspath(config_path)}")
                print(f"      ✅ Same dir: {'YES' if result else 'NO'}")
            else:
                test_cases.append(("Relative path", False))
                print("      ❌ Failed to create config")
        finally:
            os.chdir(original_cwd)
    
    # Results Summary
    print("\n📊 TEST RESULTS SUMMARY:")
    all_passed = all(result for _, result in test_cases)
    for test_name, result in test_cases:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")
    
    print("\n🎯 CONCLUSION:")
    if all_passed:
        print("   ✅ ALL TESTS PASSED")
        print("   ✅ Project config files ARE being created in the same directory as the document")
        print("   ✅ The implementation is working correctly")
        print("   ✅ The reported issue appears to be RESOLVED or was a misunderstanding")
    else:
        print("   ❌ SOME TESTS FAILED")
        print("   ❌ There may be an actual issue with the implementation")
    
    print("\n📝 RECOMMENDATION:")
    if all_passed:
        print("   The current implementation is working as intended.")
        print("   Config files are correctly placed in the same directory as the markdown documents.")
        print("   No code changes are needed - the feature is working correctly.")
    else:
        print("   Investigation needed - there may be a real issue to fix.")
    
    print("=" * 70)
    return all_passed

if __name__ == "__main__":
    success = test_issue_resolution()
    sys.exit(0 if success else 1)
